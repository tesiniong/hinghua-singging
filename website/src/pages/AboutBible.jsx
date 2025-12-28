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
            借助<a href="https://dl.lib.ntu.edu.tw/s/westrare/item/129333" target="_blank">臺灣大學圖書館數位典藏館</a>和 <a href="https://books.google.ca/books?id=5jiwAAAAIAAJ&printsec=frontcover#v=onepage&q&f=false" target="_blank">Google 圖書</a> 所提供的資料，本站得以彙整這部珍貴的歷史影像。我們將原書掃描檔進行處理後以此為底本，致力於將羅馬字轉寫為數位文本，讓這份百年前的語言遺產在數位時代獲得新生。
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
          <h2>漢字轉寫</h2>
          <p>
            1912年出版的《新舊約聖經》（以及1934年出版的《新約全書附詩篇》）皆不曾有漢字版。本站參考多種莆仙語專著和鄰近漢語的用字，以盡量避免多音字為原則編纂了漢字版本。詳細的用字規則仍在制定中。常見的用字如下：
          </p>

          <div className="hanzi-table-wrapper">
            <table className="hanzi-table">
              <thead>
                <tr>
                  <th>平話字</th>
                  <th>漢字</th>
                  <th>意思</th>
                </tr>
              </thead>
              <tbody>
                <tr><td>ā</td><td>啊</td><td>語助詞</td></tr>
                <tr><td>ā̤</td><td>解</td><td>能、會</td></tr>
                <tr><td>ah-na</td><td>安生</td><td>這樣</td></tr>
                <tr><td>bā̤</td><td>𣍐</td><td>不能、不會</td></tr>
                <tr><td>beoh</td><td>慾</td><td>要、想</td></tr>
                <tr><td>buh</td><td>複</td><td>又</td></tr>
                <tr><td>ca̤̍</td><td>這</td><td>這</td></tr>
                <tr><td>chu̍i</td><td>喙</td><td>嘴</td></tr>
                <tr><td>ciâ</td><td>者</td><td>這裡</td></tr>
                <tr><td>ciô̤</td><td>燳</td><td>各個</td></tr>
                <tr><td>cuh</td><td>即</td><td>就</td></tr>
                <tr><td>da</td><td>仱</td><td>現在</td></tr>
                <tr><td>da̍i</td><td>第一</td><td>最</td></tr>
                <tr><td>da̤u̍h</td><td>着</td><td>得、要、必須</td></tr>
                <tr><td>deo</td><td>都</td><td>都</td></tr>
                <tr><td>deó</td><td>著</td><td>在</td></tr>
                <tr><td>dó</td><td>涂</td><td>土</td></tr>
                <tr><td>do̤-ng</td><td>當央</td><td>當中</td></tr>
                <tr><td>ē</td><td>其</td><td>的</td></tr>
                <tr><td>gah</td><td>佮</td><td>和、與</td></tr>
                <tr><td>ga̍i</td><td>家己</td><td>自己</td></tr>
                <tr><td>ga̍u</td><td>遘</td><td>到</td></tr>
                <tr><td>hiô̤</td><td>遐</td><td>那裡</td></tr>
                <tr><td>ho̤h</td><td>復</td><td>又、還</td></tr>
                <tr><td>hn̍g-náng</td><td>方儂</td><td>誰</td></tr>
                <tr><td>hṳ̂</td><td>許</td><td>那</td></tr>
                <tr><td>iā</td><td>亦</td><td>也</td></tr>
                <tr><td>lā-la̍h</td><td>垃垃</td><td>垃圾</td></tr>
                <tr><td>lē</td><td>咧</td><td>語助詞</td></tr>
                <tr><td>léng</td><td>連</td><td>和、跟</td></tr>
                <tr><td>leo̍h</td><td>落</td><td>在</td></tr>
                <tr><td>lō̤</td><td>咯</td><td>嗎</td></tr>
                <tr><td>meh</td><td>乜</td><td>豈、難道</td></tr>
                <tr><td>mo̍ih-nō̤</td><td>物乇</td><td>東西</td></tr>
                <tr><td>ka̍ng</td><td>勘</td><td>問</td></tr>
                <tr><td>náng</td><td>儂</td><td>人</td></tr>
                <tr><td>nō̤</td><td>喏</td><td>僅僅、才</td></tr>
                <tr><td>sā̤</td><td>穧</td><td>多</td></tr>
                <tr><td>seh-na</td><td>怎生</td><td>怎麼</td></tr>
                <tr><td>seo</td><td>廝</td><td>相</td></tr>
                <tr><td>seo̍h</td><td>蜀</td><td>一</td></tr>
                <tr><td>ta̤̍h</td><td>摕</td><td>拿</td></tr>
                <tr><td>tó</td><td>塗</td><td>土</td></tr>
              </tbody>
            </table>
          </div>
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
