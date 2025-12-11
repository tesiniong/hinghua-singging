import './SingleLanguage.css';

function SingleLanguage({ chapter, language, pageMapping, bookName }) {
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

  const isRoman = language === 'rom';
  const fontClass = isRoman ? 'font-roman' : 'font-chinese';

  return (
    <div className={`single-language ${fontClass}`}>
      <div className="single-chapter">
        {chapter.verses.map((verse, index) => {
          const verseText = verse[language];
          // 對於羅馬字模式，如果經文末尾沒有空格或標點，加上空格
          const needsSpace = isRoman && index < chapter.verses.length - 1 &&
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
