import { useState, useEffect } from 'react';
import './BibleReader.css';
import BookSelector from './BookSelector';
import ModeSelector from './ModeSelector';
import DualColumn from './DualColumn';
import RubyMode from './RubyMode';
import SingleLanguage from './SingleLanguage';
import SearchBox from './SearchBox';

function BibleReader({ bibleData }) {
  const [mode, setMode] = useState('dual'); // 'dual', 'ruby', 'han-only', 'rom-only'
  const [currentBookIndex, setCurrentBookIndex] = useState(0);
  const [currentChapter, setCurrentChapter] = useState(0);
  const [pageMapping, setPageMapping] = useState(null);
  const [pageOcrResults, setPageOcrResults] = useState(null);

  useEffect(() => {
    // 載入章節-頁面對應表
    fetch(`${import.meta.env.BASE_URL}chapter-page-mapping.json`)
      .then(response => response.json())
      .then(data => setPageMapping(data))
      .catch(err => console.error('Failed to load page mapping:', err));

    // 載入 OCR 結果（用於精確查找經節對應的頁面）
    fetch(`${import.meta.env.BASE_URL}page-ocr-results.json`)
      .then(response => response.json())
      .then(data => setPageOcrResults(data))
      .catch(err => console.error('Failed to load page OCR results:', err));
  }, []);

  if (!bibleData || !bibleData.books || bibleData.books.length === 0) {
    return <div className="bible-reader-error">沒有可用的聖經資料</div>;
  }

  const book = bibleData.books[currentBookIndex];

  if (!book || !book.chapters || book.chapters.length === 0) {
    return (
      <div className="bible-reader-error">
        此書卷尚未錄入資料
      </div>
    );
  }

  const chapter = book.chapters[currentChapter];

  // 獲取當前章節對應的頁面（使用 OCR 結果找到該章第1節的頁面）
  const getPageForChapter = () => {
    if (!pageOcrResults || !book.name_han) return null;

    let targetPage = null;
    const sortedPages = Object.keys(pageOcrResults).sort();

    for (const pageNum of sortedPages) {
      const pageInfo = pageOcrResults[pageNum];

      // 檢查書名是否匹配
      if (pageInfo.book_han !== book.name_han) {
        continue;
      }

      const pageChapter = pageInfo.chapter;
      const pageVerse = pageInfo.verse || 1;

      // 找到最後一個 (chapter:verse) <= (目標chapter:1) 的頁面
      if (pageChapter < chapter.chapter) {
        targetPage = pageNum;
        continue;
      }
      if (pageChapter === chapter.chapter && pageVerse <= 1) {
        targetPage = pageNum;
      }
      if (pageChapter > chapter.chapter) {
        break;
      }
    }

    return targetPage;
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

  const handleBookSelect = (bookIndex) => {
    setCurrentBookIndex(bookIndex);
    setCurrentChapter(0); // 切換書卷時重置到第一章
  };

  return (
    <div className="bible-reader">
      <div className="container">
        <BookSelector
          bibleData={bibleData}
          currentBookIndex={currentBookIndex}
          onBookSelect={handleBookSelect}
        />

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
              <div>{chapter.chapter_title_han}</div>
              <div style={{ fontSize: '0.85em', color: '#666' }}>{chapter.chapter_title_rom}</div>
              {getPageForChapter() && (
                <a
                  href={`${import.meta.env.BASE_URL}viewer.html?page=${getPageForChapter()}`}
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
          {mode === 'dual' && (
            <DualColumn
              chapter={chapter}
              pageMapping={pageMapping}
              pageOcrResults={pageOcrResults}
              bookName={book.name_han}
            />
          )}
          {mode === 'ruby' && (
            <RubyMode
              chapter={chapter}
              pageMapping={pageMapping}
              pageOcrResults={pageOcrResults}
              bookName={book.name_han}
            />
          )}
          {mode === 'han-only' && (
            <SingleLanguage
              chapter={chapter}
              language="han"
              pageMapping={pageMapping}
              pageOcrResults={pageOcrResults}
              bookName={book.name_han}
            />
          )}
          {mode === 'rom-only' && (
            <SingleLanguage
              chapter={chapter}
              language="rom"
              pageMapping={pageMapping}
              pageOcrResults={pageOcrResults}
              bookName={book.name_han}
            />
          )}
        </div>
      </div>
    </div>
  );
}

export default BibleReader;
