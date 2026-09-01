/**
 * 興化平話字的共用轉換工具。
 *
 * 「平話字」指帶調符的正式寫法（Siō̤ng-Da̤̍）；
 * 「輸入式」指可用一般鍵盤打出的等價寫法（sioong5-daa4）：
 *   a̤ -> aa   e̤ -> ee   o̤ -> oo   ṳ -> y   ⁿ -> nn   聲調 -> 尾端數字 1-7
 *
 * bucToInput 與 normalizeInput 原本寫在 RomToHanConverter.jsx 內，
 * 搜尋功能也需要同一套邏輯，因此抽出共用。
 */

// 簡化版平話字轉輸入式（前端版本）
export function bucToInput(syllable) {
  // 移除星號
  const clean = syllable.replace(/\*$/, '').trim().toLowerCase();

  // 特殊字符映射
  const charMap = {
    'a̤': 'aa',
    'e̤': 'ee',
    'o̤': 'oo',
    'ṳ': 'y',
    'ⁿ': 'nn'
  };

  // NFD 分解以識別調符
  let result = clean.normalize('NFD');

  // 提取調號
  const toneMarks = {
    '\u0301': '2',  // acute
    '\u0302': '3',  // circumflex
    '\u030D': '4',  // vertical line
    '\u0304': '5',  // macron
  };

  let tone = '1';  // 預設陰平

  for (const [mark, toneNum] of Object.entries(toneMarks)) {
    if (result.includes(mark)) {
      tone = toneNum;
      result = result.replace(mark, '');
      break;
    }
  }

  // NFC 正規化
  result = result.normalize('NFC');

  // 替換特殊字符（按長度排序）
  for (const [buc, input] of Object.entries(charMap).sort((a, b) => b[0].length - a[0].length)) {
    result = result.split(buc).join(input);
  }

  // 判斷入聲調號
  if (result.endsWith('h')) {
    if (tone === '4') {
      tone = '7';
    } else if (tone === '1') {
      tone = '6';
    } else if (tone === '5') {
      tone = '6';
    }
  }

  return result + tone;
}

// 將混合輸入轉為輸入式，並處理標點符號
export function normalizeInput(text) {
  // 半形到全形標點映射
  const punctMap = {
    ',': '，',
    '.': '。',
    '!': '！',
    '?': '？',
    ';': '；',
    ':': '：',
    '(': '（',
    ')': '）',
    '[': '「',
    ']': '」',
    '{': '『',
    '}': '』',
    '"': '「',
    "'": '\u2019',  // 右單引號 '
    '<': '《',
    '>': '》'
  };

  // 分割：保留空格、連字號、中英文標點符號
  const tokens = text.split(/(\s+|-+|[，。！？；：、（）「」『』《》,.!?;:()[\]{}"'<>])/);

  return tokens.map(token => {
    // 空字符串，跳過
    if (!token) {
      return '';
    }

    // 保留空格和連字號
    if (/^[\s-]+$/.test(token)) {
      return token;
    }

    // 半形標點轉全形
    if (punctMap[token]) {
      return punctMap[token];
    }

    // 全形標點保留
    if (/^[，。！？；：、（）「」『』《》]+$/.test(token)) {
      return token;
    }

    // 檢查是否為羅馬字音節（含平話字特殊字符、調符，或輸入式數字調號）
    // NFD 分解後檢查，以支援預組合字元（如 ē）和組合字元（e + ̄）
    const tokenNFD = token.normalize('NFD');

    // 只要包含字母，就嘗試轉換（即使有數字，因為可能是輸入式如 gaa1）
    if (/[a-z\u0324\u0304\u0306\u0302\u0303\u030D\u207F\u1E73]/i.test(tokenNFD)) {
      try {
        // 如果已經是輸入式（末尾有數字 1-7），直接返回
        if (/^[a-z]+[1-7]$/i.test(token)) {
          return token.toLowerCase();
        }
        return bucToInput(token);
      } catch {
        return token;  // 轉換失敗，保留原文
      }
    }

    // 其他（純數字、漢字等），保留原文
    return token;
  }).join('');
}

// ---------------------------------------------------------------------------
// 搜尋用的折疊 (folding)
// ---------------------------------------------------------------------------

// 一個音節：拉丁字母 + 組合變音符號 + 可能的輸入式聲調數字
const SYLLABLE_RE = /[A-Za-z\u00C0-\u024F\u0300-\u036F\u1E00-\u1EFF\u207F]+[1-7]?/g;

/** 單一音節轉輸入式；已經是輸入式就原樣小寫。 */
function syllableToInput(token) {
  if (/^[a-z]+[1-7]$/i.test(token)) return token.toLowerCase();
  try {
    return bucToInput(token);
  } catch {
    return token.toLowerCase();
  }
}

/**
 * 進一步抹除聲調與變韻的區別，讓沒學過輸入式的人也搜得到：
 * sioong5 -> siong，使 siong / sioong / Siō̤ng 都能互相命中。
 */
function looseFold(input) {
  return input
    .replace(/[1-7]$/, '')
    .replace(/aa/g, 'a')
    .replace(/ee/g, 'e')
    .replace(/oo/g, 'o')
    .replace(/nn/g, 'n')
    .replace(/y/g, 'u');
}

/**
 * 把一段羅馬字折疊成可比對的形式，並保留回原文的位置對應。
 *
 * 音節之間一律以單一空格相接，因此連字號與空格的差異會被吸收
 * （Siō̤ng-Da̤̍ 與 Siō̤ng Da̤̍ 折疊結果相同），同時避免跨音節的假命中。
 *
 * @returns {{ exact: string, loose: string, syllables: Array }}
 *   syllables 每筆記錄該音節在兩種折疊字串與原文中的起訖位置。
 */
export function foldRomanized(text) {
  const syllables = [];
  let exact = '';
  let loose = '';
  if (!text) return { exact, loose, syllables };

  SYLLABLE_RE.lastIndex = 0;
  let m;
  while ((m = SYLLABLE_RE.exec(text)) !== null) {
    const asInput = syllableToInput(m[0]);
    if (!asInput) continue;
    const asLoose = looseFold(asInput);

    if (exact) {
      exact += ' ';
      loose += ' ';
    }
    syllables.push({
      exactStart: exact.length,
      exactEnd: exact.length + asInput.length,
      looseStart: loose.length,
      looseEnd: loose.length + asLoose.length,
      origStart: m.index,
      origEnd: m.index + m[0].length,
    });
    exact += asInput;
    loose += asLoose;
  }
  return { exact, loose, syllables };
}

/**
 * 在折疊後的字串中找出命中位置，再換算回原文的起訖位置。
 * 回傳整個音節的範圍——羅馬字若只標一半音節，調符會被切開而難以辨讀。
 *
 * @returns {{ start: number, end: number } | null}
 */
export function findRomanizedMatch(folded, query, fuzzy) {
  const haystack = fuzzy ? folded.loose : folded.exact;
  if (!query || !haystack) return null;
  const at = haystack.indexOf(query);
  if (at === -1) return null;

  const until = at + query.length;
  const hit = folded.syllables.filter((s) => {
    const [start, end] = fuzzy ? [s.looseStart, s.looseEnd] : [s.exactStart, s.exactEnd];
    return start < until && end > at;
  });
  if (hit.length === 0) return null;
  return { start: hit[0].origStart, end: hit[hit.length - 1].origEnd };
}
