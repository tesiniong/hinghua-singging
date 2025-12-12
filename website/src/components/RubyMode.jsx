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

  const renderRubyTokens = (tokens, verseHan) => {
    // 找出漢字文本中所有換行符的位置，並轉換為"不含換行符"時的位置
    const adjustedBreakPositions = [];
    let charCount = 0; // 不含換行符的字符數

    for (let i = 0; i < verseHan.length; i++) {
      if (verseHan[i] === '\n') {
        // 記錄這個換行符應該在第幾個字符之後插入
        adjustedBreakPositions.push(charCount);
      } else {
        charCount++;
      }
    }

    const hasLineBreaks = adjustedBreakPositions.length > 0;

    // 渲染基本邏輯
    const renderBasicTokens = () => {
      return tokens.map((token, idx) => {
        if (token.type === 'punct') {
          return <span key={idx} className="ruby-punct">{token.han}</span>;
        }

        if (token.type === 'word' && token.han && token.rom) {
          return (
            <ruby key={idx} className="ruby-word">
              {token.han}
              <rt>{token.rom}</rt>
            </ruby>
          );
        }

        if (token.type === 'word' && token.han) {
          return <span key={idx} className="ruby-word-no-rom">{token.han}</span>;
        }

        if (token.type === 'word' && token.rom) {
          return <span key={idx} className="ruby-rom-only">{token.rom}</span>;
        }

        return null;
      });
    };

    // 如果沒有換行符，直接渲染
    if (!hasLineBreaks) {
      return renderBasicTokens();
    }

    // 有換行符的情況：需要在適當位置插入 <br>
    const result = [];
    let charPosition = 0; // 當前已渲染的字符數（不含換行符）
    let nextBreakIndex = 0; // 下一個需要插入的換行符索引

    tokens.forEach((token, idx) => {
      // 在渲染當前 token 之前，檢查是否需要插入換行符
      while (nextBreakIndex < adjustedBreakPositions.length &&
             charPosition >= adjustedBreakPositions[nextBreakIndex]) {
        result.push(<br key={`br-${nextBreakIndex}`} />);
        nextBreakIndex++;
      }

      // 渲染當前 token
      if (token.type === 'punct') {
        result.push(<span key={idx} className="ruby-punct">{token.han}</span>);
        charPosition += token.han.length;
      } else if (token.type === 'word' && token.han && token.rom) {
        result.push(
          <ruby key={idx} className="ruby-word">
            {token.han}
            <rt>{token.rom}</rt>
          </ruby>
        );
        charPosition += token.han.length;
      } else if (token.type === 'word' && token.han) {
        result.push(<span key={idx} className="ruby-word-no-rom">{token.han}</span>);
        charPosition += token.han.length;
      } else if (token.type === 'word' && token.rom) {
        result.push(<span key={idx} className="ruby-rom-only">{token.rom}</span>);
        // 只有羅馬字沒有漢字，不增加 charPosition
      }
    });

    // 檢查渲染完所有 tokens 後是否還有未處理的換行符
    while (nextBreakIndex < adjustedBreakPositions.length) {
      result.push(<br key={`br-${nextBreakIndex}`} />);
      nextBreakIndex++;
    }

    // 多行經文結尾額外加一個換行
    if (hasLineBreaks) {
      result.push(<br key="final-break" />);
    }

    return result;
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
            {renderRubyTokens(verse.tokens, verse.han)}
          </span>
        ))}
      </div>
    </div>
  );
}

export default RubyMode;
