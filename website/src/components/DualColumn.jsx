import './DualColumn.css';

function DualColumn({ chapter, pageMapping, bookName }) {
  if (!chapter || !chapter.verses) {
    return <div>沒有經文資料</div>;
  }

  const getPageForVerse = (verseNum) => {
    if (!pageMapping) return null;

    // Try actual book name first, then fallback to 創世記
    const bookMapping = pageMapping[bookName] || pageMapping['創世記'];
    if (!bookMapping) return null;

    const chapterMapping = bookMapping[String(chapter.chapter)];
    if (!chapterMapping) return null;

    // Try to find specific verse page, otherwise use chapter start page
    if (chapterMapping.verses && chapterMapping.verses[String(verseNum)]) {
      return chapterMapping.verses[String(verseNum)];
    }

    return chapterMapping.page_start;
  };

  return (
    <div className="dual-column">
      {chapter.verses.map((verse) => (
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
            <div className="verse-rom">{verse.rom}</div>
            <div className="verse-han">{verse.han}</div>
          </div>
        </div>
      ))}
    </div>
  );
}

export default DualColumn;
