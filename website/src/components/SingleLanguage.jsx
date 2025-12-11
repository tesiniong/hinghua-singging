import './SingleLanguage.css';

function SingleLanguage({ chapter, language }) {
  if (!chapter || !chapter.verses) {
    return <div>沒有經文資料</div>;
  }

  const renderTokens = (tokens, lang) => {
    return tokens.map((token, idx) => {
      if (token.type === 'punct') {
        return <span key={idx} className="single-punct">{token[lang]}</span>;
      }
      if (token.type === 'word') {
        return (
          <span key={idx} className={`single-word word-${token.form}`}>
            {token[lang]}
          </span>
        );
      }
      return null;
    });
  };

  const isRoman = language === 'rom';
  const fontClass = isRoman ? 'font-roman' : 'font-chinese';

  return (
    <div className={`single-language ${fontClass}`}>
      <div className="single-chapter">
        {chapter.verses.map((verse) => (
          <div key={verse.verse} className="single-verse">
            <sup className="verse-number">{verse.verse}</sup>
            <span className="verse-text">
              {renderTokens(verse.tokens, language)}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

export default SingleLanguage;
