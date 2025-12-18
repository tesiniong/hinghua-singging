import './ModeSelector.css';

function ModeSelector({ currentMode, onModeChange, isEnglishForeword }) {
  const modes = [
    { id: 'rom-only', label: '羅馬字原文', icon: 'A' },
    { id: 'han-only', label: '漢字轉寫', icon: '漢' },
    { id: 'dual', label: '雙欄對照', icon: '⚏' },
    { id: 'ruby', label: 'Ruby 注音', icon: '㋐' },
  ];

  return (
    <div className="mode-selector">
      <div className="mode-label">閱讀模式：</div>
      <div className="mode-buttons">
        {modes.map(mode => (
          <button
            key={mode.id}
            className={`mode-button ${currentMode === mode.id ? 'active' : ''}`}
            onClick={() => onModeChange(mode.id)}
            disabled={isEnglishForeword && mode.id !== 'rom-only'}
          >
            <span className="mode-icon">{mode.icon}</span>
            <span className="mode-text">{mode.label}</span>
          </button>
        ))}
      </div>
    </div>
  );
}

export default ModeSelector;
