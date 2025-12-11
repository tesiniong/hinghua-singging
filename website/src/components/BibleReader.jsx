import { useState, useEffect } from 'react';
import './BibleReader.css';
import ModeSelector from './ModeSelector';
import DualColumn from './DualColumn';
import RubyMode from './RubyMode';
import SingleLanguage from './SingleLanguage';
import SearchBox from './SearchBox';

function BibleReader({ bibleData }) {
  const [mode, setMode] = useState('dual'); // 'dual', 'ruby', 'han-only', 'rom-only'
  const [currentChapter, setCurrentChapter] = useState(0);
  const [pageMapping, setPageMapping] = useState(null);

  useEffect(() => {
    fetch(`${import.meta.env.BASE_URL}chapter-page-mapping.json`)
      .then(response => response.json())
      .then(data => setPageMapping(data))
      .catch(err => console.error('Failed to load page mapping:', err));
  }, []);

  if (!bibleData || !bibleData.books || bibleData.books.length === 0) {
    return <div className="bible-reader-error">沒有可用的聖經資料</div>;
  }

  const book = bibleData.books[0];
  const chapter = book.chapters[currentChapter];

  // 獲取當前章節對應的頁面
  const getPageForChapter = () => {
    if (!pageMapping || !book.name_han) return null;
    const bookMapping = pageMapping[book.name_han];
    if (!bookMapping) return null;
    const chapterMapping = bookMapping[String(chapter.chapter)];
    if (!chapterMapping) return null;
    return chapterMapping.page_start;
  };

  const handleModeChange = (newMode) => {
    setMode(newMode);
  };

  const handlePrevChapter = () => {
    if (currentChapter > 0) {
      setCurrentChapter(currentChapter - 1);
    }
  };

  const handleNextChapter = () => {
    if (currentChapter < book.chapters.length - 1) {
      setCurrentChapter(currentChapter + 1);
    }
  };

  const handleSearchResultClick = (chapterIdx) => {
    setCurrentChapter(chapterIdx);
    // 滾動到頁面頂部
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <div className="bible-reader">
      <div className="container">
        <SearchBox bibleData={bibleData} onResultClick={handleSearchResultClick} />

        <div className="bible-controls">
          <ModeSelector currentMode={mode} onModeChange={handleModeChange} />

          <div className="chapter-nav">
            <button
              onClick={handlePrevChapter}
              disabled={currentChapter === 0}
              className="nav-button"
            >
              ← 上一章
            </button>

            <span className="chapter-indicator">
              第 {chapter.chapter} 章
              {getPageForChapter() && (
                <a
                  href={`/viewer.html?page=${getPageForChapter()}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="page-link"
                  title="查看原始掃描頁面"
                >
                  📖
                </a>
              )}
            </span>

            <button
              onClick={handleNextChapter}
              disabled={currentChapter === book.chapters.length - 1}
              className="nav-button"
            >
              下一章 →
            </button>
          </div>
        </div>

        <div className="bible-content">
          {mode === 'dual' && <DualColumn chapter={chapter} />}
          {mode === 'ruby' && <RubyMode chapter={chapter} />}
          {mode === 'han-only' && <SingleLanguage chapter={chapter} language="han" />}
          {mode === 'rom-only' && <SingleLanguage chapter={chapter} language="rom" />}
        </div>
      </div>
    </div>
  );
}

export default BibleReader;
