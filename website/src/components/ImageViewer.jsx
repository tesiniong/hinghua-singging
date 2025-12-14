import { useState, useEffect } from 'react';
import './ImageViewer.css';

function ImageViewer() {
  const [currentPage, setCurrentPage] = useState(null);
  const [imagePath, setImagePath] = useState('');
  const [scale, setScale] = useState(1);
  const [position, setPosition] = useState({ x: 0, y: 0 });
  const [isDragging, setIsDragging] = useState(false);
  const [dragStart, setDragStart] = useState({ x: 0, y: 0 });

  const MIN_PAGE = 1;
  const MAX_PAGE = 1485;

  useEffect(() => {
    // 從 URL 參數獲取圖片路徑
    const params = new URLSearchParams(window.location.search);
    const page = params.get('page');
    if (page) {
      const pageNum = parseInt(page, 10);
      setCurrentPage(pageNum);
      setImagePath(`${import.meta.env.BASE_URL}images/${page}.webp`);
    }
  }, []);

  const handleZoomIn = () => {
    setScale(prev => Math.min(prev + 0.2, 3));
  };

  const handleZoomOut = () => {
    setScale(prev => Math.max(prev - 0.2, 0.5));
  };

  const handleReset = () => {
    setScale(1);
    setPosition({ x: 0, y: 0 });
  };

  const handlePrevPage = () => {
    if (currentPage > MIN_PAGE) {
      const newPage = currentPage - 1;
      const newPageStr = newPage.toString().padStart(4, '0');
      setCurrentPage(newPage);
      setImagePath(`${import.meta.env.BASE_URL}images/${newPageStr}.webp`);
      // 更新 URL
      const newUrl = `${window.location.pathname}?page=${newPageStr}`;
      window.history.pushState({}, '', newUrl);
      // 重置縮放和位置
      setScale(1);
      setPosition({ x: 0, y: 0 });
    }
  };

  const handleNextPage = () => {
    if (currentPage < MAX_PAGE) {
      const newPage = currentPage + 1;
      const newPageStr = newPage.toString().padStart(4, '0');
      setCurrentPage(newPage);
      setImagePath(`${import.meta.env.BASE_URL}images/${newPageStr}.webp`);
      // 更新 URL
      const newUrl = `${window.location.pathname}?page=${newPageStr}`;
      window.history.pushState({}, '', newUrl);
      // 重置縮放和位置
      setScale(1);
      setPosition({ x: 0, y: 0 });
    }
  };

  const handleMouseDown = (e) => {
    setIsDragging(true);
    setDragStart({
      x: e.clientX - position.x,
      y: e.clientY - position.y
    });
  };

  const handleMouseMove = (e) => {
    if (isDragging) {
      setPosition({
        x: e.clientX - dragStart.x,
        y: e.clientY - dragStart.y
      });
    }
  };

  const handleMouseUp = () => {
    setIsDragging(false);
  };

  const handleWheel = (e) => {
    e.preventDefault();
    if (e.deltaY < 0) {
      handleZoomIn();
    } else {
      handleZoomOut();
    }
  };

  if (!imagePath) {
    return (
      <div className="image-viewer-error">
        <p>沒有指定圖片</p>
      </div>
    );
  }

  return (
    <div className="image-viewer">
      <div className="viewer-controls">
        <button
          onClick={handlePrevPage}
          className="control-btn"
          disabled={currentPage <= MIN_PAGE}
        >
          ← 前一頁
        </button>
        <button onClick={handleZoomOut} className="control-btn">縮小 (-)</button>
        <button onClick={handleReset} className="control-btn">重置</button>
        <button onClick={handleZoomIn} className="control-btn">放大 (+)</button>
        <button
          onClick={handleNextPage}
          className="control-btn"
          disabled={currentPage >= MAX_PAGE}
        >
          下一頁 →
        </button>
      </div>

      <div
        className="viewer-container"
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onMouseLeave={handleMouseUp}
        onWheel={handleWheel}
      >
        <img
          src={imagePath}
          alt="聖經頁面"
          className="viewer-image"
          style={{
            transform: `translate(${position.x}px, ${position.y}px) scale(${scale})`,
            cursor: isDragging ? 'grabbing' : 'grab'
          }}
          draggable={false}
        />
      </div>

      <div className="viewer-instructions">
        <p>
          完整圖檔、PDF請見{' '}
          <a
            href="https://github.com/tesiniong/hinghua-singging"
            target="_blank"
            rel="noopener noreferrer"
          >
            Github
          </a>
          。
        </p>
      </div>
    </div>
  );
}

export default ImageViewer;
