import React, { useState, useEffect, useRef } from 'react';
import './RomToHanConverter.css';

// 簡化版平話字轉輸入式（前端版本）
function bucToInput(syllable) {
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
function normalizeInput(text) {
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
  const tokens = text.split(/(\s+|-+|[，。！？；：、（）「」『』《》,.\!?;:\(\)\[\]\{\}"'<>])/);

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
    if (/[a-z̤̄̆̂̃̍ⁿṳ]/i.test(tokenNFD)) {
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

const RomToHanConverter = () => {
  const [inputRom, setInputRom] = useState('');
  const [dict, setDict] = useState(null);
  const [convertedTokens, setConvertedTokens] = useState([]);
  const [selectedIndex, setSelectedIndex] = useState(null);
  const [selectedCharIndex, setSelectedCharIndex] = useState(null);  // 點擊多字詞的哪個字
  const [candidatePos, setCandidatePos] = useState({ x: 0, y: 0 });
  const outputRef = useRef(null);
  const candidateRef = useRef(null);

  // 載入字典
  useEffect(() => {
    fetch(`${import.meta.env.BASE_URL}romToHanDict.json`)
      .then(res => res.json())
      .then(data => {
        console.log('字典載入成功:', Object.keys(data.syllables).length, '個音節');
        setDict(data);
      })
      .catch(err => console.error('載入字典失敗:', err));
  }, []);

  // 點擊外部關閉候選字選單
  useEffect(() => {
    const handleClickOutside = (e) => {
      if (candidateRef.current && !candidateRef.current.contains(e.target)) {
        setSelectedIndex(null);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // 轉換函數（貪婪匹配詞組）
  const convertRomToHan = (romText) => {
    if (!dict) return [];

    // 正規化輸入
    const normalized = normalizeInput(romText);

    // 分詞：按空格和標點符號分割（包含所有全形標點）
    const segments = normalized.split(/([，。！？；：、（）「」『』《》''"\s]+)/);

    const result = [];

    for (const segment of segments) {
      // 保留標點和空格
      if (/^[，。！？；：、（）「」『』《》''"\s]+$/.test(segment)) {
        result.push({
          type: 'punct',
          rom: segment,
          han: segment,
          candidates: []
        });
        continue;
      }

      // 保留非羅馬字（漢字、數字、外語等）
      if (!/^[a-z0-9-]+$/i.test(segment)) {
        result.push({
          type: 'text',
          rom: segment,
          han: segment,
          candidates: []
        });
        continue;
      }

      // 將連字號分隔的音節轉為陣列
      const syllables = segment.toLowerCase().split('-').filter(s => s);

      let i = 0;
      while (i < syllables.length) {
        let matched = false;

        // 貪婪匹配：從最長的詞組開始
        for (let len = Math.min(6, syllables.length - i); len > 1; len--) {
          const phrase = syllables.slice(i, i + len).join('-');

          if (dict.phrases[phrase]) {
            const candidates = dict.phrases[phrase];
            const han = candidates[0].han;

            // 記錄每個字對應的音節（用於候選字選單）
            const syllableList = syllables.slice(i, i + len);
            const charToSyllable = [];

            // 簡單對應：假設字數等於音節數
            if (han.length === len) {
              for (let j = 0; j < han.length; j++) {
                charToSyllable.push(syllableList[j]);
              }
            } else {
              // 字數與音節數不匹配，給每個字分配第一個音節
              for (let j = 0; j < han.length; j++) {
                charToSyllable.push(syllableList[0]);
              }
            }

            result.push({
              type: 'phrase',
              rom: phrase,
              han: han,
              candidates: candidates,
              charToSyllable: charToSyllable  // 每個字對應的音節
            });
            i += len;
            matched = true;
            break;
          }
        }

        // 沒有匹配到詞組，查單音節
        if (!matched) {
          const syl = syllables[i];

          if (dict.syllables[syl]) {
            const candidates = dict.syllables[syl];
            result.push({
              type: 'syllable',
              rom: syl,
              han: candidates[0].han,
              candidates: candidates
            });
          } else {
            // 未知音節，顯示 ▣
            result.push({
              type: 'unknown',
              rom: syl,
              han: '▣',
              candidates: []
            });
          }

          i++;
        }
      }
    }

    return result;
  };

  // 處理輸入變化
  const handleInputChange = (e) => {
    const text = e.target.value;
    setInputRom(text);

    if (text.trim()) {
      const tokens = convertRomToHan(text);
      setConvertedTokens(tokens);
    } else {
      setConvertedTokens([]);
    }
  };

  // 顯示候選字選單
  const showCandidates = (index, charIndex, e) => {
    const token = convertedTokens[index];

    // 計算位置
    const rect = e.target.getBoundingClientRect();
    setCandidatePos({
      x: rect.left,
      y: rect.bottom + window.scrollY
    });

    setSelectedIndex(index);
    setSelectedCharIndex(charIndex);
  };

  // 選擇候選字
  const selectCandidate = (index, charIndex, newValue, isFromDict) => {
    const newTokens = [...convertedTokens];
    const token = newTokens[index];

    if (isFromDict) {
      // 選擇的是詞表中的形式，整個替換
      token.han = newValue;
    } else if (charIndex === null) {
      // 選擇的是單字的整個候選詞，替換整個詞
      token.han = newValue;
    } else {
      // 選擇的是單字候選，只替換那個字
      const chars = Array.from(token.han);
      chars[charIndex] = newValue;
      token.han = chars.join('');
    }

    setConvertedTokens(newTokens);
    setSelectedIndex(null);
    setSelectedCharIndex(null);
  };

  // 複製到剪貼簿
  const copyToClipboard = () => {
    const hanText = convertedTokens.map(t => t.han).join('').replace(/\s+/g, '');

    navigator.clipboard.writeText(hanText).then(() => {
      alert('已複製到剪貼簿！');
    }).catch(err => {
      console.error('複製失敗:', err);
      alert('複製失敗，請手動選取文字複製');
    });
  };

  // 清空
  const clearAll = () => {
    setInputRom('');
    setConvertedTokens([]);
    setSelectedIndex(null);
  };

  return (
    <div className="rom-to-han-converter">
      <div className="converter-header">
        <h1>羅馬字轉漢字工具</h1>
        {/*<p className="subtitle">Ló̤-má-cī Dṳ̆ng Hāng-ci̍ Dô̤-gṳ</p>*/}
        <p className="description">
          輸入興化平話字或輸入式拼音，自動轉換為漢字。點擊漢字可選擇其他候選字。
        </p>
      </div>

      <div className="converter-body">
        <div className="input-section">
          <label htmlFor="rom-input">羅馬字輸入：</label>
          <textarea
            id="rom-input"
            className="rom-input"
            placeholder="例如：Î-ging ū lâ̤u ē seō, î-hā̤u dih-dih ca̍i ū.&#10;或：I3-ging1 u5 laau3 e5 seo5, i3-haau5 dih-dih cai4 u5."
            value={inputRom}
            onChange={handleInputChange}
            rows={6}
          />
          <div className="input-hint">
            （平話字和輸入式可混合輸入）
          </div>
        </div>

        <div className="output-section">
          <div className="output-header">
            <label>漢字輸出：</label>
            <div className="output-actions">
              <button
                className="btn-copy"
                onClick={copyToClipboard}
                disabled={convertedTokens.length === 0}
              >
                📋 複製
              </button>
              <button
                className="btn-clear"
                onClick={clearAll}
                disabled={inputRom.length === 0}
              >
                🗑️ 清空
              </button>
            </div>
          </div>

          <div className="han-output" ref={outputRef}>
            {convertedTokens.length === 0 ? (
              <div className="output-placeholder">漢字將顯示在這裡...</div>
            ) : (
              convertedTokens.map((token, idx) => {
                // 標點符號，不可點擊
                if (token.type === 'punct' || token.type === 'text') {
                  return (
                    <span key={idx} className={`token ${token.type}`}>
                      {token.han}
                    </span>
                  );
                }

                // 多字詞，每個字都可點擊
                if (token.han.length > 1) {
                  return (
                    <span key={idx} className="token phrase">
                      {Array.from(token.han).map((char, charIdx) => (
                        <span
                          key={charIdx}
                          className="char clickable"
                          onClick={(e) => showCandidates(idx, charIdx, e)}
                          title={`點擊選字 (${token.charToSyllable ? token.charToSyllable[charIdx] || token.rom : token.rom})`}
                        >
                          {char}
                        </span>
                      ))}
                    </span>
                  );
                }

                // 單字，整個可點擊
                return (
                  <span
                    key={idx}
                    className={`token ${token.type} clickable`}
                    onClick={(e) => showCandidates(idx, null, e)}
                    title={`點擊選字 (${token.rom})`}
                  >
                    {token.han}
                  </span>
                );
              })
            )}
          </div>
        </div>
      </div>

      {/* 候選字彈出選單 */}
      {selectedIndex !== null && (() => {
        const token = convertedTokens[selectedIndex];
        if (!token) return null;

        let candidatesToShow = [];
        let headerText = '';

        if (selectedCharIndex === null) {
          // 點擊的是單字或整個詞
          candidatesToShow = (token.candidates || []).map(c => ({
            ...c,
            isFromDict: true
          }));
          headerText = `選擇候選字 (${token.rom})`;
        } else {
          // 點擊的是多字詞中的某個字
          const syllable = token.charToSyllable ? token.charToSyllable[selectedCharIndex] : null;

          if (syllable && dict) {
            // 先添加詞表中的所有形式（可能有多個，如「仁愛」「情愛」）
            const dictForms = token.candidates || [];
            candidatesToShow.push(...dictForms.map(c => ({
              ...c,
              isFromDict: true,
              label: '詞表'
            })));

            // 再添加該音節的所有候選字
            const syllableCandidates = dict.syllables[syllable] || [];
            candidatesToShow.push(...syllableCandidates.map(c => ({
              ...c,
              isFromDict: false,
              label: null
            })));
          }

          headerText = `選擇候選字 (${syllable || token.rom})`;
        }

        if (candidatesToShow.length === 0) return null;

        return (
          <div
            className="candidates-popup"
            ref={candidateRef}
            style={{
              left: `${candidatePos.x}px`,
              top: `${candidatePos.y}px`
            }}
          >
            <div className="candidates-header">
              {headerText}
            </div>
            <div className="candidates-grid">
              {candidatesToShow.map((candidate, idx) => {
                const isCurrentlySelected = selectedCharIndex === null
                  ? candidate.han === token.han
                  : (candidate.isFromDict && candidate.han === token.han);

                return (
                  <div
                    key={idx}
                    className={`candidate-item ${isCurrentlySelected ? 'selected' : ''}`}
                    onClick={() => selectCandidate(selectedIndex, selectedCharIndex, candidate.han, candidate.isFromDict)}
                  >
                    <span className="candidate-han">{candidate.han}</span>
                    <span className="candidate-freq">
                      {Math.round(candidate.freq * 10) / 10}
                    </span>
                  </div>
                );
              })}
            </div>
          </div>
        );
      })()}

      <div className="converter-info">
        <h3>使用說明</h3>
        <ul>
          <li><strong>輸入格式：</strong>支援興化平話字（如 <code>Pó-chéng</code>）或輸入式拼音（如 <code>Pou2-cheng2</code>），也可混合使用</li>
          <ul>
            <li><code>a̤ = aa</code>、<code>e̤ = ee</code>、<code>o̤ = oo</code>、<code>ṳ = y</code>、<code>ⁿ = nn</code></li>
            <li><code>a = a1</code>、<code>á = a2</code>、<code>â = a3</code>、<code>a̍ = a4</code>、<code>ā = a5</code>、<code>ah = ah6</code>、<code>a̍h = ah7</code>，1、6可不輸調號</li>
          </ul>
          <li><strong>分詞：</strong>同一個詞的音節用連字號 <code>-</code> 連接，不同詞用空格分隔</li>
          <li><strong>候選字：</strong>點擊漢字可查看並選擇其他候選字（按聖經中的詞頻排序）</li>
          <li><strong>未知音節：</strong>字典中沒有的音節會顯示為 <code>▣</code></li>
          <li><strong>非羅馬字：</strong>保留原文</li>
        </ul>

        <h3>資料來源</h3>
        <ul>
          <li><a href="https://github.com/tesiniong/borhlang-ime" target="_blank" rel="noopener">木蘭輸入法</a>（現代詞彙）</li>
          <li>聖經文本（詞頻統計）</li>
          <li>共收錄 2,000+ 個音節、18,000+ 個詞組</li>
        </ul>

        <h3>注意</h3>
        <ul>
          <li>由於資料來源限制，輸出結果可能包含錯誤，請謹慎甄別。</li>
        </ul>
      </div>
    </div>
  );
};

export default RomToHanConverter;
