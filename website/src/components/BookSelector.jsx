import { useState } from 'react';
import './BookSelector.css';

function BookSelector({ bibleData, currentBookIndex, onBookSelect }) {
  const [isOpen, setIsOpen] = useState(false);

  if (!bibleData || !bibleData.books || bibleData.books.length === 0) {
    return null;
  }

  const books = bibleData.books;
  const currentBook = books[currentBookIndex];

  // 目前只有一卷書，暫時不需要舊約/新約分類
  // 如果未來有多卷，可以根據 book index 判斷

  return (
    <div className="book-selector">
      <button
        className="book-selector-button"
        onClick={() => setIsOpen(!isOpen)}
      >
        <span className="book-name-display">
          <span className="book-name-rom">{currentBook.name_rom}</span>
          <span className="book-name-sep">·</span>
          <span className="book-name-han">{currentBook.name_han}</span>
        </span>
        <span className="dropdown-arrow">{isOpen ? '▲' : '▼'}</span>
      </button>

      {isOpen && (
        <div className="book-selector-dropdown">
          <div className="book-list">
            {books.map((book, index) => (
              <button
                key={index}
                className={`book-item ${index === currentBookIndex ? 'active' : ''}`}
                onClick={() => {
                  onBookSelect(index);
                  setIsOpen(false);
                }}
              >
                <span className="book-item-rom">{book.name_rom}</span>
                <span className="book-item-sep">·</span>
                <span className="book-item-han">{book.name_han}</span>
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default BookSelector;
