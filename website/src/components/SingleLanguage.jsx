import './SingleLanguage.css';

function SingleLanguage({ chapter, language, pageMapping, pageOcrResults, bookName }) {
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

  const isRoman = language === 'rom';
  const fontClass = isRoman ? 'font-roman' : 'font-chinese';

  return (
    <div className={`single-language ${fontClass}`}>
      <div className="single-chapter">
        {verses.map((verse, index) => {
          const verseText = verse[language];
          // 對於羅馬字模式，如果經文末尾沒有空格或標點，加上空格
          const needsSpace = isRoman && index < verses.length - 1 &&
                             verseText && !/[\s.,;:!?]$/.test(verseText);

          return (
            <span key={verse.verse} className="single-verse">
              <sup className="verse-number">
                {verse.verse}
                {getPageForVerse(verse.verse) && (
                  <a
                    href={`${import.meta.env.BASE_URL}viewer.html?page=${getPageForVerse(verse.verse)}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="verse-image-link-inline"
                    title="查看原始掃描頁面"
                  >
                    📖
                  </a>
                )}
              </sup>
              <span className="verse-text">{verseText}{needsSpace ? ' ' : ''}</span>
            </span>
          );
        })}
      </div>
    </div>
  );
}

export default SingleLanguage;
