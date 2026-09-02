#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""受限的 CTC beam search 解碼：只走合法音節的字首樹，並用正本的音節 bigram 打分。

kraken 預設是逐格取最大機率的貪婪解碼，會吐出「da̤̍u̍h」這種兩個調符的音節。
這裡改成 prefix beam search，每條路徑記住「目前這個音節到哪一個字首樹節點」：
離開字首樹（不可能成為合法音節）扣 oov_penalty，音節收尾時不是完整音節扣 incomplete_penalty，
完整音節加上 lm_weight × log P(音節 | 前一音節)。大小寫不管；數字、標點、空格、連字號是音節邊界；
連字號前後不能有空格。

  decode.py -m models/x.mlmodel --manifest dataset/pages_test_auto.txt --labels dataset/pages_test_auto_labels.json
      → 比較貪婪與 beam 解碼的 CER（可用 --lm-weight、--beam、--oov-penalty 掃參數）
其餘腳本用 line_decoder() 取得解碼函式。
"""

import argparse
import collections
import json
import math
import re
import sys
import unicodedata
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import DATA, WORK, cer, load_rom_verses, nfc, nfd  # noqa: E402

INITIALS = ["", "b", "p", "m", "d", "t", "n", "l", "g", "k", "ng", "h", "c", "ch", "s"]
UNK = "<unk>"


def valid_syllables():
    finals = [l.strip() for l in open(DATA / "hinghua-finals.txt", encoding="utf-8") if l.strip() and not l.startswith("#")]
    return {nfd(i + f) for i in INITIALS for f in finals}


class Trie:
    __slots__ = ("children", "terminal")

    def __init__(self):
        self.children = {}
        self.terminal = False

    @classmethod
    def build(cls, words):
        root = cls()
        for w in words:
            node = root
            for ch in w:
                node = node.children.setdefault(ch, cls())
            node.terminal = True
        return root


def is_letter(ch):
    return ch.isalpha() or unicodedata.combining(ch) or ch == "ⁿ"


def syllable_tokens(text):
    """一節經文 → 音節序列（小寫 NFD，去掉標點與數字；數字處視為斷開的上下文）。"""
    out = []
    for tok in re.split(r"[\s\-]+", text):
        t = nfd(tok.lower()).strip("*")
        t = "".join(ch for ch in t if is_letter(ch))
        if t:
            out.append(t)
    return out


class SyllableLM:
    """音節 bigram，絕對折扣後退到 unigram；unigram 對 3,420 個合法音節做加法平滑。"""

    def __init__(self, texts, vocab, discount=0.75, alpha=0.5):
        self.uni = collections.Counter()
        self.bi = collections.defaultdict(collections.Counter)
        for t in texts:
            prev = None
            for s in syllable_tokens(t):
                s = s if s in vocab else UNK
                self.uni[s] += 1
                if prev is not None:
                    self.bi[prev][s] += 1
                prev = s
        self.total = sum(self.uni.values())
        self.vsize = len(vocab) + 1
        self.d, self.alpha = discount, alpha
        self.ctx_total = {p: sum(c.values()) for p, c in self.bi.items()}
        self.ctx_types = {p: len(c) for p, c in self.bi.items()}
        self._cache = {}
        # 訓練文本上的平均每音節成本（-log P），解碼時當作每個音節的插入獎勵，讓 LM 不偏好少出音節
        tot = n = 0
        for t in texts[:2000]:
            prev = None
            for s in syllable_tokens(t):
                s = s if s in vocab else UNK
                tot -= self.logp(prev, s)
                n += 1
                prev = s
        self.mean_cost = tot / max(n, 1)

    def logp_uni(self, s):
        return math.log((self.uni.get(s, 0) + self.alpha) / (self.total + self.alpha * self.vsize))

    def logp(self, prev, s):
        key = (prev, s)
        v = self._cache.get(key)
        if v is not None:
            return v
        pu = math.exp(self.logp_uni(s))
        if prev is None or prev not in self.bi:
            v = math.log(pu)
        else:
            n = self.ctx_total[prev]
            c = self.bi[prev].get(s, 0)
            lam = self.d * self.ctx_types[prev] / n
            v = math.log(max(c - self.d, 0) / n + lam * pu)
        self._cache[key] = v
        return v


def build_lm(vocab, exclude=None, **kw):
    """exclude：{英文書名: {(章, 節), …}} 不拿來估 bigram（評估時排除測試頁或受測書卷，避免看過答案）。"""
    filled = load_rom_verses()  # 不含 OCR 草稿
    exclude = exclude or {}
    texts = [t for eng, vs in filled.items() for k, t in vs.items() if k not in exclude.get(eng, set())]
    return SyllableLM(texts, vocab, **kw)


def verses_on_pages(pages):
    """這些頁上的經節（含頁首前一節），供 build_lm(exclude=…) 用。"""
    from common import load_page_map, prev_verse, verses_on_page
    pm, all_pages = load_page_map()
    out = collections.defaultdict(set)
    for p in pages:
        if p not in pm:
            continue
        eng, vs = verses_on_page(pm, all_pages, p)
        if vs:
            pv = prev_verse(eng, *vs[0])
            out[eng].update(vs + ([pv] if pv else []))
    return out


class Decoder:
    def __init__(self, l2c, trie, lm, beam=8, topk=6, lm_weight=0.5, oov_penalty=6.0, incomplete_penalty=3.0,
                 syllable_bonus=None):
        self.l2c = l2c  # label → 單一字元
        self.trie, self.lm = trie, lm
        self.beam, self.topk = beam, topk
        self.lm_weight, self.oov_penalty, self.incomplete_penalty = lm_weight, oov_penalty, incomplete_penalty
        # 每個音節的插入獎勵；預設抵銷 LM 的平均成本，避免權重一高就漏掉短音節
        self.syllable_bonus = lm_weight * lm.mean_cost if syllable_bonus is None else syllable_bonus

    # 每條路徑的音節狀態：(buf, node, prev, score)。node=None 表示已離開字首樹。
    def _extend(self, state, ch):
        buf, node, prev, score = state
        low = ch.lower()
        if is_letter(low):
            if node is None:
                return (buf + low, None, prev, score)
            nxt = node.children.get(low)
            if nxt is None:
                return (buf + low, None, prev, score - self.oov_penalty)
            return (buf + low, nxt, prev, score)
        return self._close(state, reset=ch.isdigit())

    def _close(self, state, reset=False):
        buf, node, prev, score = state
        if buf:
            # 每個音節收尾都付 bigram 成本；不合法的以 <unk> 計，這樣 LM 權重不會把路徑推出字首樹
            tok = buf if node is not None and node.terminal else UNK
            score += self.lm_weight * self.lm.logp(prev, tok) + self.syllable_bonus
            if tok == UNK and node is not None:
                score -= self.incomplete_penalty  # 字首合法但沒收完（如 gô 少了 ng）
            prev = tok
        if reset:
            prev = None
        return ("", self.trie, prev, score)

    def decode(self, probs):
        """probs: (C, W) softmax。回傳 (labels, 每個字元的機率)。"""
        logp = np.log(np.maximum(probs, 1e-12))
        C, W = logp.shape
        NEG = -1e30
        init_state = ("", self.trie, None, 0.0)
        # beam: prefix(tuple) → [log_pb, log_pnb, state, emits(list of prob)]
        beam = {(): [0.0, NEG, init_state, ()]}
        for t in range(W):
            col = logp[:, t]
            cands = np.argpartition(-col, min(self.topk, C - 1))[:self.topk]
            nxt = {}

            def add(prefix, pb, pnb, state, emits):
                e = nxt.get(prefix)
                if e is None:
                    nxt[prefix] = [pb, pnb, state, emits]
                else:
                    e[0] = np.logaddexp(e[0], pb)
                    e[1] = np.logaddexp(e[1], pnb)

            for prefix, (pb, pnb, state, emits) in beam.items():
                total = np.logaddexp(pb, pnb)
                # blank
                add(prefix, total + col[0], NEG, state, emits)
                last = prefix[-1] if prefix else None
                last_ch = self.l2c.get(last) if last is not None else None
                for c in cands:
                    c = int(c)
                    if c == 0:
                        continue
                    ch = self.l2c[c]
                    if (ch == " " and last_ch == "-") or (ch == "-" and last_ch == " "):
                        continue  # 連字號前後不會有空格
                    lp = col[c]
                    if c == last:
                        add(prefix, NEG, pnb + lp, state, emits)  # 重複：合併
                        if pb > NEG:
                            add(prefix + (c,), NEG, pb + lp, self._extend(state, self.l2c[c]), emits + (math.exp(lp),))
                    else:
                        add(prefix + (c,), NEG, total + lp, self._extend(state, self.l2c[c]), emits + (math.exp(lp),))
            ranked = sorted(nxt.items(), key=lambda kv: -(np.logaddexp(kv[1][0], kv[1][1]) + kv[1][2][3]))
            beam = dict(ranked[:self.beam])
        best, best_score = None, NEG
        for prefix, (pb, pnb, state, emits) in beam.items():
            st = self._close(state)
            s = np.logaddexp(pb, pnb) + st[3]
            if s > best_score:
                best, best_score = (prefix, emits), s
        return list(best[0]), list(best[1])


def line_decoder(net, exclude=None, **kw):
    """回傳 decode(probs) → (文字, 平均信心, 最低信心) 的函式，供 recognize.py 使用。"""
    vocab = valid_syllables()
    lm = build_lm(vocab, exclude=exclude)
    l2c = {lab[0]: ch for lab, ch in net.codec.l2c.items()}
    dec = Decoder(l2c, Trie.build(vocab), lm, **kw)

    def run(probs):
        labels, confs = dec.decode(probs)
        text = nfc("".join(l2c[x] for x in labels))
        return text, (round(sum(confs) / len(confs), 4) if confs else 0.0), (round(min(confs), 4) if confs else 0.0)
    return run


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-m", "--model", required=True)
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--labels", help="圖檔 → 標籤的 JSON；不給則讀 .gt.txt")
    ap.add_argument("--beam", type=int, default=8)
    ap.add_argument("--topk", type=int, default=6)
    ap.add_argument("--lm-weight", type=float, nargs="*", default=[0.0, 0.3, 0.6, 1.0])
    ap.add_argument("--oov-penalty", type=float, nargs="*", default=[6.0])
    ap.add_argument("--limit", type=int)
    ap.add_argument("--discount", type=float, nargs="*", default=[0.75])
    ap.add_argument("--incomplete-penalty", type=float, default=3.0)
    ap.add_argument("--lm-all", action="store_true", help="bigram 連測試頁的經文一起估（預設排除，以免看過答案）")
    ap.add_argument("--show-diffs", type=int, default=0, help="列出前 N 行 beam 與貪婪解碼不同的例子")
    ap.add_argument("--bonus-scale", type=float, nargs="*", default=[1.0], help="插入獎勵 = scale × lm_weight × 平均音節成本")
    args = ap.parse_args()
    from PIL import Image
    from kraken.lib import models
    from kraken.lib.ctc_decoder import greedy_decoder
    from kraken.lib.dataset import ImageInputTransforms
    net = models.load_any(args.model, device="cuda:0")
    batch, channels, height, width = net.nn.input
    ts = ImageInputTransforms(batch, height, width, channels, (16, 0), True)
    paths = [l.strip() for l in open(args.manifest, encoding="utf-8") if l.strip()][:args.limit]
    labels = json.load(open(args.labels, encoding="utf-8")) if args.labels else None
    gts, mats = [], []
    for p in paths:
        gt = labels[p] if labels else Path(p).with_suffix(".gt.txt").read_text(encoding="utf-8")
        gts.append(gt.strip())
        o, _ = net.forward(ts(Image.open(p)).unsqueeze(0))
        mats.append(np.asarray(o)[0])
    l2c = {lab[0]: ch for lab, ch in net.codec.l2c.items()}
    greedy = [nfc("".join(x[0] for x in net.codec.decode(greedy_decoder(m)))) for m in mats]
    full, b = cer(list(zip(greedy, gts)))
    print(f"greedy            lines={len(gts)} CER_full={full:.4f} CER_base={b:.4f} exact={sum(nfd(p) == nfd(g) for p, g in zip(greedy, gts)) / len(gts):.3f}")
    vocab = valid_syllables()
    exclude = None if args.lm_all else verses_on_pages({Path(p).parent.name for p in paths})
    if exclude:
        print("bigram excludes", {e: len(v) for e, v in exclude.items()})
    trie = Trie.build(vocab)
    import time
    for disc in args.discount:
        lm = build_lm(vocab, exclude=exclude, discount=disc)
        print(f"lm mean cost per syllable {lm.mean_cost:.2f} nats")
        for oov in args.oov_penalty:
          for bs in args.bonus_scale:
            for w in args.lm_weight:
                dec = Decoder(l2c, trie, lm, beam=args.beam, topk=args.topk, lm_weight=w, oov_penalty=oov,
                              incomplete_penalty=args.incomplete_penalty, syllable_bonus=bs * w * lm.mean_cost)
                t0 = time.time()
                preds = [nfc("".join(l2c[x] for x in dec.decode(m)[0])) for m in mats]
                dt = (time.time() - t0) / len(mats)
                full, b = cer(list(zip(preds, gts)))
                ex = sum(nfd(p) == nfd(g) for p, g in zip(preds, gts)) / len(gts)
                print(f"beam={args.beam} disc={disc} oov={oov} inc={args.incomplete_penalty} bonus×{bs} lm={w:<4} "
                      f"CER_full={full:.4f} CER_base={b:.4f} exact={ex:.3f}  ({dt * 1000:.0f} ms/line)")
                shown = 0
                for p_, g_, gr in zip(preds, gts, greedy):
                    if shown >= args.show_diffs:
                        break
                    if nfd(p_) != nfd(gr):
                        tag = "beam✓" if nfd(p_) == nfd(g_) else ("greedy✓" if nfd(gr) == nfd(g_) else "both✗")
                        print(f"   [{tag}] GT: {g_}\n          greedy: {gr}\n          beam:   {p_}")
                        shown += 1


if __name__ == "__main__":
    main()
