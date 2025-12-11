import './RubyMode.css';

function RubyMode({ chapter, pageMapping, bookName }) {
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
        {chapter.verses.map((verse, idx) => (
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
