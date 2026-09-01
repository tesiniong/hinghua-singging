import { useState, useEffect, useMemo } from 'react';
import './SearchBox.css';
import { foldRomanized, findRomanizedMatch } from '../utils/romanization';

// 結果過多時只渲染前面這些筆，其餘只報總數，避免一次插入上千個節點
const MAX_RESULTS = 200;
const DEBOUNCE_MS = 180;
const HAN_RE = /[㐀-䶿一-鿿豈-﫿]/;

function SearchBox({ bibleData, onResultClick }) {
  const [searchTerm, setSearchTerm] = useState('');
  const [query, setQuery] = useState('');
  const [fuzzy, setFuzzy] = useState(true);

  // 經節索引：折疊只在資料載入時做一次，不隨每次按鍵重算
  const verses = useMemo(() => {
    if (!bibleData || !bibleData.books) return [];
    const out = [];
    bibleData.books.forEach((book, bookIndex) => {
      book.chapters.forEach((chapter, chapterIdx) => {
        chapter.sections.forEach((section) => {
          if (section.type !== 'verse') return;
          const rom = section.rom || '';
          out.push({
            bookName: book.name_han,
            bookIndex,
            chapterNum: chapter.chapter,
            chapterIdx,
            verseNum: section.verse,
            rom,
            han: section.han || '',
            folded: foldRomanized(rom),
          });
        });
      });
    });
    return out;
  }, [bibleData]);

  // 打字時先緩衝，停下來才真的查
  useEffect(() => {
    const timer = setTimeout(() => setQuery(searchTerm), DEBOUNCE_MS);
    return () => clearTimeout(timer);
  }, [searchTerm]);

  const { results, total } = useMemo(() => {
    const term = query.trim();
    if (!term || verses.length === 0) return { results: [], total: 0 };

    const foldedQuery = foldRomanized(term);
    const romQuery = fuzzy ? foldedQuery.loose : foldedQuery.exact;
    const hanQuery = HAN_RE.test(term) ? term : '';

    const found = [];
    for (const verse of verses) {
      const romHit = romQuery ? findRomanizedMatch(verse.folded, romQuery, fuzzy) : null;
      let hanHit = null;
      if (hanQuery && verse.han) {
        const at = verse.han.indexOf(hanQuery);
        if (at !== -1) hanHit = { start: at, end: at + hanQuery.length };
      }
      if (romHit || hanHit) found.push({ ...verse, romHit, hanHit });
    }
    return { results: found.slice(0, MAX_RESULTS), total: found.length };
  }, [verses, query, fuzzy]);

  const isSettling = searchTerm.trim() !== '' && searchTerm !== query;

  const highlight = (text, hit) => {
    if (!hit) return text;
    return (
      <>
        {text.slice(0, hit.start)}
        <mark>{text.slice(hit.start, hit.end)}</mark>
        {text.slice(hit.end)}
      </>
    );
  };

  return (
    <div className="search-box">
      <div className="search-input-wrapper">
        <input
          type="text"
          className="search-input"
          placeholder="搜尋平話字、輸入式或漢字..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        {searchTerm && (
          <button
            className="clear-button"
            onClick={() => setSearchTerm('')}
            aria-label="清除搜尋"
          >
            ✕
          </button>
        )}
      </div>

      <div className="search-options">
        <div className="search-mode" role="group" aria-label="比對方式">
          <button
            className={`search-mode-button ${fuzzy ? 'active' : ''}`}
            onClick={() => setFuzzy(true)}
            aria-pressed={fuzzy}
          >
            模糊
          </button>
          <button
            className={`search-mode-button ${!fuzzy ? 'active' : ''}`}
            onClick={() => setFuzzy(false)}
            aria-pressed={!fuzzy}
          >
            精確
          </button>
        </div>
        <span className="search-hint">
          {fuzzy
            ? '不分聲調與變韻：siong 可找到 Siō̤ng'
            : '聲調與變韻須相符：sioong5 或 Siō̤ng'}
        </span>
      </div>

      {isSettling && <div className="search-loading">搜尋中...</div>}

      {results.length > 0 && (
        <div className="search-results">
          <div className="results-header">
            找到 {total} 個結果
            {total > results.length && `，顯示前 ${results.length} 筆`}
          </div>
          <div className="results-list">
            {results.map((result, idx) => (
              <div
                key={idx}
                className="result-item"
                onClick={() => onResultClick(result.bookIndex, result.chapterIdx)}
              >
                <div className="result-reference">
                  {result.bookName} {result.chapterNum}:{result.verseNum}
                </div>
                <div className="result-text">
                  {result.han && (
                    <div className="result-han">{highlight(result.han, result.hanHit)}</div>
                  )}
                  {result.rom && (
                    <div className="result-rom">{highlight(result.rom, result.romHit)}</div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {query.trim() && results.length === 0 && !isSettling && (
        <div className="no-results">沒有找到符合的結果</div>
      )}
    </div>
  );
}

export default SearchBox;
