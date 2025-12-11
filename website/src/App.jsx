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
        <div className="container">
          <h1>興化語聖經</h1>
          <p className="subtitle">Hing-hua Bible (1912)</p>
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
