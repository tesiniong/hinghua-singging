import { useState, useEffect, useRef } from 'react';
import { Link, useLocation } from 'react-router-dom';
import ThemeToggle from './ThemeToggle';
import './Navbar.css';

function Navbar() {
  const location = useLocation();
  const [isVisible, setIsVisible] = useState(true);
  const [lastScrollY, setLastScrollY] = useState(0);
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const menuRef = useRef(null);

  // 處理滾動事件
  useEffect(() => {
    const handleScroll = () => {
      const currentScrollY = window.scrollY;

      // 如果在頂部（滾動位置小於 10px），總是顯示
      if (currentScrollY < 10) {
        setIsVisible(true);
      }
      // 向上滾動，顯示導航欄
      else if (currentScrollY < lastScrollY) {
        setIsVisible(true);
      }
      // 向下滾動，隱藏導航欄
      else if (currentScrollY > lastScrollY && currentScrollY > 100) {
        setIsVisible(false);
        // 導航欄隱藏時一併收起選單（原本靠額外的 effect 同步 state）
        setIsMenuOpen(false);
      }

      setLastScrollY(currentScrollY);
    };

    // 添加滾動監聽，使用 passive 提升性能
    window.addEventListener('scroll', handleScroll, { passive: true });

    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
  }, [lastScrollY]);

  // 點擊外部關閉選單
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (menuRef.current && !menuRef.current.contains(event.target)) {
        setIsMenuOpen(false);
      }
    };

    if (isMenuOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isMenuOpen]);

  // 切換選單開關
  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  // 點擊連結後關閉選單
  const handleLinkClick = () => {
    setIsMenuOpen(false);
  };

  return (
    <nav className={`navbar ${isVisible ? 'navbar-visible' : 'navbar-hidden'}`}>
      <div className="navbar-container">
        <Link to="/" className="navbar-brand">
          <span className="navbar-brand-han">興化平話聖經</span>
          <span className="navbar-brand-rom">Hing-hua̍ Báⁿ-uā Si̍ng-ging</span>
        </Link>

        <div className="navbar-right">
          <div className="navbar-theme">
            <ThemeToggle />
          </div>

          <div className="navbar-menu-container" ref={menuRef}>
            <button
              className="navbar-menu-button"
              onClick={toggleMenu}
              aria-label="選單"
            >
              ☰
            </button>

            {isMenuOpen && (
              <div className="navbar-dropdown">
                <Link
                  to="/"
                  className={`navbar-dropdown-link ${location.pathname === '/' ? 'active' : ''}`}
                  onClick={handleLinkClick}
                >
                  首頁
                </Link>
                <Link
                  to="/about-bible"
                  className={`navbar-dropdown-link ${location.pathname === '/about-bible' ? 'active' : ''}`}
                  onClick={handleLinkClick}
                >
                  聖經介紹
                </Link>
                <Link
                  to="/about-language"
                  className={`navbar-dropdown-link ${location.pathname === '/about-language' ? 'active' : ''}`}
                  onClick={handleLinkClick}
                >
                  平話字介紹
                </Link>
                <Link
                  to="/homophone-table"
                  className={`navbar-dropdown-link ${location.pathname === '/homophone-table' ? 'active' : ''}`}
                  onClick={handleLinkClick}
                >
                  同音字表
                </Link>
                <Link
                  to="/rom-to-han-converter"
                  className={`navbar-dropdown-link ${location.pathname === '/rom-to-han-converter' ? 'active' : ''}`}
                  onClick={handleLinkClick}
                >
                  羅馬字轉漢字
                </Link>
              </div>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
