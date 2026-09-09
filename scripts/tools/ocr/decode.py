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
                            add(prefix + (c,), NEG, pb + lp, self._extend(state, self.l2c[c]), emits + ((math.exp(lp), t),))
                    else:
                        add(prefix + (c,), NEG, total + lp, self._extend(state, self.l2c[c]), emits + ((math.exp(lp), t),))
            ranked = sorted(nxt.items(), key=lambda kv: -(np.logaddexp(kv[1][0], kv[1][1]) + kv[1][2][3]))
            beam = dict(ranked[:self.beam])
        best, best_score = None, NEG
        for prefix, (pb, pnb, state, emits) in beam.items():
            st = self._close(state)
            s = np.logaddexp(pb, pnb) + st[3]
            if s > best_score:
                best, best_score = (prefix, emits), s
        return list(best[0]), [p for p, _ in best[1]], [t for _, t in best[1]]


def ctc_logp(logp, labels, t0, t1, blank=0):
    """CTC 前向演算法：第 t0..t1-1 格產生 labels 的 log 機率（含空白與重複的所有路徑）。"""
    if t1 - t0 < len(labels) or not labels:
        return -1e9
    ext = [blank]
    for lab in labels:
        ext += [lab, blank]
    ext = np.array(ext)
    S = len(ext)
    NEG = -1e30
    skip = np.zeros(S, bool)  # 可以跳過中間空白直接接到 s-2：ext[s] 不是空白且與 ext[s-2] 不同
    skip[2:] = (ext[2:] != blank) & (ext[2:] != ext[:-2])
    alpha = np.full(S, NEG)
    alpha[0] = logp[blank, t0]
    alpha[1] = logp[ext[1], t0]
    for t in range(t0 + 1, t1):
        a1 = np.concatenate(([NEG], alpha[:-1]))
        a2 = np.concatenate(([NEG, NEG], alpha[:-2]))
        new = np.logaddexp(alpha, a1)
        new = np.where(skip, np.logaddexp(new, a2), new)
        alpha = new + logp[ext, t]
    return float(np.logaddexp(alpha[-1], alpha[-2]))


DIGIT_PRIOR_OUT = -3.0  # 不在該頁預期集合裡的數字：先驗扣 3 nats（要有明顯的影像證據才保留）
SEQ_BONUS, SEQ_AHEAD = 4.0, 3  # 頁內依閱讀順序解碼：接在上一個節號後面 1..SEQ_AHEAD 的數字加分
# SEQ_BONUS 在測試集上 1.5→89.9%、4→92.3%、6→92.9% 的節號正確率；取 4 是因為再大只換到 0.6 個百分點，
# 而偏置越強、原書真的跳號（節號漏印、經文併節）時越可能被硬掰成連號


def rescore_numbers(logp, chars, expected, c2l, prior_out=DIGIT_PRIOR_OUT, pad=6, context=None):
    """把一行裡每段數字換成該頁預期節號中最可能的：在數字所占的時段（前後鄰字的發射格之間）
    對每個候選算 CTC 機率，加上先驗。回傳 (新字元序列, [每段的 {raw, best, alts, conf}])。
    chars：[(字元, 機率, 發射格), …]。expected：該頁預期的整數集合；空集合則不動。
    context：同一頁逐行共用的 {"last": 上一個節號}，有給就對接續的節號加 SEQ_BONUS。"""
    if not expected:
        return chars, []
    W = logp.shape[1]
    cands = sorted({str(n) for n in expected if 0 < n < 1000 and all(d in c2l for d in str(n))})
    out, nums, i = [], [], 0
    bound_col = logp.max(axis=0)  # 每格最大值：任何序列機率的上界，用來估絕對信心
    while i < len(chars):
        if not chars[i][0].isdigit():
            out.append(chars[i])
            i += 1
            continue
        j = i
        while j + 1 < len(chars) and chars[j + 1][0].isdigit():
            j += 1
        raw = "".join(ch for ch, _, _ in chars[i:j + 1])
        t0 = chars[i - 1][2] + 1 if i > 0 else max(0, chars[i][2] - pad)
        t1 = chars[j + 1][2] if j + 1 < len(chars) else min(W, chars[j][2] + pad + 1)
        if t1 <= t0:
            t0, t1 = max(0, chars[i][2] - 1), min(W, chars[j][2] + 2)
        scores = {}
        last = context.get("last") if context else None
        for cand in ([raw] if raw not in cands else []) + cands:
            lp = ctc_logp(logp, [c2l[d] for d in cand], t0, t1)
            bonus = SEQ_BONUS if last is not None and last < int(cand) <= last + SEQ_AHEAD else 0.0
            scores[cand] = lp + (bonus if cand in cands else prior_out)
        best = max(scores, key=scores.get)
        if context is not None and best in cands:
            context["last"] = int(best)
        z = np.logaddexp.reduce(list(scores.values()))
        alts = {c: round(float(v - z), 2) for c, v in scores.items() if v - z > -8.0}
        conf = round(float(scores[best] - (0.0 if best in cands else prior_out) - bound_col[t0:t1].sum()), 2)
        nums.append({"raw": raw, "best": best, "alts": dict(sorted(alts.items(), key=lambda kv: -kv[1])), "conf": conf})
        mean_p = sum(p for _, p, _ in chars[i:j + 1]) / (j - i + 1)
        out.extend((d, mean_p, chars[i][2]) for d in best)
        i = j + 1
    return out, nums


def line_decoder(net, exclude=None, **kw):
    """回傳 decode(probs, expected=None) → (文字, 平均信心, 最低信心, 數字候選) 的函式，供 recognize.py 使用。
    expected 是該頁預期的節號集合（common.page_numbers）；給了就把數字往這些值重評分。"""
    vocab = valid_syllables()
    lm = build_lm(vocab, exclude=exclude)
    l2c = {lab[0]: ch for lab, ch in net.codec.l2c.items()}
    c2l = {ch: lab for lab, ch in l2c.items()}
    dec = Decoder(l2c, Trie.build(vocab), lm, **kw)

    def run(probs, expected=None, context=None):
        labels, confs, frames = dec.decode(probs)
        chars = [(l2c[x], p, t) for x, p, t in zip(labels, confs, frames)]
        nums = []
        if expected:
            chars, nums = rescore_numbers(np.log(np.maximum(probs, 1e-12)), chars, expected, c2l, context=context)
        confs = [p for _, p, _ in chars]
        text = nfc("".join(ch for ch, _, _ in chars))
        return text, (round(sum(confs) / len(confs), 4) if confs else 0.0), (round(min(confs), 4) if confs else 0.0), nums
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
    ap.add_argument("--digits", action="store_true", help="另算數字（節號）序列的正確率：貪婪／beam／beam＋頁面節號重評分")
    ap.add_argument("--digit-prior", type=float, default=DIGIT_PRIOR_OUT, help="重評分時集合外數字的先驗（log）")
    ap.add_argument("--seq-bonus", type=float, help="頁內接續節號的加分（預設 SEQ_BONUS）")
    args = ap.parse_args()
    if args.seq_bonus is not None:
        global SEQ_BONUS
        SEQ_BONUS = args.seq_bonus
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
                decoded = [dec.decode(m) for m in mats]
                preds = [nfc("".join(l2c[x] for x in d[0])) for d in decoded]
                dt = (time.time() - t0) / len(mats)
                full, b = cer(list(zip(preds, gts)))
                ex = sum(nfd(p) == nfd(g) for p, g in zip(preds, gts)) / len(gts)
                print(f"beam={args.beam} disc={disc} oov={oov} inc={args.incomplete_penalty} bonus×{bs} lm={w:<4} "
                      f"CER_full={full:.4f} CER_base={b:.4f} exact={ex:.3f}  ({dt * 1000:.0f} ms/line)")
                if args.digits:
                    from common import load_page_map, page_numbers
                    pm, pages = load_page_map()
                    c2l = {ch: lab for lab, ch in l2c.items()}
                    digs = lambda s: re.findall(r"\d+", s)  # noqa: E731
                    n = ok_g = ok_b = ok_r = ok_s = 0
                    resc, seq = [], []
                    ctx, cur_page = None, None
                    for path, m, d in zip(paths, mats, decoded):
                        page = Path(path).parent.name
                        if page != cur_page:
                            cur_page, ctx = page, {}
                        chars = [(l2c[x], p, t) for x, p, t in zip(*d)]
                        exp = page_numbers(pm, pages, page)
                        lp_ = np.log(np.maximum(m, 1e-12))
                        c1, _ = rescore_numbers(lp_, list(chars), exp, c2l, prior_out=args.digit_prior)
                        c2, _ = rescore_numbers(lp_, list(chars), exp, c2l, prior_out=args.digit_prior, context=ctx)
                        resc.append(nfc("".join(ch for ch, _, _ in c1)))
                        seq.append(nfc("".join(ch for ch, _, _ in c2)))
                    for g_, gr, p_, r_, s_ in zip(gts, greedy, preds, resc, seq):
                        if not digs(g_):
                            continue
                        n += 1
                        ok_g += digs(gr) == digs(g_)
                        ok_b += digs(p_) == digs(g_)
                        ok_r += digs(r_) == digs(g_)
                        ok_s += digs(s_) == digs(g_)
                    fullr, br = cer(list(zip(resc, gts)))
                    fulls, _ = cer(list(zip(seq, gts)))
                    print(f"   digits: lines with numbers={n} exact greedy={ok_g / n:.3f} beam={ok_b / n:.3f} "
                          f"beam+rescore={ok_r / n:.3f} (CER {fullr:.4f}) +sequence={ok_s / n:.3f} (CER {fulls:.4f})")
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
