import { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import ThemeToggle from './ThemeToggle';
import './Navbar.css';

function Navbar() {
  const location = useLocation();
  const [isVisible, setIsVisible] = useState(true);
  const [lastScrollY, setLastScrollY] = useState(0);

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
      }

      setLastScrollY(currentScrollY);
    };

    // 添加滾動監聽，使用 passive 提升性能
    window.addEventListener('scroll', handleScroll, { passive: true });

    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
  }, [lastScrollY]);

  return (
    <nav className={`navbar ${isVisible ? 'navbar-visible' : 'navbar-hidden'}`}>
      <div className="navbar-container">
        <Link to="/" className="navbar-brand">
          <span className="navbar-brand-han">興化平話聖經</span>
          <span className="navbar-brand-rom">Hing-hua̍ Báⁿ-uā Si̍ng-ging</span>
        </Link>

        <div className="navbar-menu">
          <Link
            to="/"
            className={`navbar-link ${location.pathname === '/' ? 'active' : ''}`}
          >
            首頁
          </Link>
          <Link
            to="/about-bible"
            className={`navbar-link ${location.pathname === '/about-bible' ? 'active' : ''}`}
          >
            聖經介紹
          </Link>
          <Link
            to="/about-language"
            className={`navbar-link ${location.pathname === '/about-language' ? 'active' : ''}`}
          >
            平話字介紹
          </Link>
        </div>

        <div className="navbar-theme">
          <ThemeToggle />
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
