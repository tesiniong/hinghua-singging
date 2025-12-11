import './DualColumn.css';

function DualColumn({ chapter }) {
  if (!chapter || !chapter.verses) {
    return <div>沒有經文資料</div>;
  }

  const renderTokens = (tokens, type) => {
    return tokens.map((token, idx) => {
      if (token.type === 'punct') {
        return <span key={idx} className="punct">{token[type]}</span>;
      }
      if (token.type === 'word') {
        return (
          <span key={idx} className={`word word-${token.form}`}>
            {token[type]}
          </span>
        );
      }
      return null;
    });
  };

  return (
    <div className="dual-column">
      {chapter.verses.map((verse) => (
        <div key={verse.verse} className="verse-row">
          <div className="verse-number">{verse.verse}</div>

          <div className="verse-content">
            <div className="verse-rom">
              {renderTokens(verse.tokens, 'rom')}
            </div>

            <div className="verse-han">
              {renderTokens(verse.tokens, 'han')}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}

export default DualColumn;
