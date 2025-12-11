import { useState, useEffect } from 'react';
import './App.css';
import BibleReader from './components/BibleReader';

function App() {
  const [bibleData, setBibleData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {fetch(`${import.meta.env.BASE_URL}bible_data.json`)
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed to load bible data');
        }
        return response.json();
      })
      .then(data => {
        setBibleData(data);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="app-loading">
        <div className="loading-spinner"></div>
        <p>載入中...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="app-error">
        <h2>載入錯誤</h2>
        <p>{error}</p>
      </div>
    );
  }

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-container">
          <div className="title-line title-han">舊新約全書　興化白話</div>
          <div className="title-line title-rom">GŪ-SING-IO̤H CÉ̤NG-CṲ   HING-HUA̍ BÁⁿ-UĀ</div>
          <div className="title-line title-eng">
            <span className="title-eng-large">THE HOLY BIBLE</span><br />
            <span className="title-eng-script">Containing the</span> <span className="title-eng-sc">OLD AND NEW TESTAMENTS</span><br />
            <span className="title-eng-sc">IN THE HINGHWA DIALECT, ROMANIZED</span><br />
            <span className="title-eng-sc">ANNO DOMINI 1912</span>
          </div>
        </div>
      </header>

      <main className="app-main">
        <BibleReader bibleData={bibleData} />
      </main>

      <footer className="app-footer">
        <div className="container">
          <p>&copy; 2025 興化語聖經數位化專案</p>
          <p className="mt-1">Created by Tè Sîn-iông, 桃泽</p>
        </div>
      </footer>
    </div>
  );
}

export default App;
