import { useState, useEffect } from 'react';
import './AboutBible.css';

function ProgressTable({ stats }) {
  if (!stats || !stats.totals) return null;

  const calculatePercent = (value, total) => {
    if (total === 0) return '0.0';
    return ((value / total) * 100).toFixed(1);
  };

  const renderTable = (lang) => {
    const data = stats[lang];
    const totals = stats.totals;
    const langText = lang === 'rom' ? '羅馬字' : '漢字';

    return (
      <table className="progress-table">
        <thead>
          <tr>
            <th>{langText}</th>
            <th>舊約</th>
            <th>新約</th>
            <th>總計</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>書</td>
            <td>{data.ot.books}/{totals.ot.books} ({calculatePercent(data.ot.books, totals.ot.books)}%)</td>
            <td>{data.nt.books}/{totals.nt.books} ({calculatePercent(data.nt.books, totals.nt.books)}%)</td>
            <td>{data.total.books}/{totals.all.books} ({calculatePercent(data.total.books, totals.all.books)}%)</td>
          </tr>
          <tr>
            <td>章</td>
            <td>{data.ot.chapters}/{totals.ot.chapters} ({calculatePercent(data.ot.chapters, totals.ot.chapters)}%)</td>
            <td>{data.nt.chapters}/{totals.nt.chapters} ({calculatePercent(data.nt.chapters, totals.nt.chapters)}%)</td>
            <td>{data.total.chapters}/{totals.all.chapters} ({calculatePercent(data.total.chapters, totals.all.chapters)}%)</td>
          </tr>
          <tr>
            <td>節</td>
            <td>{data.ot.verses}/{totals.ot.verses} ({calculatePercent(data.ot.verses, totals.ot.verses)}%)</td>
            <td>{data.nt.verses}/{totals.nt.verses} ({calculatePercent(data.nt.verses, totals.nt.verses)}%)</td>
            <td>{data.total.verses}/{totals.all.verses} ({calculatePercent(data.total.verses, totals.all.verses)}%)</td>
          </tr>
        </tbody>
      </table>
    );
  };

  return (
    <div className="progress-tables-container">
      {renderTable('rom')}
      {renderTable('han')}
    </div>
  );
}


function AboutBible() {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    fetch(`${import.meta.env.BASE_URL}stats.json`)
      .then(response => response.json())
      .then(data => setStats(data))
      .catch(err => console.error("Failed to load stats.json:", err));
  }, []);


  return (
    <div className="about-page">
      <div className="about-container">
        <h1 className="about-title">關於興化語聖經</h1>
        <p className="about-subtitle">About the Hinghua Bible</p>

        <section className="about-section">
          <h2>緣起與傳承</h2>
          <p>
            本站致力於保存並重現<strong>1912年</strong>出版的《<strong>興化語舊新約全書</strong>》。這部珍貴的文獻由<strong>美以美會</strong>傳教士<strong>蒲魯士</strong>（William N. Brewster）夫婦等人翻譯，採用<strong>興化平話字</strong>書寫，並由美國聖經公會發行。
          </p>
          <p>
            此版本以<a href="https://w.wiki/GcBJ" target="_blank">施約瑟淺文理譯本</a>翻譯而成。全書含舊約39卷、新約27卷，共計一千四百多頁，承載了百年前莆仙地區的語言風貌。
          </p>
          <p>
            憑藉數位化工程，我們期盼讓這份百年前的語言遺產不再塵封於圖書館的角落，而能重新活躍於現代人的視野中，供學界研究，亦供後人追尋鄉音。
          </p>
        </section>

        <section className="about-section">
          <h2>數位化目標</h2>
          <p>
              這不僅是一次掃描，更是一場「文字復活」的工程。
          </p>
          <p>
            借助<a href="https://dl.lib.ntu.edu.tw/s/westrare/item/129333" target="_blank">臺灣大學圖書館數位典藏館</a>和 <a href="https://hdl.handle.net/2027/uc1.31822025315045" target="_blank">HathiTrust Digital Library</a> 所提供的資料，本站得以彙整這部珍貴的歷史影像。我們將原書掃描檔進行處理後以此為底本，致力於將羅馬字轉寫為數位文本，讓這份百年前的語言遺產在數位時代獲得新生。
          </p>
        </section>

        <section className="about-section">
          <h2>當前進度</h2>
          <p>
            本專案的文本數位化工作仍在進行中。目前的錄入進度詳細如下：
          </p>
          {stats ? <ProgressTable stats={stats} /> : <p>正在載入統計資料...</p>}
        </section>

        <section className="about-section">
          <h2>如何使用</h2>
          <p>
            為了滿足不同的閱讀需求，本站提供了多種瀏覽模式。
          </p>
          <p>
            點擊經節旁的 📖 圖示，隨時可喚出原書掃描頁，讓您與歷史文獻零距離接觸。
          </p>
        </section>

        <section className="about-section">
          <h2>參與貢獻</h2>
          <p>
            這是一個開源專案，每一份力量都彌足珍貴。無論是協助錄入剩餘經卷、校對文本，或是提供語言學建議，我們都誠摯歡迎。若您對興化語感興趣，請<a href="https://github.com/tesiniong/hinghua-singging" target="_blank">加入我們</a>，一起守護這門日漸式微的美麗語言。
          </p>
        </section>

        <section className="about-section about-footer-section">
          <h2>維護者</h2>
          <p className="contact-info">
            Siniong, 桃泽
          </p>
        </section>
      </div>
    </div>
  );
}

export default AboutBible;
