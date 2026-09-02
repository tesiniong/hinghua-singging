import './SingleLanguage.css';
import DraftMark from './DraftMark';

function SingleLanguage({ chapter, language, pageOcrResults, bookName, isForeword }) {
  if (!chapter || !chapter.sections) {
    return <div>沒有經文資料</div>;
  }

  // 過濾出經節（排除段落標題）
  const verses = chapter.sections.filter(section => section.type === 'verse');

  const getPageForVerse = (verseNum) => {
    // 序言不顯示節級頁碼連結
    if (isForeword) return null;
    if (!pageOcrResults) return null;

    // 找到該書該章該節對應的頁面
    // 邏輯：找到最後一個 (chapter:verse) <= (目標chapter:目標verse) 的頁面
    let targetPage = null;
    const sortedPages = Object.keys(pageOcrResults).sort();

    for (const pageNum of sortedPages) {
      const pageInfo = pageOcrResults[pageNum];

      // 檢查書名是否匹配
      if (pageInfo.book_han !== bookName) {
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

  // 將文本中的換行符轉換為 <br> 元素
  // hasLineBreaks: 如果有節內換行，結尾會額外加 <br>
  const renderTextWithLineBreaks = (text, hasLineBreaks) => {
    if (!text) return null;

    const lines = text.split('\n');
    return (
      <>
        {lines.map((line, index) => (
          <span key={index}>
            {line}
            {index < lines.length - 1 && <br />}
          </span>
        ))}
        {hasLineBreaks && !isForeword && <br />}
      </>
    );
  };

  const renderVerse = (verse, index) => {
    const verseText = verse[language];
    const hasLineBreaks = verseText && verseText.includes('\n');
    const draftFlags = isRoman ? verse.rom_draft : undefined; // 只有羅馬字會是 OCR 草稿

    // 對於羅馬字模式，如果經文末尾沒有空格或標點，加上空格
    // 但如果有節內換行，就不加空格（因為已經有 <br>）
    const needsSpace = isRoman && index < verses.length - 1 &&
                       verseText && !/[\s.,;:!?]$/.test(verseText) && !hasLineBreaks;

    return (
      <>
        {!isForeword && (
          <span className="verse-number">
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
            <DraftMark flags={draftFlags} compact />
          </span>
        )}
        <span className={`verse-text${draftFlags ? ' rom-draft' : ''}`}>
          {renderTextWithLineBreaks(verseText, hasLineBreaks)}
          {!isForeword && needsSpace ? ' ' : ''}
        </span>
      </>
    );
  };

  return (
    <div className={`single-language ${fontClass}`}>
      <div className="single-chapter">
        {verses.map((verse, index) => (
          isForeword ? (
            <p key={verse.verse} className="single-paragraph">
              {renderVerse(verse, index)}
            </p>
          ) : (
            <span key={verse.verse} className="single-verse">
              {renderVerse(verse, index)}
            </span>
          )
        ))}
      </div>
    </div>
  );
}

export default SingleLanguage;
