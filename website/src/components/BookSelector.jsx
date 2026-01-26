import { useState, useEffect, useRef, useCallback } from 'react';
import './BookSelector.css';

function BookSelector({ bibleData, currentBookIndex, currentChapter, onBookSelect, onChapterSelect }) {
  const [isOpen, setIsOpen] = useState(false);
  const [bookList, setBookList] = useState([]);
  const [selectedBook, setSelectedBook] = useState(null); // 展開章節選擇的書卷
  const [chapterPopupPosition, setChapterPopupPosition] = useState({ top: 0 });
  const selectorRef = useRef(null);
  const dropdownRef = useRef(null);
  const bookCellRefs = useRef({});

  // 載入書目清單
  useEffect(() => {
    fetch(`${import.meta.env.BASE_URL}bookList.json`)
      .then(res => res.json())
      .then(data => setBookList(data))
      .catch(err => console.error('載入書目清單失敗:', err));
  }, []);

  // 點擊外部關閉選單
  useEffect(() => {
    const handleClickOutside = (e) => {
      if (selectorRef.current && !selectorRef.current.contains(e.target)) {
        setIsOpen(false);
        setSelectedBook(null);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  if (!bibleData || !bibleData.books || bibleData.books.length === 0) {
    return null;
  }

  const currentBook = bibleData.books[currentBookIndex];

  // 根據英文名稱找到書卷在 bibleData 中的索引
  const findBookIndex = (engName) => {
    return bibleData.books.findIndex(b => b.name_eng === engName);
  };

  // 計算章節選擇器位置（相對於 dropdown）
  const updateChapterPopupPosition = useCallback((book) => {
    const cellElement = bookCellRefs.current[book.eng];
    const dropdownElement = dropdownRef.current;
    if (cellElement && dropdownElement) {
      const cellRect = cellElement.getBoundingClientRect();
      const dropdownRect = dropdownElement.getBoundingClientRect();
      // 計算相對於 dropdown 的垂直位置
      setChapterPopupPosition({
        top: cellRect.bottom - dropdownRect.top + dropdownElement.scrollTop + 4
      });
    }
  }, []);

  // 監聽 dropdown 滾動，更新章節選單位置
  useEffect(() => {
    const dropdownElement = dropdownRef.current;
    if (!dropdownElement || !selectedBook) return;

    const handleScroll = () => {
      updateChapterPopupPosition(selectedBook);
    };

    dropdownElement.addEventListener('scroll', handleScroll);
    return () => dropdownElement.removeEventListener('scroll', handleScroll);
  }, [selectedBook, updateChapterPopupPosition]);

  // 處理書卷點擊
  const handleBookClick = (book, e) => {
    if (!book.hasContent) return;

    // 如果點擊已選中的書卷，關閉章節選擇器
    if (selectedBook && selectedBook.eng === book.eng) {
      setSelectedBook(null);
      return;
    }

    // 計算章節選擇器位置
    updateChapterPopupPosition(book);
    setSelectedBook(book);
  };

  // 檢查章節是否有內容
  const chapterHasContent = (bookEngName, chapter) => {
    const bookIndex = findBookIndex(bookEngName);
    if (bookIndex === -1) return false;
    const bookData = bibleData.books[bookIndex];
    if (!bookData || !bookData.chapters) return false;
    // 檢查該章節是否存在於 bibleData 中
    return bookData.chapters.some(ch => ch.chapter === chapter);
  };

  // 處理章節點擊
  const handleChapterClick = (book, chapter) => {
    // 檢查章節是否有內容
    if (!chapterHasContent(book.eng, chapter)) return;

    const bookIndex = findBookIndex(book.eng);
    if (bookIndex !== -1) {
      onBookSelect(bookIndex);
      if (onChapterSelect) {
        onChapterSelect(chapter);
      }
    }
    setSelectedBook(null);
    setIsOpen(false);
  };

  // 分組書卷
  const forewordBooks = bookList.filter(b => b.testament === 'foreword');
  const otBooks = bookList.filter(b => b.testament === 'ot');
  const ntBooks = bookList.filter(b => b.testament === 'nt');

  // 渲染書卷網格
  const renderBookGrid = (books, title) => (
    <div className="book-section">
      <h3 className="book-section-title">{title}</h3>
      <div className="book-grid">
        {books.map((book) => (
          <div
            key={book.eng}
            ref={el => bookCellRefs.current[book.eng] = el}
            className={`book-cell ${!book.hasContent ? 'disabled' : ''} ${
              currentBook?.name_eng === book.eng ? 'current' : ''
            } ${selectedBook?.eng === book.eng ? 'selected' : ''}`}
            onClick={(e) => handleBookClick(book, e)}
          >
            <span className="book-abbr">{book.abbr || book.han.slice(0, 2)}</span>
            <span className="book-full-name">{book.rom}</span>
          </div>
        ))}
      </div>
    </div>
  );

  // 渲染章節選擇器
  const renderChapterPopup = () => {
    if (!selectedBook) return null;

    const chapters = Array.from({ length: selectedBook.chapters }, (_, i) => i + 1);

    return (
      <div
        className="chapter-popup"
        style={{ top: chapterPopupPosition.top }}
      >
        <div className="chapter-popup-header">
          <span>{selectedBook.han}</span>
          <button className="chapter-popup-close" onClick={() => setSelectedBook(null)}>×</button>
        </div>
        <div className="chapter-grid">
          {chapters.map(ch => {
            const hasContent = chapterHasContent(selectedBook.eng, ch);
            const isCurrent = currentBook?.name_eng === selectedBook.eng && currentChapter === ch;
            return (
              <button
                key={ch}
                className={`chapter-cell ${isCurrent ? 'current' : ''} ${!hasContent ? 'disabled' : ''}`}
                onClick={() => handleChapterClick(selectedBook, ch)}
                disabled={!hasContent}
              >
                {ch}
              </button>
            );
          })}
        </div>
      </div>
    );
  };

  return (
    <div className="book-selector" ref={selectorRef}>
      <button
        className="book-selector-button"
        onClick={() => {
          setIsOpen(!isOpen);
          if (isOpen) setSelectedBook(null);
        }}
      >
        <span className="book-name-display">
          <span className="book-name-han">{currentBook.name_han}</span>
          <span className="book-name-sep">·</span>
          <span className="book-name-rom">{currentBook.name_rom}</span>
        </span>
        <span className="dropdown-arrow">{isOpen ? '▲' : '▼'}</span>
      </button>

      {isOpen && (
        <div className="book-selector-dropdown" ref={dropdownRef}>
          {forewordBooks.length > 0 && renderBookGrid(forewordBooks, '前言')}
          {renderBookGrid(otBooks, '舊約聖經')}
          {renderBookGrid(ntBooks, '新約聖經')}
          {renderChapterPopup()}
        </div>
      )}
    </div>
  );
}

export default BookSelector;
