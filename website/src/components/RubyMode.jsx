import './RubyMode.css';

function RubyMode({ chapter, pageMapping, pageOcrResults, bookName }) {
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

  const renderRubyTokens = (tokens) => {
    return tokens.map((token, idx) => {
      if (token.type === 'punct') {
        // 只使用漢字標點
        return <span key={idx} className="ruby-punct">{token.han}</span>;
      }

      if (token.type === 'word' && token.han && token.rom) {
        // 有羅馬字和漢字的詞
        return (
          <ruby key={idx} className="ruby-word">
            {token.han}
            <rt>{token.rom}</rt>
          </ruby>
        );
      }

      if (token.type === 'word' && token.han) {
        // 只有漢字
        return <span key={idx} className="ruby-word-no-rom">{token.han}</span>;
      }

      if (token.type === 'word' && token.rom) {
        // 只有羅馬字（這種情況應該很少見）
        return <span key={idx} className="ruby-rom-only">{token.rom}</span>;
      }

      return null;
    });
  };

  return (
    <div className="ruby-mode">
      <div className="ruby-chapter">
        {verses.map((verse, idx) => (
          <span key={verse.verse} className="ruby-verse">
            <sup className="verse-marker">
              {verse.verse}
              {getPageForVerse(verse.verse) && (
                <a
                  href={`${import.meta.env.BASE_URL}viewer.html?page=${getPageForVerse(verse.verse)}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="verse-image-link-ruby"
                  title="查看原始掃描頁面"
                >
                  📖
                </a>
              )}
            </sup>
            {renderRubyTokens(verse.tokens)}
          </span>
        ))}
      </div>
    </div>
  );
}

export default RubyMode;
