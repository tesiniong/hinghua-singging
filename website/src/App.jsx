import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import AboutBible from './pages/AboutBible';
import AboutLanguage from './pages/AboutLanguage';

function App() {
  return (
    <Router basename={import.meta.env.BASE_URL}>
      <div className="app">
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about-bible" element={<AboutBible />} />
          <Route path="/about-language" element={<AboutLanguage />} />
        </Routes>
        <footer className="app-footer">
          <div className="container">
            <p>&copy; 2025 興化語聖經數位化專案</p>
            <p className="mt-1">Created by Siniong, 桃泽</p>
          </div>
        </footer>
      </div>
    </Router>
  );
}

export default App;
