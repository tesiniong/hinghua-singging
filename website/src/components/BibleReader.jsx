import { useState, useEffect, useRef } from 'react';
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
  const controlsRef = useRef(null);
  const [shouldScrollToControls, setShouldScrollToControls] = useState(false);

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

  const book = bibleData.books[currentBookIndex];
  const isForeword = book.name_eng === 'Foreword' || book.name_eng === 'Preface';
  const isEnglishForeword = book.name_eng === 'Foreword';

  useEffect(() => {
    // 如果是英文序，強制切換到 rom-only 模式
    if (isEnglishForeword && mode !== 'rom-only') {
      setMode('rom-only');
    }
  }, [currentBookIndex, isEnglishForeword]);

  // Effect to scroll to controls after search result click
  useEffect(() => {
    if (shouldScrollToControls && controlsRef.current) {
      controlsRef.current.scrollIntoView({ behavior: 'smooth', block: 'start' });
      setShouldScrollToControls(false);
    }
  }, [shouldScrollToControls, currentBookIndex, currentChapter]);


  if (!bibleData || !bibleData.books || bibleData.books.length === 0) {
    return <div className="bible-reader-error">沒有可用的聖經資料</div>;
  }

  if (!book || !book.chapters || book.chapters.length === 0) {
    return (
      <div className="bible-reader-error">
        此書卷尚未錄入資料
      </div>
    );
  }

  const chapter = book.chapters[currentChapter];

  // 獲取當前章節對應的頁面
  const getPageForChapter = () => {
    // 序言直接使用 page mapping
    if (isForeword) {
      if (!pageMapping || !pageMapping[book.name_han]) return null;
      try {
        return pageMapping[book.name_han]["1"].page_start;
      } catch (e) {
        return null;
      }
    }

    // 一般書卷使用 OCR 結果找到該章第1節的頁面
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

  const handleSearchResultClick = (bookIndex, chapterIndex) => {
    setCurrentBookIndex(bookIndex);
    setCurrentChapter(chapterIndex);
    setShouldScrollToControls(true);
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
          currentChapter={currentChapter + 1}  // 傳遞 1-based 章節號
          onBookSelect={handleBookSelect}
          onChapterSelect={(ch) => setCurrentChapter(ch - 1)}  // 轉換為 0-based 索引
        />

        <SearchBox bibleData={bibleData} onResultClick={handleSearchResultClick} />

        <div className="bible-controls" ref={controlsRef}>
          <ModeSelector
            currentMode={mode}
            onModeChange={handleModeChange}
            isEnglishForeword={isEnglishForeword}
          />

          <div className="chapter-nav">
            <button
              onClick={handlePrevChapter}
              disabled={currentChapter === 0}
              className="nav-button"
            >
              ← 上一章
            </button>

            <span className="chapter-indicator">
              {chapter.chapter_title_han && <div>{chapter.chapter_title_han}</div>}
              {chapter.chapter_title_rom && <div style={{ fontSize: '0.85em', color: '#666' }}>{chapter.chapter_title_rom}</div>}
            </span>

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
              isForeword={isForeword}
            />
          )}
          {mode === 'ruby' && (
            <RubyMode
              chapter={chapter}
              pageMapping={pageMapping}
              pageOcrResults={pageOcrResults}
              bookName={book.name_han}
              isForeword={isForeword}
            />
          )}
          {mode === 'han-only' && (
            <SingleLanguage
              chapter={chapter}
              language="han"
              pageMapping={pageMapping}
              pageOcrResults={pageOcrResults}
              bookName={book.name_han}
              isForeword={isForeword}
            />
          )}
          {mode === 'rom-only' && (
            <SingleLanguage
              chapter={chapter}
              language="rom"
              pageMapping={pageMapping}
              pageOcrResults={pageOcrResults}
              bookName={book.name_han}
              isForeword={isForeword}
            />
          )}
        </div>
      </div>
    </div>
  );
}

export default BibleReader;
