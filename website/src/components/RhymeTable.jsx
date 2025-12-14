import React, { useState, useMemo } from 'react';
import './RhymeTable.css';
import rhymeData from '../data/rhymeTableData.json';

function RhymeTable() {
  // 所有方言點
  const allDialects = [
    '莆田', '江口', '南日', '華亭', '常泰', '新縣',
    '笏石', '平海', '湄洲', '東莊', '東海', '仙遊',
    '游洋', '楓亭', '園莊', '鳳山'
  ];

  // 預設顯示莆田和仙遊
  const [selectedDialects, setSelectedDialects] = useState(['莆田', '仙遊']);

  // 切換方言點選擇
  const toggleDialect = (dialect) => {
    setSelectedDialects(prev => {
      if (prev.includes(dialect)) {
        // 至少保留一個方言點
        if (prev.length > 1) {
          return prev.filter(d => d !== dialect);
        }
        return prev;
      } else {
        return [...prev, dialect];
      }
    });
  };

  // 全選/全不選
  const toggleAll = () => {
    if (selectedDialects.length === allDialects.length) {
      setSelectedDialects(['莆田', '仙遊']); // reset to default
    } else {
      setSelectedDialects(allDialects);
    }
  };

  return (
    <div className="rhyme-table-container">
      {/* 方言点选择器 */}
      <div className="dialect-selector">
        <h4>選擇方言點：</h4>
        <div className="dialect-checkboxes">
          <label className="select-all-checkbox">
            <input
              type="checkbox"
              checked={selectedDialects.length === allDialects.length}
              onChange={toggleAll}
            />
            <span>全選/重置</span>
          </label>
          {allDialects.map(dialect => (
            <label key={dialect} className="dialect-checkbox">
              <input
                type="checkbox"
                checked={selectedDialects.includes(dialect)}
                onChange={() => toggleDialect(dialect)}
              />
              <span>{dialect}</span>
            </label>
          ))}
        </div>
      </div>

      {/* 表格容器（支援橫向捲動） */}
      <div className="table-wrapper">
        <table className="rhyme-table">
          <thead>
            {/* 第一行header */}
            <tr>
              <th rowSpan={2} className="sticky-col sticky-header col-letter">韻母字</th>
              <th rowSpan={2} className="sticky-col sticky-header col-examples">例字</th>
              <th rowSpan={2} className="sticky-col sticky-header col-value">擬音</th>
              <th colSpan={selectedDialects.length} className="sticky-header">音值</th>
            </tr>
            {/* 第二行header - 方言點名稱 */}
            <tr>
              {selectedDialects.map(dialect => (
                <th key={dialect} className="sticky-header dialect-header">
                  {dialect}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rhymeData.map((row, rowIndex) => (
              <tr key={rowIndex} className={row.hasBorder ? 'border-bottom' : ''}>
                {/* 韻母字 - 只在 rowSpan != 0 時渲染 */}
                {row.rowSpan !== 0 && (
                  <td
                    className="sticky-col col-letter"
                    rowSpan={row.rowSpan > 1 ? row.rowSpan : 1}
                  >
                    <div dangerouslySetInnerHTML={{ __html: row.letter }} />
                  </td>
                )}

                {/* 例字 - 每列都渲染 */}
                <td className="col-examples">
                  <div dangerouslySetInnerHTML={{ __html: row.examples }} />
                </td>

                {/* 擬音 - 只在 phoneticRowSpan != 0 時渲染 */}
                {row.phoneticRowSpan !== 0 && (
                  <td
                    className="col-value"
                    rowSpan={row.phoneticRowSpan > 1 ? row.phoneticRowSpan : 1}
                  >
                    <div dangerouslySetInnerHTML={{ __html: row.phonetic }} />
                  </td>
                )}

                {/* 各方言點音值 */}
                {selectedDialects.map((dialect, dialectIndex) => {
                  const allDialectIndex = allDialects.indexOf(dialect);
                  const value = row.dialectValues[allDialectIndex];
                  return (
                    <td key={dialectIndex} className="dialect-value">
                      <div dangerouslySetInnerHTML={{ __html: value || '-' }} />
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default RhymeTable;
