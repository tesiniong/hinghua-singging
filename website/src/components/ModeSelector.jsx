import './ModeSelector.css';

function ModeSelector({ currentMode, onModeChange }) {
  const modes = [
    { id: 'dual', label: '雙欄對照', icon: '⚏' },
    { id: 'ruby', label: 'Ruby 注音', icon: '㋐' },
    { id: 'han-only', label: '僅漢字', icon: '漢' },
    { id: 'rom-only', label: '僅羅馬字', icon: 'A' },
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
