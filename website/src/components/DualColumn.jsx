import './DualColumn.css';

function DualColumn({ chapter, pageMapping, pageOcrResults, bookName }) {
  if (!chapter || !chapter.sections) {
    return <div>沒有經文資料</div>;
  }

  // 過濾出經節（排除段落標題）
  const verses = chapter.sections.filter(section => section.type === 'verse');

  const getPageForVerse = (verseNum) => {
    if (!pageOcrResults) return null;

    // 找到該書該章該節對應的頁面
    // 邏輯：找到最後一個 (chapter:verse) <= (目標chapter:目標verse) 的頁面
    let targetPage = null;
    const sortedPages = Object.keys(pageOcrResults).sort();

    for (const pageNum of sortedPages) {
      const pageInfo = pageOcrResults[pageNum];

      // 檢查書名是否匹配
      if (pageInfo.book_hanci !== bookName) {
        continue;
      }

      const pageChapter = pageInfo.chapter;
      const pageVerse = pageInfo.verse || 1;

      // 比較頁面起始位置和目標位置
      // 如果頁面起始 <= 目標，則這可能是正確的頁面
      if (pageChapter < chapter.chapter ||
          (pageChapter === chapter.chapter && pageVerse <= verseNum)) {
        targetPage = pageNum;
      } else {
        // 頁面起始 > 目標，表示已經超過了，停止搜尋
        break;
      }
    }

    return targetPage;
  };

  // 將文本中的換行符轉換為 <br> 元素
  const renderTextWithLineBreaks = (text) => {
    if (!text) return null;

    const lines = text.split('\n');
    return lines.map((line, index) => (
      <span key={index}>
        {line}
        {index < lines.length - 1 && <br />}
      </span>
    ));
  };

  return (
    <div className="dual-column">
      {verses.map((verse) => (
        <div key={verse.verse} className="verse-row">
          <div className="verse-number">
            {verse.verse}
            {getPageForVerse(verse.verse) && (
              <a
                href={`${import.meta.env.BASE_URL}viewer.html?page=${getPageForVerse(verse.verse)}`}
                target="_blank"
                rel="noopener noreferrer"
                className="verse-image-link"
                title="查看原始掃描頁面"
              >
                📖
              </a>
            )}
          </div>

          <div className="verse-content">
            <div className="verse-rom">{renderTextWithLineBreaks(verse.rom)}</div>
            <div className="verse-han">{renderTextWithLineBreaks(verse.han)}</div>
          </div>
        </div>
      ))}
    </div>
  );
}

export default DualColumn;
