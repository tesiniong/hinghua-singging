import { useState } from 'react';
import './SearchBox.css';

function SearchBox({ bibleData, onResultClick }) {
  const [searchTerm, setSearchTerm] = useState('');
  const [results, setResults] = useState([]);
  const [isSearching, setIsSearching] = useState(false);

  const handleSearch = (term) => {
    setSearchTerm(term);

    if (!term.trim() || !bibleData) {
      setResults([]);
      return;
    }

    setIsSearching(true);

    // 搜尋所有書卷的所有章節的所有經節
    const searchResults = [];
    const lowerTerm = term.toLowerCase();

    bibleData.books.forEach(book => {
      book.chapters.forEach((chapter, chapterIdx) => {
        // 過濾出經節（排除段落標題）
        const verses = chapter.sections.filter(section => section.type === 'verse');

        verses.forEach(verse => {
          // 搜尋羅馬字和漢字
          const romText = verse.rom.toLowerCase();
          const hanText = verse.han;

          if (romText.includes(lowerTerm) || hanText.includes(term)) {
            searchResults.push({
              bookName: book.name_han,
              chapterNum: chapter.chapter,
              chapterIdx: chapterIdx,
              verseNum: verse.verse,
              rom: verse.rom,
              han: verse.han,
            });
          }
        });
      });
    });

    setResults(searchResults);
    setIsSearching(false);
  };

  const highlightText = (text, term) => {
    if (!term) return text;

    const index = text.toLowerCase().indexOf(term.toLowerCase());
    if (index === -1) return text;

    return (
      <>
        {text.substring(0, index)}
        <mark>{text.substring(index, index + term.length)}</mark>
        {text.substring(index + term.length)}
      </>
    );
  };

  return (
    <div className="search-box">
      <div className="search-input-wrapper">
        <input
          type="text"
          className="search-input"
          placeholder="搜尋羅馬字或漢字..."
          value={searchTerm}
          onChange={(e) => handleSearch(e.target.value)}
        />
        {searchTerm && (
          <button
            className="clear-button"
            onClick={() => handleSearch('')}
          >
            ✕
          </button>
        )}
      </div>

      {isSearching && (
        <div className="search-loading">搜尋中...</div>
      )}

      {results.length > 0 && (
        <div className="search-results">
          <div className="results-header">
            找到 {results.length} 個結果
          </div>
          <div className="results-list">
            {results.map((result, idx) => (
              <div
                key={idx}
                className="result-item"
                onClick={() => onResultClick(result.chapterIdx)}
              >
                <div className="result-reference">
                  {result.bookName} {result.chapterNum}:{result.verseNum}
                </div>
                <div className="result-text">
                  <div className="result-han">
                    {highlightText(result.han, searchTerm)}
                  </div>
                  <div className="result-rom">
                    {highlightText(result.rom, searchTerm)}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {searchTerm && results.length === 0 && !isSearching && (
        <div className="no-results">沒有找到符合的結果</div>
      )}
    </div>
  );
}

export default SearchBox;
