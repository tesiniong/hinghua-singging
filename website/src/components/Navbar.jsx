import { Link, useLocation } from 'react-router-dom';
import ThemeToggle from './ThemeToggle';
import './Navbar.css';

function Navbar() {
  const location = useLocation();

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-brand">
          <span className="navbar-brand-han">興化白話聖經</span>
          <span className="navbar-brand-rom">Hing-hua̍ Bá-uā Sìng-gîng</span>
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
            語音介紹
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
