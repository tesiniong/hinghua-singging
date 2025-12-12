import './AboutBible.css';

function AboutBible() {
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
            我們希望透過數位化工程，讓這份百年前的語言遺產不再塵封於圖書館的角落，而能重新活躍於現代人的視野中，供學界研究，亦供後人追尋鄉音。
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
            目前已完成全書影像處理，並率先釋出《創世記》、《馬太福音》、《約翰二書》、《約翰三書》、《使徒猶大書》五卷的完整數位文本。其餘 61 卷的錄入工作正如火如荼進行中。
          </p>
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
            Tè Sîn-iông, 桃泽
          </p>
        </section>
      </div>
    </div>
  );
}

export default AboutBible;
