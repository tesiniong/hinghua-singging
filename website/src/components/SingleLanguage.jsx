import './SingleLanguage.css';

function SingleLanguage({ chapter, language, pageMapping, bookName }) {
  if (!chapter || !chapter.verses) {
    return <div>沒有經文資料</div>;
  }

  const getPageForVerse = (verseNum) => {
    if (!pageMapping || !bookName) return null;
    const bookMapping = pageMapping[bookName];
    if (!bookMapping) return null;
    const chapterMapping = bookMapping[String(chapter.chapter)];
    if (!chapterMapping || !chapterMapping.verses) return null;
    return chapterMapping.verses[String(verseNum)];
  };

  const isRoman = language === 'rom';
  const fontClass = isRoman ? 'font-roman' : 'font-chinese';

  return (
    <div className={`single-language ${fontClass}`}>
      <div className="single-chapter">
        {chapter.verses.map((verse) => (
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
            <span className="verse-text">{verse[language]}</span>
          </span>
        ))}
      </div>
    </div>
  );
}

export default SingleLanguage;
