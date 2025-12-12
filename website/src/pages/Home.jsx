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
          <div className="title-line title-han">舊新約全書　興化白話</div>
          <div className="title-line title-rom">GŪ-SING-IO̤H CÉ̤NG-CṲ   HING-HUA̍ BÁⁿ-UĀ</div>
          <div className="title-line title-eng">
            <span className="title-eng-large">THE HOLY BIBLE</span><br />
            <span className="title-eng-script">Containing the</span> <span className="title-eng-sc">OLD AND NEW TESTAMENTS</span><br />
            <span className="title-eng-sc">in the HINGHWA DIALECT, ROMANIZED</span><br />
            <span className="title-eng-sc">anno domini 1912</span>
          </div>
        </div>
      </header>

      <section className="app-intro">
        <div className="intro-container">
          <p className="intro-text">
            本網站收錄 <strong>1912 年</strong>出版的<strong>興化語</strong>（又稱<strong>興化語</strong>、<strong>興化話</strong>）<strong>舊新約全書</strong>數位化/數字化版本。
            興化語是莆田、仙遊地區使用的閩語變體，本<strong>聖經</strong>採用<strong>興化平話字</strong>書寫（此<strong>羅馬字</strong>系統保留了19世紀末的<strong>舊新約全書</strong>音系），
            並提供<strong>漢字轉寫</strong>對照，目標是完整呈現<strong>舊約</strong>與<strong>新約</strong>經文。
          </p>
          <p className="intro-text intro-eng">
            This website features a digitized version of the <strong>Hinghwa</strong> (also known as <strong>Pu-Xian Min</strong>) <strong>Holy Bible</strong>, originally published in <strong>1912</strong>.
            Hinghwa is a variety of Min Chinese spoken in the Putian and Xianyou regions. This <strong>Bible</strong> is written in <strong>Hinghwa Romanized</strong> script (a <strong>Romanized</strong> system preserving the phonology of the late 19th century)
            and provides a parallel <strong>Chinese character transliteration</strong>, aiming to fully present the scriptures of the <strong>Old Testament</strong> and <strong>New Testament</strong>.
          </p>
        </div>
      </section>

      <main className="app-main">
        <BibleReader bibleData={bibleData} />
      </main>
    </div>
  );
}

export default Home;
