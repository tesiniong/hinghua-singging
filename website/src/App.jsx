import { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import AboutBible from './pages/AboutBible';
import AboutLanguage from './pages/AboutLanguage';
import HomophoneTable from './pages/HomophoneTable';
import RomToHanConverter from './pages/RomToHanConverter';

function App() {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    fetch(`${import.meta.env.BASE_URL}stats.json`)
      .then(response => response.json())
      .then(data => setStats(data))
      .catch(err => console.error("Failed to load stats.json:", err));
  }, []);

  return (
    <Router basename={import.meta.env.BASE_URL}>
      <div className="app">
        <Navbar />
        <main className="app-main">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/about-bible" element={<AboutBible />} />
            <Route path="/about-language" element={<AboutLanguage />} />
            <Route path="/homophone-table" element={<HomophoneTable />} />
            <Route path="/rom-to-han-converter" element={<RomToHanConverter />} />
          </Routes>
        </main>
        <footer className="app-footer">
          <div className="container">
            {stats && (
              <p className="stats-summary">
                羅馬字已錄入 {stats.rom.total.verses} 節 | 漢字已錄入 {stats.han.total.verses} 節
              </p>
            )}
            <p>&copy; 2025 興化語聖經數位化專案</p>
            <p className="mt-1">Created by Siniong, 桃泽</p>
          </div>
        </footer>
      </div>
    </Router>
  );
}

export default App;
