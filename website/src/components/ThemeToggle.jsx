import { useState, useEffect } from 'react';
import './ThemeToggle.css';

function ThemeToggle() {
  // 從 localStorage 讀取，預設為 system
  const [theme, setTheme] = useState(() => {
    return localStorage.getItem('theme') || 'system';
  });

  useEffect(() => {
    const applyTheme = (selectedTheme) => {
      let actualTheme = selectedTheme;

      if (selectedTheme === 'system') {
        // 檢測系統偏好
        actualTheme = window.matchMedia('(prefers-color-scheme: dark)').matches
          ? 'dark'
          : 'light';
      }

      // 設定 data-theme 屬性到 html 元素
      document.documentElement.setAttribute('data-theme', actualTheme);
    };

    // 應用當前主題
    applyTheme(theme);

    // 儲存到 localStorage
    localStorage.setItem('theme', theme);

    // 如果是 system 模式，監聽系統主題變化
    if (theme === 'system') {
      const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
      const handler = (e) => {
        document.documentElement.setAttribute('data-theme', e.matches ? 'dark' : 'light');
      };

      mediaQuery.addEventListener('change', handler);
      return () => mediaQuery.removeEventListener('change', handler);
    }
  }, [theme]);

  const handleThemeChange = (newTheme) => {
    setTheme(newTheme);
  };

  return (
    <div className="theme-toggle">
      <button
        className={`theme-button ${theme === 'light' ? 'active' : ''}`}
        onClick={() => handleThemeChange('light')}
        aria-label="明亮模式"
        title="明亮模式"
      >
        ☀️
      </button>
      <button
        className={`theme-button ${theme === 'dark' ? 'active' : ''}`}
        onClick={() => handleThemeChange('dark')}
        aria-label="黑暗模式"
        title="黑暗模式"
      >
        🌙
      </button>
      <button
        className={`theme-button ${theme === 'system' ? 'active' : ''}`}
        onClick={() => handleThemeChange('system')}
        aria-label="系統設定"
        title="系統設定"
      >
        💻
      </button>
    </div>
  );
}

export default ThemeToggle;
