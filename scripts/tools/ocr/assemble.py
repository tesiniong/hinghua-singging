#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把逐頁辨識結果組回經節，填入 rom.txt 的空節號，並產生校對報告。

  assemble.py --book Genesis --chapters 21-37            # 只寫候選 JSON 與報告
  assemble.py --book Genesis --chapters 21-37 --write    # 同時填入 data/rom.txt（只填空節）

前置：recognize.py 已產生相關頁面的 WORK/recognized/<page>.json。
"""

import argparse
import collections
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (BOOKS, DATA, WORK, base, clusters, load_page_map, load_rom_verses, nfc,  # noqa: E402
                    prev_verse, verses_on_page)

NOISE_RE = re.compile(r"^[\d\s:.;,'\"()\-]*$")  # 只有數字與標點：頁眉章節號、頁碼
# 章標題「Dā̤ 11 Ca̤uⁿ.」的去符號形式；粗體數字常被漏讀，所以數字可缺，但沒數字時要有句點
CHAPTER_RE = re.compile(r"(?<![a-z])d{1,2}a\s*(\d*)(?:\s*[^\sa-z]{1,3}|\s+[a-z]{1,2})?\s*ca[a-z]*\.?")
CHAPTER_SHORT_RE = re.compile(r"^[^a-z]{0,3}d?a\s*(\d*)\s*ca[a-z]*\.?[^a-z]{0,3}$")  # 整行只有章標題，首字母也可缺
HEADER_RE = re.compile(r"\d+\s*:\s*\d*")  # 頁眉的「章: 節」
NUM_RE = re.compile(r"^(\d{1,3})[.,;:]?$")
GLUED_RE = re.compile(r"^(\d{1,3})([^\W\d].*)$")  # 節號黏在下一個詞前面，如「4Gah」


def digit_lev(a, b):
    """兩個數字字串的編輯距離（節號誤讀判定用）。"""
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def is_noise(t, band=False):
    """頁眉（章節號、大寫書名）、頁碼與其他非經文的行。band=True 表示位於頁面最上或最下緣。"""
    s = t.strip()
    if not s or NOISE_RE.match(s):
        return True
    letters = [c for c in s if c.isalpha()]
    upper = sum(c.isupper() for c in letters) / len(letters) if letters else 0
    if band:
        return len(s) <= 6 or (len(letters) >= 2 and upper >= 0.5) or bool(HEADER_RE.search(s))
    return len(letters) >= 3 and upper > 0.6


def split_heading(t):
    """若行內含章標題，回傳 (章號或 None, 標題前的文字, 標題後的文字)；否則 None。"""
    cl, pb = clusters(t)
    low = pb.lower()
    m = CHAPTER_RE.search(low)
    if m and (m.group(1) or m.group(0).endswith(".")):
        ch = int(m.group(1)) if m.group(1) else None
        return ch, nfc("".join(cl[:m.start()])).strip(), nfc("".join(cl[m.end():])).strip()
    m = CHAPTER_SHORT_RE.match(low.strip()) if len(low.strip()) <= 22 else None
    if m:
        return (int(m.group(1)) if m.group(1) else None), "", ""
    return None


def syllables(text):
    """切出音節（以空格與連字號分隔），去掉標點與數字。組合符號（U+0300–036F）要視為字母的一部分。"""
    cleaned = re.sub(r"[^\w\s\-\u0300-\u036f]", " ", text)
    return [s for s in re.split(r"[\s\-]+", cleaned) if s and not s.isdigit()]


def expected_markers(eng, start, next_start):
    """本頁應出現的標記，依序：章標題（第 1 節不印節號）或節號。start 是本頁第一個節號。"""
    vpc = BOOKS[eng]["verses_per_chapter"]
    items = []
    c, v = start
    while (c, v) < next_start and c <= len(vpc):
        items.append(("head", c, 1) if v == 1 else ("num", c, v))
        v += 1
        if v > vpc[c - 1]:
            c, v = c + 1, 1
    return items


def observe_page(rec):
    """把一頁的辨識結果轉成觀察序列：數字、章標題、文字 token（含是否要黏在前一個 token 後）。"""
    obs = []
    carry = False
    ys = [ln["y"] for ln in rec["lines"]] or [0]
    top, bottom = min(ys) + 0.06 * (max(ys) - min(ys)), max(ys) - 0.03 * (max(ys) - min(ys))

    line_no = -1

    def tokens(t, conf):
        nonlocal carry
        toks = t.split()
        for k, tok in enumerate(toks):
            btok = base(tok)  # 上標數字偶爾黏到雜散的組合符號
            m = NUM_RE.match(btok)
            g = None if m else GLUED_RE.match(tok)
            if m or g:
                obs.append({"kind": "num", "value": int((m or g).group(1)), "conf": conf, "line": line_no})
                if g:
                    obs.append({"kind": "text", "value": g.group(2), "conf": conf, "glue": False, "line": line_no})
                carry = False
                continue
            obs.append({"kind": "text", "value": tok, "conf": conf, "glue": k == 0 and carry, "line": line_no})
            carry = False
        if toks:
            carry = toks[-1].endswith("-") and not NUM_RE.match(base(toks[-1]))

    for line_no, ln in enumerate(rec["lines"]):
        t = ln["text"].strip()
        if (ln.get("header") or ln.get("footer")) and not split_heading(t) \
                and (is_noise(t, True) or len(syllables(t)) <= 4):
            continue  # 頁眉、頁碼（位置像，內容也像）
        if is_noise(t, ln["y"] < top or ln["y"] > bottom):
            continue
        heading = split_heading(t)
        if heading:
            ch, before, after = heading
            if before:
                tokens(before, ln["conf"])
            obs.append({"kind": "head", "value": ch, "conf": ln["conf"], "line": line_no})
            carry = False
            if after:
                tokens(after, ln["conf"])
            continue
        tokens(t, ln["conf"])
    return obs


def align_markers(expected, observed, seg_len, want_len, window=5):
    """預期標記與觀察到的標記做序列對齊，同時要求切出來的每節長度符合預期音節數。

    seg_len[j]：第 j 個觀察標記到下一個標記之間的音節數（seg_len[m] 是最後一個標記之後）。
    want_len(i)：預期第 i 節的音節數（漢字版字數），未知時回傳 None。
    回傳 observed 索引 → expected 索引（或 None）。
    """
    def sub(e, o):
        if e[0] == "head" and o["kind"] == "head":
            return 0.0 if o["value"] in (None, e[1]) else 0.3
        if e[0] == "num" and o["kind"] == "num":
            if o["value"] == e[2]:
                return 0.0 if o.get("cap") else 0.3
            d = digit_lev(str(o["value"]), str(e[2]))
            if d <= 1:
                return 0.5 if o.get("cap") else 1.0  # 節號後多半接大寫字母；接小寫的數字較可疑
            if d == 2:
                return 2.0 if o.get("cap") else 2.5  # 磨損頁的單位數節號幾乎隨機，靠長度線索裁決
            return 4.0
        return 6.0

    def ins(o):  # 觀察到的數字是雜訊
        return 1.0 if o.get("cap") else 0.4

    def length_cost(i0, i1, j0, j1):
        """預期第 i0..i1-1 節合併起來，對應觀察標記 j0..j1-1 之間的文字。"""
        got = sum(seg_len[j0:j1])
        want = [want_len(i) for i in range(i0, i1)]
        if any(w is None for w in want):
            return 1.0 if got < 3 else 0.0
        w = sum(want)
        return 3.0 * max(0, abs(got - w) - 2 - 0.1 * w) / max(w, 8)

    DEL = 1.2  # 預期的節號沒被讀出
    n, m = len(expected), len(observed)
    INF = float("inf")
    best = [[INF] * m for _ in range(n)]
    back = [[None] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            c = sub(expected[i], observed[j])
            if c >= 5:
                continue
            # 前面全部沒配上
            v = c + DEL * i + sum(ins(o) for o in observed[:j])
            arg = None
            for i0 in range(max(0, i - window), i):
                for j0 in range(max(0, j - window), j):
                    if best[i0][j0] == INF:
                        continue
                    cand = best[i0][j0] + c + DEL * (i - i0 - 1) + sum(ins(o) for o in observed[j0 + 1:j]) \
                        + length_cost(i0, i, j0, j)
                    if cand < v:
                        v, arg = cand, (i0, j0)
            best[i][j], back[i][j] = v, arg
    # 結尾：最後一個配對之後的都不配（頁末經文通常跨頁，不算長度）
    end_v, end = DEL * n + sum(ins(o) for o in observed), None
    for i in range(n):
        for j in range(m):
            if best[i][j] < INF:
                v = best[i][j] + DEL * (n - 1 - i) + sum(ins(o) for o in observed[j + 1:])
                if v < end_v:
                    end_v, end = v, (i, j)
    match = [None] * m
    while end is not None:
        i, j = end
        match[j] = i
        end = back[i][j]
    return match


class Assembler:
    def __init__(self, eng, han_len=None):
        self.eng = eng
        self.han_len = han_len or {}  # (章, 節) → 漢字版音節數，切節時當長度線索
        self.pieces = collections.defaultdict(list)
        self.confs = collections.defaultdict(list)
        self.flags = collections.defaultdict(set)
        self.lines = collections.defaultdict(list)  # (章, 節) → [(頁, 行索引), …]，供校對報告裁圖
        self.page = None
        self.last = None  # 上一頁結束時所在的經節

    def add_text(self, key, tok, glue, conf, line=None):
        if line is not None and (self.page, line) not in self.lines[key]:
            self.lines[key].append((self.page, line))
        buf = self.pieces[key]
        if glue and buf:
            buf[-1] += tok
        else:
            buf.append(tok)
        self.confs[key].append(conf)

    def feed_page(self, page, rec, start, next_start):
        self.page = page
        expected = expected_markers(self.eng, start, next_start)
        obs = observe_page(rec)
        for k, o in enumerate(obs):
            if o["kind"] == "num":
                nxt = next((x for x in obs[k + 1:] if x["kind"] != "num"), None)
                o["cap"] = bool(nxt and nxt["kind"] == "text" and nxt["value"][:1].isupper())
        markers = [o for o in obs if o["kind"] != "text"]
        seg_len = [0] * (len(markers) + 1)  # 每個標記到下一個標記之間的音節數；[0] 是第一個標記之前
        k = 0
        for o in obs:
            if o["kind"] == "text":
                seg_len[k] += len(syllables(o["value"]))
            else:
                k += 1

        def want_len(i):
            e = expected[i]
            return self.han_len.get((e[1], e[2])) if self.han_len else None
        match = align_markers(expected, markers, seg_len[1:], want_len)
        by_marker = {id(o): match[k] for k, o in enumerate(markers)}
        # 切成段：每個標記帶著它後面的文字；對不上預期的標記是雜訊，文字併回前一段
        segments = [{"ei": None, "texts": []}]
        for o in obs:
            if o["kind"] == "text":
                segments[-1]["texts"].append(o)
                continue
            ei = by_marker[id(o)]
            if ei is None:
                segments[-1]["junk"] = segments[-1].get("junk", []) + [o]
            else:
                segments.append({"ei": ei, "texts": [], "obs": o})
        first = prev_verse(self.eng, *start) or start  # 頁首通常是前一節的尾巴
        if self.last is not None and self.last != first:
            self.flags[self.last].add(f"頁 {page} 開始時位於 {self.last[0]}:{self.last[1]}，依頁面對應表校正為 {first[0]}:{first[1]}")
            self.flags[first].add(f"頁 {page} 開始時依頁面對應表校正位置，前一頁末尾的切節可能有誤")
        cur = first
        for idx, seg in enumerate(segments):
            if seg["ei"] is None:
                keys = [first]
            else:
                e = expected[seg["ei"]]
                cur = (e[1], e[2])
                o = seg["obs"]
                if e[0] == "head":
                    self.flags[cur].add("首節（首字放大）")
                    if o["value"] not in (None, e[1]):
                        self.flags[cur].add(f"章標題讀作 {o['value']}，依序推定為 {e[1]}")
                elif o["value"] != e[2]:
                    self.flags[cur].add(f"節號讀作 {o['value']}，依序推定為 {e[2]}")
                next_ei = segments[idx + 1]["ei"] if idx + 1 < len(segments) else len(expected)
                keys = [(x[1], x[2]) for x in expected[seg["ei"]:next_ei]]
            for o in seg.get("junk", []):
                self.flags[keys[0]].add(f"文中出現非預期數字 {o['value']}" if o["kind"] == "num" else "出現位置不符的章標題")
            self.place_texts(keys, seg["texts"], idx == 0)
            cur = keys[-1]
        # 頁末：最後一段之後還沒出現的預期標記
        self.last = cur

    def place_texts(self, keys, texts, is_first):
        """把一段文字分給 keys 這幾節。多於一節時表示中間的節號沒讀出來：
        有漢字版字數就照字數切開，否則全部併入第一節。"""
        if len(keys) > 1:
            counts = [self.han_len.get(k) for k in keys[:-1]]
            if all(c is not None for c in counts) and not is_first:
                cut = 0
                ki = 0
                acc = 0
                for o in texts:
                    if ki < len(counts) and acc >= counts[ki]:
                        ki += 1
                        acc = 0
                    self.add_text(keys[ki], o["value"], o["glue"] and acc > 0, o["conf"], o.get("line"))
                    acc += len(syllables(o["value"]))
                for kk in keys[1:]:
                    self.flags[kk].add("節號未辨識出，依漢字版字數切分，請核對切節位置")
                    pk = prev_verse(self.eng, *kk)
                    if pk:
                        self.flags[pk].add("下一節節號未辨識出，依漢字版字數切分")
                return
            for kk in keys[1:]:
                self.flags[kk].add("節號未辨識出，經文可能併入前一節")
                pk = prev_verse(self.eng, *kk)
                if pk:
                    self.flags[pk].add("下一節節號未辨識出，可能含下一節經文")
        for o in texts:
            self.add_text(keys[0], o["value"], o["glue"], o["conf"], o.get("line"))

    def verse_text(self, key):
        parts = list(self.pieces.get(key, []))
        if key[1] == 1 and len(parts) >= 2 and len(parts[0]) == 1 and parts[0].isalpha():
            # 章首放大字母獨立成一塊，其後該音節其餘字母印成大寫：接回並改小寫
            rest = re.sub(r"^[^\W\d_]+", lambda m: m.group(0).lower(), parts[1])
            parts = [parts[0] + rest] + parts[2:]
        s = " ".join(parts)
        s = re.sub(r"\s+([,.;:!?)])", r"\1", s)
        s = re.sub(r"\(\s+", "(", s)
        return nfc(re.sub(r"\s+", " ", s)).strip()


def load_han_verses(eng):
    """han.txt 中該書卷的經文，{(章, 節): 漢字}，用來交叉檢查音節數。"""
    han_name = BOOKS[eng]["han"]
    out, book, ch, key = {}, None, None, None
    for line in open(DATA / "han.txt", encoding="utf-8"):
        if line.startswith("# "):
            book, key = line[2:].strip(), None
        elif line.startswith("## "):
            ch, key = int(line[3:]), None
        elif line.startswith("###") or not line.strip():
            key = None
        else:
            m = re.match(r"^(\d+)\s*(.*)", line)
            if m and book == han_name:
                key = (ch, int(m.group(1)))
                if m.group(2).strip():
                    out[key] = m.group(2).strip()
                else:
                    key = None
            elif key and book == han_name:  # 詩歌體的續行
                out[key] += line.strip()
    return out


def han_syllables(text):
    """漢字版的音節數：每個漢字一音節，「」內的合音字算一音節，{} 專名標記不計。"""
    text = re.sub(r"「[^」]*」", "x", text)
    return sum(1 for c in text if "\u4e00" <= c <= "\u9fff" or c in "々x")


def parse_chapters(spec):
    a, _, b = spec.partition("-")
    return list(range(int(a), int(b or a) + 1))


def pages_for(pm, pages, eng, chapters):
    out = []
    for p in pages:
        e, vs = verses_on_page(pm, pages, p)
        if e == eng and any(c in chapters for c, _ in vs):
            out.append(p)
    return out


def fill_rom(eng, cands, path=DATA / "rom.txt"):
    """把候選經文填進 rom.txt 的空節號行；缺少的章節區塊會補上骨架。回傳填入數。"""
    rom_name = nfc(BOOKS[eng]["rom"])
    lines = open(path, encoding="utf-8").read().split("\n")
    # 找書卷範圍
    starts = [i for i, ln in enumerate(lines) if ln.startswith("# ")]
    b0 = next((i for i in starts if nfc(lines[i][2:].strip()) == rom_name), None)
    if b0 is None:
        raise SystemExit(f"rom.txt 沒有書卷 {rom_name}，請先加上 '# {rom_name}'")
    b1 = next((i for i in starts if i > b0), len(lines))
    # 補缺少的章節骨架
    have = {int(lines[i][3:]) for i in range(b0, b1) if lines[i].startswith("## ")}
    for c in sorted({c for c, _ in cands} - have):
        block = [f"## {c}"] + [str(v) for v in range(1, BOOKS[eng]["verses_per_chapter"][c - 1] + 1)]
        insert_at = b1
        for i in range(b0 + 1, b1):
            if lines[i].startswith("## ") and int(lines[i][3:]) > c:
                insert_at = i
                break
        lines[insert_at:insert_at] = block
        b1 += len(block)
    n = 0
    ch = None
    for i in range(b0, b1):
        ln = lines[i]
        if ln.startswith("## "):
            ch = int(ln[3:])
            continue
        m = re.match(r"^(\d+)\s*$", ln)
        if m and ch is not None and (ch, int(m.group(1))) in cands and cands[(ch, int(m.group(1)))]:
            lines[i] = f"{m.group(1)} {cands[(ch, int(m.group(1)))]}"
            n += 1
    open(path, "w", encoding="utf-8").write("\n".join(lines))
    return n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", required=True, help="英文書名，如 Genesis")
    ap.add_argument("--chapters", required=True, help="如 21-37 或 5")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--evaluate", action="store_true", help="與 rom.txt 已有的經文比對，輸出逐節 CER")
    args = ap.parse_args()
    eng = args.book
    chapters = parse_chapters(args.chapters)
    pm, pages = load_page_map()
    filled = load_rom_verses()
    lexicon = {s.lower() for verses in filled.values() for t in verses.values() for s in syllables(t)}
    plist = pages_for(pm, pages, eng, chapters)
    han = load_han_verses(eng)
    asm = Assembler(eng, {k: han_syllables(v) for k, v in han.items()})
    for p in plist:
        f = WORK / "recognized" / f"{p}.json"
        if not f.exists():
            raise SystemExit(f"缺少 {f}，請先執行 recognize.py --pages {p}")
        rec = json.load(open(f, encoding="utf-8"))
        start = (pm[p]["chapter"], pm[p]["verse"])
        i = pages.index(p)
        nxt = pm[pages[i + 1]] if i + 1 < len(pages) else None
        next_start = (nxt["chapter"], nxt["verse"]) if nxt and nxt["book_english"] == eng else (10**6, 1)
        asm.feed_page(p, rec, start, next_start)
    targets = [(c, v) for c in chapters for v in range(1, BOOKS[eng]["verses_per_chapter"][c - 1] + 1)]
    cands, report = {}, []
    for key in targets:
        text = asm.verse_text(key)
        existing = filled.get(eng, {}).get(key)
        oov = [s for s in syllables(text) if s.lower() not in lexicon]
        if key in han and text:
            d = len(syllables(text)) - han_syllables(han[key])
            if abs(d) > 2:
                asm.flags[key].add(f"音節數與漢字版差 {d:+d}")
        conf = min(asm.confs[key]) if asm.confs[key] else 0.0
        flags = set(asm.flags.get(key, ()))
        if not text:
            flags.add("沒有辨識到經文")
        if oov:
            flags.add("含詞表外音節：" + " ".join(oov))
        if conf and conf < 0.6:
            flags.add(f"低信心 {conf:.2f}")
        if existing:
            flags.add("rom.txt 已有內容，不覆寫")
        else:
            cands[key] = text
        report.append({"chapter": key[0], "verse": key[1], "text": text, "conf_min": round(conf, 3),
                       "oov": oov, "flags": sorted(flags), "existing": existing})
    outdir = WORK / "recognized"
    stem = f"{eng.replace(' ', '_')}_{chapters[0]}-{chapters[-1]}"
    json.dump(report, open(outdir / f"{stem}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    flagged = [r for r in report if r["flags"] and r["flags"] != ["rom.txt 已有內容，不覆寫"]]
    md = [f"# {eng} {chapters[0]}–{chapters[-1]} 校對報告", "",
          f"頁面：{plist[0]}–{plist[-1]}；經節 {len(targets)}，候選 {len(cands)}，需注意 {len(flagged)}", "",
          "| 章:節 | 信心 | 注意事項 | 經文 |", "|---|---|---|---|"]
    for r in flagged:
        md.append(f"| {r['chapter']}:{r['verse']} | {r['conf_min']:.2f} | {'；'.join(r['flags'])} | {r['text']} |")
    (outdir / f"{stem}_report.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"pages {plist[0]}–{plist[-1]} ({len(plist)}), verses {len(targets)}, candidates {len(cands)}, flagged {len(flagged)}")
    print(f"report: {outdir / (stem + '_report.md')}")
    if args.evaluate:
        from common import cer, lev, nfd
        pairs = [(r["text"], r["existing"]) for r in report if r["existing"]]
        full, b = cer(pairs)
        exact = sum(nfd(p).strip() == nfd(g).strip() for p, g in pairs)
        near = sum(lev(nfd(p), nfd(g)) <= 2 for p, g in pairs)
        print(f"evaluate: verses with ground truth={len(pairs)} CER_full={full:.4f} CER_base={b:.4f} "
              f"exact={exact} ({exact / len(pairs):.2f}) within_2_edits={near} ({near / len(pairs):.2f})")
        worst = sorted(((lev(nfd(p), nfd(g)) / max(1, len(nfd(g))), r) for r, (p, g) in
                        zip([r for r in report if r["existing"]], pairs)), key=lambda x: -x[0])[:8]
        for d, r in worst:
            print(f"  {r['chapter']}:{r['verse']} ned={d:.2f} | OCR: {r['text'][:70]} | GT: {r['existing'][:70]}")
    if args.write:
        n = fill_rom(eng, cands)
        print(f"filled {n} verses into {DATA / 'rom.txt'}")


if __name__ == "__main__":
    main()
