import './DraftMark.css';

// 網站上對 OCR 草稿的統一說法；不要寫成「AI 生成」
export const DRAFT_LABEL = 'OCR 辨識草稿，未經校對';

/**
 * 節層級的草稿標記。flags 來自 bible_data.json 的 verse.rom_draft
 * （assemble.py 寫入時附上的校對旗標）；有旗標的節另加 ⚠，滑鼠移上可看疑點。
 * compact：放在上標節號旁時用，跟著節號的大小與位置。
 */
function DraftMark({ flags, compact = false }) {
  if (!flags) return null;
  const flagged = flags.length > 0;
  const title = flagged ? `${DRAFT_LABEL}。辨識時的疑點：${flags.join('；')}` : DRAFT_LABEL;
  return (
    <span
      className={`draft-mark${flagged ? ' flagged' : ''}${compact ? ' compact' : ''}`}
      title={title}
      aria-label={title}
    >
      草稿{flagged && <span className="draft-mark-warn" aria-hidden="true">⚠</span>}
    </span>
  );
}

export default DraftMark;
