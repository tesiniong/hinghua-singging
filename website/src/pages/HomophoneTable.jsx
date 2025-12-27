import { useState, useEffect, useMemo } from 'react';
import './HomophoneTable.css';

// 聲母配置（興化語）
const INITIALS = [
  { value: '', label: '∅' },
  { value: 'b', label: 'b' },
  { value: 'p', label: 'p' },
  { value: 'm', label: 'm' },
  { value: 'd', label: 'd' },
  { value: 't', label: 't' },
  { value: 'n', label: 'n' },
  { value: 'l', label: 'l' },
  { value: 'g', label: 'g' },
  { value: 'k', label: 'k' },
  { value: 'ng', label: 'ng' },
  { value: 'h', label: 'h' },
  { value: 'c', label: 'c' },
  { value: 'ch', label: 'ch' },
  { value: 's', label: 's' },
];

// 聲調配置（興化語）
const TONES = [
  { value: '1', label: '1 (陰平)' },
  { value: '2', label: '2 (陽平)' },
  { value: '3', label: '3 (上聲)' },
  { value: '4', label: '4 (陰去)' },
  { value: '5', label: '5 (陽去)' },
  { value: '6', label: '6 (陰入)' },
  { value: '7', label: '7 (陽入)' },
];

// 韻母顯示轉換函數
const formatRhyme = (rhyme) => {
  if (!rhyme) return '';
  return rhyme
    .replace(/aa/g, 'a̤')
    .replace(/ee/g, 'e̤')
    .replace(/oo/g, 'o̤')
    .replace(/nn/g, 'ⁿ')
    .replace(/y/g, 'ṳ');
};

export default function HomophoneTable() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  const [selectedInitials, setSelectedInitials] = useState(new Set());
  const [selectedRhymes, setSelectedRhymes] = useState(new Set());
  const [selectedTones, setSelectedTones] = useState(new Set());

  // 載入資料
  useEffect(() => {
    fetch(`${import.meta.env.BASE_URL}homophoneData.json`)
      .then(res => res.json())
      .then(jsonData => {
        setData(jsonData);
        setLoading(false);
      })
      .catch(err => {
        console.error('載入同音字表失敗:', err);
        setLoading(false);
      });
  }, []);

  // 從資料中提取所有韻母，並按類型分組
  const allRhymes = useMemo(() => {
    if (!data) return { open: [], nasal: [], ng: [], checked: [] };

    const rhymesSet = new Set();
    data.syllables.forEach(s => rhymesSet.add(s.r));

    // 將韻母分類
    const open = [];    // 陰聲韻（不以 ⁿ, ng, h 結尾）
    const nasal = [];   // 鼻化韻（以 ⁿ 結尾）
    const ng = [];      // 鼻音韻（以 ng 結尾）
    const checked = []; // 入聲韻（以 h 結尾）

    Array.from(rhymesSet).forEach(r => {
      const displayLabel = formatRhyme(r);
      const obj = { value: r, label: displayLabel };

      if (displayLabel.endsWith('ⁿ')) {
        nasal.push(obj);
      } else if (displayLabel.endsWith('ng')) {
        ng.push(obj);
      } else if (displayLabel.endsWith('h')) {
        checked.push(obj);
      } else {
        open.push(obj);
      }
    });

    // 每類內部按字母序排序
    const sortFn = (a, b) => a.value.localeCompare(b.value);
    open.sort(sortFn);
    nasal.sort(sortFn);
    ng.sort(sortFn);
    checked.sort(sortFn);

    return { open, nasal, ng, checked };
  }, [data]);

  // 過濾音節
  const filteredSyllables = useMemo(() => {
    if (!data) return [];

    // 如果全都沒選擇，返回空陣列
    if (selectedInitials.size === 0 && selectedRhymes.size === 0 && selectedTones.size === 0) {
      return [];
    }

    return data.syllables.filter(s => {
      const matchInitial = selectedInitials.size === 0 || selectedInitials.has(s.i);
      const matchRhyme = selectedRhymes.size === 0 || selectedRhymes.has(s.r);
      const matchTone = selectedTones.size === 0 || selectedTones.has(s.t);
      return matchInitial && matchRhyme && matchTone;
    });
  }, [data, selectedInitials, selectedRhymes, selectedTones]);

  // 計算總字數
  const totalCharsCount = useMemo(() => {
    return filteredSyllables.reduce((sum, syllable) => sum + syllable.chars.length, 0);
  }, [filteredSyllables]);

  // 切換選擇工具函數
  const toggleSelection = (set, value, setFunction) => {
    const newSet = new Set(set);
    if (newSet.has(value)) {
      newSet.delete(value);
    } else {
      newSet.add(value);
    }
    setFunction(newSet);
  };

  if (loading) {
    return (
      <div className="homophone-container">
        <div className="loading">載入中...</div>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="homophone-container">
        <div className="error">載入失敗</div>
      </div>
    );
  }

  return (
    <div className="homophone-container">
      <h1>同音字表</h1>
      <p className="disclaimer">
        本字表由系統自動產生，可能因文本對齊失效、辨識錯誤、過度類推、類推失敗等原因產生錯誤，請謹慎判斷。<br/>本表暫時不區分甲乙類陽入音節。
      </p>

      {/* 聲母選擇 */}
      <div className="filter-section">
        <div className="filter-header">
          <h2>聲母</h2>
          <button 
            onClick={() => setSelectedInitials(new Set())} 
            className="action-btn"
            disabled={selectedInitials.size === 0}
          >
            清除
          </button>
        </div>
        <div className="filter-buttons">
          {INITIALS.map(initial => {
            const isSelected = selectedInitials.has(initial.value);
            return (
              <button
                key={initial.value}
                onClick={() => toggleSelection(selectedInitials, initial.value, setSelectedInitials)}
                className={`filter-btn ${isSelected ? 'selected initial-selected' : ''}`}
              >
                {initial.label}
              </button>
            );
          })}
        </div>
      </div>

      {/* 韻母選擇 */}
      <div className="filter-section">
        <div className="filter-header">
          <h2>韻母</h2>
          <button
            onClick={() => setSelectedRhymes(new Set())}
            className="action-btn"
            disabled={selectedRhymes.size === 0}
          >
            清除
          </button>
        </div>

        {/* 陰聲韻 */}
        <div className="rhyme-group">
          <h3 className="rhyme-group-title">陰聲韻</h3>
          <div className="filter-buttons">
            {allRhymes.open.map(rhymeObj => {
              const isSelected = selectedRhymes.has(rhymeObj.value);
              return (
                <button
                  key={rhymeObj.value}
                  onClick={() => toggleSelection(selectedRhymes, rhymeObj.value, setSelectedRhymes)}
                  className={`filter-btn ${isSelected ? 'selected rhyme-selected' : ''}`}
                >
                  {rhymeObj.label}
                </button>
              );
            })}
          </div>
        </div>

        {/* 鼻化韻 */}
        <div className="rhyme-group">
          <h3 className="rhyme-group-title">鼻化韻</h3>
          <div className="filter-buttons">
            {allRhymes.nasal.map(rhymeObj => {
              const isSelected = selectedRhymes.has(rhymeObj.value);
              return (
                <button
                  key={rhymeObj.value}
                  onClick={() => toggleSelection(selectedRhymes, rhymeObj.value, setSelectedRhymes)}
                  className={`filter-btn ${isSelected ? 'selected rhyme-selected' : ''}`}
                >
                  {rhymeObj.label}
                </button>
              );
            })}
          </div>
        </div>

        {/* 鼻音韻 */}
        <div className="rhyme-group">
          <h3 className="rhyme-group-title">鼻音韻</h3>
          <div className="filter-buttons">
            {allRhymes.ng.map(rhymeObj => {
              const isSelected = selectedRhymes.has(rhymeObj.value);
              return (
                <button
                  key={rhymeObj.value}
                  onClick={() => toggleSelection(selectedRhymes, rhymeObj.value, setSelectedRhymes)}
                  className={`filter-btn ${isSelected ? 'selected rhyme-selected' : ''}`}
                >
                  {rhymeObj.label}
                </button>
              );
            })}
          </div>
        </div>

        {/* 入聲韻 */}
        <div className="rhyme-group">
          <h3 className="rhyme-group-title">入聲韻</h3>
          <div className="filter-buttons">
            {allRhymes.checked.map(rhymeObj => {
              const isSelected = selectedRhymes.has(rhymeObj.value);
              return (
                <button
                  key={rhymeObj.value}
                  onClick={() => toggleSelection(selectedRhymes, rhymeObj.value, setSelectedRhymes)}
                  className={`filter-btn ${isSelected ? 'selected rhyme-selected' : ''}`}
                >
                  {rhymeObj.label}
                </button>
              );
            })}
          </div>
        </div>
      </div>

      {/* 聲調選擇 */}
      <div className="filter-section">
        <div className="filter-header">
          <h2>聲調</h2>
          <button 
            onClick={() => setSelectedTones(new Set())} 
            className="action-btn"
            disabled={selectedTones.size === 0}
          >
            清除
          </button>
        </div>
        <div className="filter-buttons">
          {TONES.map(tone => {
            const isSelected = selectedTones.has(tone.value);
            return (
              <button
                key={tone.value}
                onClick={() => toggleSelection(selectedTones, tone.value, setSelectedTones)}
                className={`filter-btn ${isSelected ? 'selected tone-selected' : ''}`}
              >
                {tone.label}
              </button>
            );
          })}
        </div>
      </div>

      {/* 結果顯示 */}
      <div className="results-section">
        <h2 className="results-title">
          結果（共 {filteredSyllables.length} 個音節，{totalCharsCount} 個字）
        </h2>

        {filteredSyllables.length === 0 ? (
          <p className="no-results">請選擇聲母、韻母或聲調以顯示結果</p>
        ) : (
          <div className="syllables-list">
            {filteredSyllables.map((syllable, idx) => (
              <div key={idx} className="syllable-item">
                <h3 className="syllable-title">
                  {/* 先顯示正式羅馬字 */}
                  <span className="syllable-display">{syllable.p_display}</span>

                  {/* 再顯示括號內的輸入碼 (彩色) */}
                  <span className="syllable-input-code">
                    (
                    {syllable.i && <span className="syllable-initial">{syllable.i}</span>}
                    <span className="syllable-rhyme">{syllable.r}</span>
                    <span className="syllable-tone">{syllable.t}</span>
                    )
                  </span>

                  {/* 顯示字數 */}
                  <span className="syllable-char-count">
                    {syllable.chars.length} 個字
                  </span>
                </h3>

                {/* 字列表 */}
                <div className="char-list">
                  {syllable.chars.length === 0 ? (
                    <span className="no-chars">(無對應漢字)</span>
                  ) : (
                    syllable.chars.map((char, charIdx) => (
                      <span key={charIdx} className="char-item">
                        {char}
                      </span>
                    ))
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}