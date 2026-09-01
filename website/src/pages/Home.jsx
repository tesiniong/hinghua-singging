import { useState, useEffect } from 'react';
import BibleReader from '../components/BibleReader';
import './Home.css';

function Home() {
  const [bibleData, setBibleData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch(`${import.meta.env.BASE_URL}bible_data.json`)
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
    <div className="home">
      <header className="app-header">
        <div className="header-container">
          <div className="title-line title-han">舊新約全書　興化平話</div>
          <div className="title-line title-rom">GŪ-SING-IO̤H CÉ̤ⁿ-CṲ HING-HUA̍ BÁⁿ-UĀ</div>
          <div className="title-line title-eng">
            <span className="title-eng-large">THE HOLY BIBLE</span><br />
            <span className="title-eng-script">Containing the</span> <span className="title-eng-sc">OLD AND NEW TESTAMENTS</span><br />
            <span className="title-eng-sc">in the HINGHWA DIALECT, ROMANIZED</span><br />
            <span className="title-eng-sc">anno domini 1912</span>
          </div>
        </div>
      </header>

      <main className="app-main">
        <BibleReader bibleData={bibleData} />
      </main>
    </div>
  );
}

export default Home;
