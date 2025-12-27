import React from 'react';
import './AboutLanguage.css';
import RhymeTable from '../components/RhymeTable';

function AboutLanguage() {
  return (
    <div className="about-page">
      <div className="about-container">

        <section className="about-section">
          <h2>語言概況</h2>
          <p>
            莆仙語又稱興化語、興化話，是閩語的一個重要分支，使用人口約500萬人，主要分布於福建省莆田市市轄區和仙遊縣；
            在福清市西南部、平潭島、永泰縣南部、惠安（包括今泉港區）北部、永春東部的一些鄰近地區的村落也有使用。
            此外，在福建福鼎、邵武、建甌、建陽、寧德、霞浦、 德化和浙江玉環、溫嶺等縣市也都發現過莆仙語方言島。
          </p>
        </section>

        <section className="about-section">
          <h2>興化平話字</h2>
          <p>
            興化平話字（<span className="rom-text">Hing-hua̍ Báⁿ-uā-ci̍</span>）是由用於書寫莆仙語的羅馬字系統，
            於1890年由基督教美以美會傳教士蒲魯士夫婦發明並推行。興化平話字在宣教工作上多有使用，
            如1897年開始發行的刊物《奮興報》（<span className="rom-text">Heo̍ng-hing-beo̍</span>，現仍有部分資料保存於
            <a href="https://www.jdjcht.com/" target="_blank" rel="noopener noreferrer">南日草湖堂</a>）、
            1900年出版的《新約全書》、1912年出版的《舊新約全書》皆以此系統書寫。
            惟興化平話字未曾在教會以外大範圍流行，自20世紀中期便逐漸淡出世人視野，今日莆仙地區的年輕信徒亦罕有使用者。
          </p>

          <p>興化平話字共有23個字母（9個用於元音，14個用於輔音），如下：</p>

          <div className="table-responsive">
            <table className="alphabet-table">
              <tbody>
                <tr>
                  <th>大寫</th>
                  <td className="rom-text">A</td><td className="rom-text">A̤</td><td className="rom-text">B</td><td className="rom-text">C</td>
                  <td className="rom-text">Ch</td><td className="rom-text">D</td><td className="rom-text">E</td><td className="rom-text">E̤</td>
                  <td className="rom-text">G</td><td className="rom-text">H</td><td className="rom-text">I</td><td className="rom-text">K</td>
                  <td className="rom-text">L</td><td className="rom-text">M</td><td className="rom-text">N</td><td className="rom-text">Ng</td>
                  <td className="rom-text">O</td><td className="rom-text">O̤</td><td className="rom-text">P</td><td className="rom-text">S</td>
                  <td className="rom-text">T</td><td className="rom-text">U</td><td className="rom-text">Ṳ</td>
                </tr>
                <tr>
                  <th>小寫</th>
                  <td className="rom-text">a</td><td className="rom-text">a̤</td><td className="rom-text">b</td><td className="rom-text">c</td>
                  <td className="rom-text">ch</td><td className="rom-text">d</td><td className="rom-text">e</td><td className="rom-text">e̤</td>
                  <td className="rom-text">g</td><td className="rom-text">h</td><td className="rom-text">i</td><td className="rom-text">k</td>
                  <td className="rom-text">l</td><td className="rom-text">m</td><td className="rom-text">n</td><td className="rom-text">ng</td>
                  <td className="rom-text">o</td><td className="rom-text">o̤</td><td className="rom-text">p</td><td className="rom-text">s</td>
                  <td className="rom-text">t</td><td className="rom-text">u</td><td className="rom-text">Ṳ</td>
                </tr>
              </tbody>
            </table>
          </div>

          <p>
            此外，興化平話字還使用四種變音符號表示聲調，詳見下文<a href="#tones">聲調章節</a>。
          </p>
        </section>

        <hr />

        <section className="about-section">
          <h2>音韻系統</h2>
          <p>
            由於興化平話字創制時間較早，其音韻系統和現代多數方言有相當差距，卻又和它們兼容。
            換言之，只要根據該地方言的音系稍加調整，就可以用興化平話字書寫大多數莆仙語方言。
            以下文章將介紹興化平話字，同時介紹多種莆仙語方言的發音。
          </p>

          <h3>聲母</h3>
          <p>興化平話字共有14個輔音聲母。零聲母沒有標記。各方言之間的讀法較為一致，不同之處於表格下方指出。</p>

          <div className="table-responsive linguistic-table-wrapper">
            <table className="phonology-table">
              <thead>
                <tr>
                  <th>字母</th>
                  <th>國際音標</th>
                  <th>例字</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td className="rom-text">b</td>
                  <td>[p]</td>
                  <td className="han-text">巴米平八筆飛白百馬買房</td>
                </tr>
                <tr>
                  <td className="rom-text">p</td>
                  <td>[pʰ]</td>
                  <td className="han-text">批皮潑迫拍浮潘蜂反範伏</td>
                </tr>
                <tr>
                  <td className="rom-text">m</td>
                  <td>[m]</td>
                  <td className="han-text">馬麻罵毛妹慢明命糜目味</td>
                </tr>
                <tr>
                  <td className="rom-text">d<sup>[1]</sup></td>
                  <td>[t]</td>
                  <td className="han-text">弟敵答知長池程定同榨詐</td>
                </tr>
                <tr>
                  <td className="rom-text">t</td>
                  <td>[tʰ]</td>
                  <td className="han-text">拖頭透讀超撐蟲柱鋤窗餿</td>
                </tr>
                <tr>
                  <td className="rom-text">n<sup>[2]</sup></td>
                  <td>[n]</td>
                  <td className="han-text">泥年奴南娘鑷染忍潤燃肉</td>
                </tr>
                <tr>
                  <td className="rom-text">l</td>
                  <td>[l]</td>
                  <td className="han-text">來羅流龍零林藍六力綠辣</td>
                </tr>
                <tr>
                  <td className="rom-text">c</td>
                  <td>[ts]</td>
                  <td className="han-text">子字錢爭狀主人叔少俞鳥</td>
                </tr>
                <tr>
                  <td className="rom-text">ch</td>
                  <td>[tsʰ]</td>
                  <td className="han-text">差青床稱出冊星象手伸颺</td>
                </tr>
                <tr>
                  <td className="rom-text">s<sup>[3]</sup></td>
                  <td>[ɬ]</td>
                  <td className="han-text">四泅習席師神船上食癢翼</td>
                </tr>
                <tr>
                  <td className="rom-text">g</td>
                  <td>[k]</td>
                  <td className="han-text">加甲舊牙外月猴含指支痣</td>
                </tr>
                <tr>
                  <td className="rom-text">k</td>
                  <td>[kʰ]</td>
                  <td className="han-text">科開口客級騎鉗吸呼齒柿</td>
                </tr>
                <tr>
                  <td className="rom-text">ng</td>
                  <td>[ŋ]</td>
                  <td className="han-text">雅願岩原元研嚴眼硬迎五</td>
                </tr>
                <tr>
                  <td className="rom-text">h</td>
                  <td>[h]</td>
                  <td className="han-text">火好下方耳歲施魚額雨遠</td>
                </tr>
                <tr>
                  <td className="rom-text">(零聲母)</td>
                  <td>∅</td>
                  <td className="han-text">啞衣影圓雲羊阮後紅弧何</td>
                </tr>
              </tbody>
            </table>
          </div>

          <div className="footnotes">
            <p>
              <small>[1] 平話字聖經中以 <span className="rom-text">d</span> 書寫的一些字，如<span className="han-text">入、二、女、內、膩、鬧、納、蹂、日、尿、紐</span>等（主要來源於中古孃母、日母），在一些方言中讀為 [l]。</small>
            </p>
            <p>
              <small>[2] 平話字聖經中以 <span className="rom-text">n</span> 書寫的一些字，如<span className="han-text">林、籃、蓮、卵、爛、欄、嶺、領、量、涼、兩<small>(斤兩)</small></span>，在一些方言中讀為 [l]。</small>
            </p>
            <p>
              <small>[3] <span className="rom-text">s</span> 在多數方言中讀作齦清邊擦音 [ɬ]，而在仙遊縣的鐘山鎮、遊洋鎮、石蒼鄉，莆田北部的莊邊鎮、新縣鎮、大洋鄉及其以西的福清市新厝鎮鳳跡村，則讀成齒清擦音 [θ]。</small>
            </p>
          </div>

          <h3>韻母</h3>
          <p>
            興化平話字共有9個單元音字母，一套韻尾（-ng、-h），能組合成豐富的韻母系統。下表列出各方言點的韻母音值，可選擇要比較的方言點進行查看。表格支援左右捲動，第一欄（韻母）固定不動。
          </p>
          <p>
            音值資料由陳浩淼先生提供。對於各方言點音系的詳細論述可見其論文《莆仙方言语音比较研究》。
          </p>
          <RhymeTable />

          <h3 id="tones">聲調</h3>
          <p>
            興化平話字共有7個聲調，不過根據後代方言的演化，19世紀末的莆田口音應能區別8種不同的單字調。
            若將變調行為也納入考慮，則可以歸納出9種不同的聲調。
          </p>
          <p>
            下表呈現了興化平話字的聲調。由於現代方言的調值差異不大，僅揀選數個方言點用於比較。
          </p>

          <div className="table-responsive">
            <table className="phonology-table">
              <thead>
                <tr>
                  <th>調類</th>
                  <th>調名</th>
                  <th>調號</th>
                  <th>例字</th>
                  <th>莆田</th>
                  <th>江口</th>
                  <th>仙遊</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>1</td>
                  <td>陰平</td>
                  <td className="rom-text">◌</td>
                  <td className="han-text">詩機衣</td>
                  <td>533</td>
                  <td>533</td>
                  <td>544</td>
                </tr>
                <tr>
                  <td>2</td>
                  <td>陽平</td>
                  <td className="rom-text">◌́</td>
                  <td className="han-text">時其移</td>
                  <td>13</td>
                  <td>13</td>
                  <td>24</td>
                </tr>
                <tr>
                  <td>3</td>
                  <td>上聲</td>
                  <td className="rom-text">◌̂</td>
                  <td className="han-text">死己以</td>
                  <td>453</td>
                  <td>453</td>
                  <td>332</td>
                </tr>
                <tr>
                  <td>4</td>
                  <td>陰去</td>
                  <td className="rom-text">◌̍</td>
                  <td className="han-text">四記意</td>
                  <td>42</td>
                  <td>42</td>
                  <td>42</td>
                </tr>
                <tr>
                  <td rowSpan="2">5</td>
                  <td>陽去</td>
                  <td rowSpan="2" className="rom-text">◌̄</td>
                  <td className="han-text">寺義異</td>
                  <td>11</td>
                  <td>11</td>
                  <td>21</td>
                </tr>
                <tr>
                  <td>(陰入白)<sup>[1]</sup></td>
                  <td className="han-text">百冊尺錫索桌潑髮</td>
                  <td>11</td>
                  <td>11</td>
                  <td>21</td>
                </tr>
                <tr>
                  <td>6</td>
                  <td>陰入</td>
                  <td className="rom-text">◌h</td>
                  <td className="han-text">失急一</td>
                  <td>21</td>
                  <td>21</td>
                  <td>2</td>
                </tr>
                <tr>
                  <td rowSpan="2">7</td>
                  <td>陽入</td>
                  <td rowSpan="2" className="rom-text">◌̍h</td>
                  <td className="han-text">習及液</td>
                  <td>4</td>
                  <td>4</td>
                  <td>4</td>
                </tr>
                <tr>
                  <td>(陽入白)<sup>[2]</sup></td>
                  <td className="han-text">白麥石糴落學末月</td>
                  <td>13</td>
                  <td>453</td>
                  <td>24</td>
                </tr>
              </tbody>
            </table>
          </div>

          <div className="footnotes">
            <p>
              <small>[1] 陰入白：指中古聲調為入聲、聲母為清音的一些白讀字。這類字的單字調在19世紀末的莆田話便已與陽去調合流（羅馬字以橫槓表示），於今日方言中亦無例外。不過這類字位於二字詞組的前字時，其變調行為和一般的陽去調字不相同，故將其特別單獨列出。這類字只出現在特定韻母中（待補）。</small>
            </p>
            <p>
              <small>[2] 陽入白：指中古聲調為入聲、聲母為濁塞音或響音的一些白讀字。在19世紀末的莆田話，這類字的寫法和其他陽入字無異（羅馬字以豎線表示，音節尾有 h），但考慮在當今方言中，這類字的韻尾已經消失，並和陽平調合流（部分方言併入上聲），因此有理由認為在平話字創制的年代，這類字是喉塞韻尾較微弱、音節時長更長而不同於一般陽入字的另一類聲調。於少數方言的老派使用者中，此類字讀作高升調，和陽平調的中升/低升調有別。這類字只出現在 ah、aih、a̤h、a̤uh、io̤h、uah、eoh、o̤h、ih、iah、oih 這幾個韻母中，而不會出現在 eh、e̤h、uh、ṳh 中。</small>
            </p>
          </div>

          <h3>連續音變</h3>
          <p>
            莆仙語有豐富的連續音變現象，主要可以分為連續變調和聲母類化兩部分。雖然平話字總是記錄音變前的音節，而使我們難以確認百餘年前連續音變的細節，但為求敘述完整，以下仍依現代莆仙語方言的連續音變規則回推當時可能的音變情況。
          </p>

          <h4>連續變調</h4>
          <p>
            變調指多個音節連讀時，聲調發生變化的語音現象。
          </p>
          <p>
            莆仙語的變調規則複雜。一般來說，詞中的非末音節都會發生變調。下表列出了今日莆田話一般的二字組變調規則（多字組、二字疊字組另有規則）。
          </p>
          <p>
            其中 6A、6B、7A、7B 分別指陰入、陰入白、陽入、陽入白。S1 表示高平調，即和陰平讀法類似但末尾不下降。一些聲調組合有多種變調方式，如「上聲＋陽平」可以讀成「陽平+陽平」或「高平+陽平」、「陽去+陽平」可以讀成「陽去+陽平」或「高平+陽平」等，和詞彙搭配、地域習慣都有關係，以下僅各列出參考資料中最常見的一種。
          </p>

          <div className="table-responsive">
            <table className="tone-sandhi-table">
              <thead>
                <tr>
                  <th className="sticky-header sticky-col diagonal-header">
                    <span className="bottom-left">前</span>
                    <span className="top-right">後</span>
                  </th>
                  <th>1</th>
                  <th>2/7B</th>
                  <th>3</th>
                  <th>4</th>
                  <th>5/6B</th>
                  <th>6A</th>
                  <th>7A</th>
                </tr>
              </thead>
              <tbody>
                <tr><th>1</th><td>5</td><td>5</td><td>5</td><td>5</td><td>2</td><td>2</td><td>5</td></tr>
                <tr><th>2/7B</th><td>5</td><td>5</td><td>5</td><td>S1</td><td>4</td><td>4</td><td>5</td></tr>
                <tr><th>3</th><td>5</td><td>2</td><td>5</td><td>5</td><td>2</td><td>2</td><td>5</td></tr>
                <tr><th>4</th><td>S1</td><td>4</td><td>S1</td><td>S1</td><td>4</td><td>4</td><td>S1</td></tr>
                <tr><th>5</th><td>5</td><td>5</td><td>5</td><td>S1</td><td>4</td><td>4</td><td>5</td></tr>
                <tr><th>6A</th><td>7A</td><td>7A</td><td>7A</td><td>7A</td><td>4<sup>[1]</sup></td><td>4<sup>[1]</sup></td><td>7A</td></tr>
                <tr><th>6B</th><td>S1</td><td>S1</td><td>S1</td><td>S1</td><td>4</td><td>4</td><td>S1</td></tr>
                <tr><th>7A</th><td>6A</td><td>6A</td><td>6A</td><td>7A</td><td>4<sup>[1]</sup></td><td>4<sup>[1]</sup></td><td>6A</td></tr>
              </tbody>
            </table>
          <div className="footnotes">
            <p><small>[1] 這幾個由入聲變成的陰去調仍保留入聲短促、帶有喉塞音的特點。下表中「音變後的讀法」以陽入記。</small></p>
          </div>
          </div>

          <p>
            詞例如下。羅馬字分為兩行，第一行為原始讀音，第二行為音變後的讀法。w 並非平話字字母之一，而是用於表示雙唇濁擦音 [β] 而臨時引入的符號。表中詞語僅作為示例，不保證該詞一定出現於19世紀末的莆田話中。
          </p>

          <div className="table-responsive linguistic-table-wrapper">
            <table className="example-table">
              <thead>
                <tr>
                  <th className="sticky-header sticky-col diagonal-header diagonal-header-wide">
                    <span className="bottom-left">前</span>
                    <span className="top-right">後</span>
                  </th>
                  <th className="sticky-header">1</th>
                  <th className="sticky-header">2</th>
                  <th className="sticky-header">3</th>
                  <th className="sticky-header">4</th>
                  <th className="sticky-header">5</th>
                  <th className="sticky-header">6A</th>
                  <th className="sticky-header">6B</th>
                  <th className="sticky-header">7A</th>
                  <th className="sticky-header">7B</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <th className="sticky-col">1</th>
                  <td><span className="han-text">豬哥</span><br/><span className="rom-text">d<b>ṳ</b>-geo</span><br/><span className="rom-text">d<b>ṳ̄</b>-geo</span></td>
                  <td><span className="han-text">烏塗</span><br/><span className="rom-text"><b>o</b>-tó</span><br/><span className="rom-text"><b>ō</b>-ló</span></td>
                  <td><span className="han-text">批紙</span><br/><span className="rom-text">p<b>a̤</b>-ciô̤</span><br/><span className="rom-text">p<b>ā̤</b>-liô̤</span></td>
                  <td><span className="han-text">興化</span><br/><span className="rom-text">H<b>i</b>ng-hua̍</span><br/><span className="rom-text">H<b>í</b>ng-ngua̍</span></td>
                  <td><span className="han-text">番柿</span><br/><span className="rom-text">hu<b>a</b>ng-kī</span><br/><span className="rom-text">hu<b>á</b>ng-ngī</span></td>
                  <td><span className="han-text">豬角</span><br/><span className="rom-text">d<b>ṳ</b>-gah</span><br/><span className="rom-text">d<b>ṳ́</b>-gah</span></td>
                  <td><span className="han-text">冬節</span><br/><span className="rom-text">d<b>a</b>ng-cā̤</span><br/><span className="rom-text">d<b>á</b>ng-nā̤</span></td>
                  <td><span className="han-text">薰盒</span><br/><span className="rom-text">he<b>o</b>ng-a̍h</span><br/><span className="rom-text">he<b>ō</b>ng-a̍h</span></td>
                  <td><span className="han-text">溪石</span><br/><span className="rom-text">k<b>a̤</b>-sa̤u̍h</span><br/><span className="rom-text">k<b>ā̤</b>-la̤u̍h</span></td>
                </tr>
                <tr>
                  <th className="sticky-col">2</th>
                  <td><span className="han-text">蝦蛄</span><br/><span className="rom-text">h<b>ó̤</b>-go</span><br/><span className="rom-text">h<b>ō̤</b>-o</span></td>
                  <td><span className="han-text">行棋</span><br/><span className="rom-text">gi<b>á</b>ⁿ-gí</span><br/><span className="rom-text">gi<b>ā</b>ⁿ-gí</span></td>
                  <td><span className="han-text">姨媽</span><br/><span className="rom-text"><b>í</b>-mâ</span><br/><span className="rom-text"><b>ī</b>-mâ</span></td>
                  <td><span className="han-text">名姓</span><br/><span className="rom-text">mi<b>á</b>-sa̍ⁿ</span><br/><span className="rom-text">mi<b>a</b>-na̍</span></td>
                  <td><span className="han-text">柴料</span><br/><span className="rom-text">ch<b>ó̤</b>-lā̤u</span><br/><span className="rom-text">ch<b>o̤̍</b>-lā̤u</span></td>
                  <td><span className="han-text">牛軛</span><br/><span className="rom-text">g<b>ú</b>-eh</span><br/><span className="rom-text">g<b>u̍</b>-eh</span></td>
                  <td><span className="han-text">松柏</span><br/><span className="rom-text">s<b>é̤</b>ng-bā</span><br/><span className="rom-text">se̤̍ng-mā</span></td>
                  <td><span className="han-text">羊肉</span><br/><span className="rom-text"><b>á̤</b>uⁿ-ne̤̍h</span><br/><span className="rom-text"><b>ā̤</b>uⁿ-ne̤̍h</span></td>
                  <td><span className="han-text">茶箬</span><br/><span className="rom-text">d<b>ó̤</b>-na̤u̍h</span><br/><span className="rom-text">d<b>ō̤</b>-na̤u̍h</span></td>
                </tr>
                <tr>
                  <th className="sticky-col">3</th>
                  <td><span className="han-text">火烌</span><br/><span className="rom-text">h<b>ô̤</b>-hu</span><br/><span className="rom-text">h<b>ō̤</b>-u</span></td>
                  <td><span className="han-text">飲糜</span><br/><span className="rom-text"><b>â</b>ng-mói</span><br/><span className="rom-text"><b>á</b>ng-mói</span></td>
                  <td><span className="han-text">短䘼</span><br/><span className="rom-text">d<b>ê̤</b>-ôiⁿ</span><br/><span className="rom-text">d<b>ē̤</b>-ôiⁿ</span></td>
                  <td><span className="han-text">蠓帳</span><br/><span className="rom-text">m<b>â</b>ng-da̤̍uⁿ</span><br/><span className="rom-text">m<b>ā</b>ng-na̤̍u</span></td>
                  <td><span className="han-text">手運</span><br/><span className="rom-text">chi<b>û</b>-eōng</span><br/><span className="rom-text">chi<b>ú</b>-eōng</span></td>
                  <td><span className="han-text">尾叔</span><br/><span className="rom-text">b<b>ô</b>i-ce̤h</span><br/><span className="rom-text">b<b>ó</b>i-le̤h</span></td>
                  <td><span className="han-text">碗缺</span><br/><span className="rom-text">u<b>â</b>ⁿ-kī</span><br/><span className="rom-text">u<b>á</b>ⁿ-kī</span></td>
                  <td><span className="han-text">煮食</span><br/><span className="rom-text">c<b>ṳ̂</b>-sia̍h</span><br/><span className="rom-text">c<b>ṳ̄</b>-lia̍h</span></td>
                  <td>-</td>
                </tr>
                <tr>
                  <th className="sticky-col">4</th>
                  <td><span className="han-text">樹奶</span><br/><span className="rom-text">chi<b>u̍</b>-neng</span><br/><span className="rom-text">chi<b>u</b>-neng</span></td>
                  <td><span className="han-text">敬虔</span><br/><span className="rom-text">g<b>i̍</b>ng-géng</span><br/><span className="rom-text">g<b>i̍</b>ng-géng</span></td>
                  <td><span className="han-text">喙䫌</span><br/><span className="rom-text">ch<b>u</b>i̍-pâ̤</span><br/><span className="rom-text">ch<b>u</b>i-wâ̤</span></td>
                  <td><span className="han-text">拜四</span><br/><span className="rom-text">b<b>a̍</b>i-si̍</span><br/><span className="rom-text">b<b>a</b>i-li̍</span></td>
                  <td><span className="han-text">鼻路</span><br/><span className="rom-text">p<b>i̍</b>-lō</span><br/><span className="rom-text">p<b>i̍</b>-lō</span></td>
                  <td><span className="han-text">四角</span><br/><span className="rom-text">s<b>i̍</b>-gah</span><br/><span className="rom-text">s<b>i̍</b>-gah</span></td>
                  <td><span className="han-text">送節</span><br/><span className="rom-text">s<b>a̍</b>ng-cā̤</span><br/><span className="rom-text">s<b>a</b>ng-cā̤</span></td>
                  <td><span className="han-text">透日</span><br/><span className="rom-text">t<b>a̍</b>u-di̍h</span><br/><span className="rom-text">t<b>a</b>u-li̍h</span></td>
                  <td><span className="han-text">褲襪</span><br/><span className="rom-text">k<b>o̍</b>-bo̍ih</span><br/><span className="rom-text">k<b>o̍</b>-bo̍ih</span></td>
                </tr>
                <tr>
                  <th className="sticky-col">5</th>
                  <td><span className="han-text">伓通</span><br/><span className="rom-text"><b>n̄</b>g-tang</span><br/><span className="rom-text"><b>n̄</b>g-nang</span></td>
                  <td><span className="han-text">舊年</span><br/><span className="rom-text">g<b>ū</b>-níng</span><br/><span className="rom-text">g<b>ū</b>-níng</span></td>
                  <td><span className="han-text">啞口</span><br/><span className="rom-text"><b>ō̤</b>-kâu</span><br/><span className="rom-text"><b>ō̤</b>-kâu</span></td>
                  <td><span className="han-text">代誌</span><br/><span className="rom-text">d<b>ā</b>i-ci̍</span><br/><span className="rom-text">d<b>a</b>i-li̍</span></td>
                  <td><span className="han-text">利便</span><br/><span className="rom-text">l<b>ī</b>-bēng</span><br/><span className="rom-text">l<b>i̍</b>-wēng</span></td>
                  <td><span className="han-text">後角</span><br/><span className="rom-text"><b>ā</b>u-gah</span><br/><span className="rom-text"><b>a̍</b>u-gah</span></td>
                  <td><span className="han-text">大伯</span><br/><span className="rom-text">du<b>ā</b>-bā</span><br/><span className="rom-text">du<b>a̍</b>-wā</span></td>
                  <td><span className="han-text">靜寂</span><br/><span className="rom-text">c<b>ī</b>ng-ci̍h</span><br/><span className="rom-text">c<b>ī</b>ng-ci̍h</span></td>
                  <td><span className="han-text">銃藥</span><br/><span className="rom-text">ch<b>ē̤</b>ng-a̤u̍h</span><br/><span className="rom-text">ch<b>ē̤</b>ng-nga̤u̍h</span></td>
                </tr>
                <tr>
                  <th className="sticky-col">6A</th>
                  <td><span className="han-text">竹篙</span><br/><span className="rom-text">d<b>e̤</b>h-geo</span><br/><span className="rom-text">d<b>e̤̍</b>h-geo</span></td>
                  <td><span className="han-text">百靈</span><br/><span className="rom-text">b<b>e</b>h-léng</span><br/><span className="rom-text">b<b>e̍</b>h-léng</span></td>
                  <td><span className="han-text">沃水</span><br/><span className="rom-text"><b>o̤</b>h-cûi</span><br/><span className="rom-text"><b>o̤̍</b>h-cûi</span></td>
                  <td><span className="han-text">出葬</span><br/><span className="rom-text">che<b>o</b>h-co̤̍ng</span><br/><span className="rom-text">che<b>o̍</b>h-co̤̍ng</span></td>
                  <td><span className="han-text">捌字</span><br/><span className="rom-text">b<b>e</b>h-cī</span><br/><span className="rom-text">b<b>e̍</b>h-cī</span></td>
                  <td><span className="han-text">粟殼</span><br/><span className="rom-text">ch<b>o̤</b>h-kah</span><br/><span className="rom-text">ch<b>o̤̍</b>h-kah</span></td>
                  <td>-</td>
                  <td><span className="han-text">竹笠</span><br/><span className="rom-text">d<b>e̤</b>h-lia̍h</span><br/><span className="rom-text">d<b>e̤̍</b>h-lia̍h</span></td>
                  <td><span className="han-text">竹箬</span><br/><span className="rom-text">d<b>e̤</b>h-na̤u̍h</span><br/><span className="rom-text">d<b>e̤̍</b>h-na̤u̍h</span></td>
                </tr>
                <tr>
                  <th className="sticky-col">6B</th>
                  <td><span className="han-text">伯公</span><br/><span className="rom-text">b<b>ā</b>-go̤ng</span><br/><span className="rom-text">b<b>a</b>-o̤ng</span></td>
                  <td><span className="han-text">隔年</span><br/><span className="rom-text">g<b>ā</b>-níng</span><br/><span className="rom-text">g<b>a</b>-níng</span></td>
                  <td><span className="han-text">甲子</span><br/><span className="rom-text">g<b>ō̤</b>-cî</span><br/><span className="rom-text">g<b>o̤</b>-lî</span></td>
                  <td><span className="han-text">缺喙</span><br/><span className="rom-text">k<b>ī</b>-chu̍i</span><br/><span className="rom-text">k<b>i</b>-lu̍i</span></td>
                  <td><span className="han-text">惜命</span><br/><span className="rom-text">s<b>ā̤</b>u-miā</span><br/><span className="rom-text">s<b>a̤̍</b>u-miā</span></td>
                  <td><span className="han-text">拍折</span><br/><span className="rom-text">p<b>ā</b>-ceh</span><br/><span className="rom-text">p<b>a̍</b>-sih</span></td>
                  <td><span className="han-text">隔壁</span><br/><span className="rom-text">g<b>ā</b>-biā</span><br/><span className="rom-text">g<b>a̍</b>-wiā</span></td>
                  <td><span className="han-text">百日</span><br/><span className="rom-text">b<b>ā</b>-di̍h</span><br/><span className="rom-text">b<b>a</b>-li̍h</span></td>
                  <td><span className="han-text">拍石</span><br/><span className="rom-text">p<b>ā</b>-sa̤u̍h</span><br/><span className="rom-text">p<b>a</b>-sa̤u̍h</span></td>
                </tr>
                <tr>
                  <th className="sticky-col">7A</th>
                  <td><span className="han-text">曝衫</span><br/><span className="rom-text">p<b>o̤̍</b>h-so̤ⁿ</span><br/><span className="rom-text">p<b>o̤</b>h-so̤ⁿ</span></td>
                  <td><span className="han-text">日頭</span><br/><span className="rom-text">d<b>i̍</b>h-táu</span><br/><span className="rom-text">d<b>i</b>h-táu</span></td>
                  <td><span className="han-text">力草</span><br/><span className="rom-text">l<b>i̍</b>h-châu</span><br/><span className="rom-text">l<b>i</b>h-châu</span></td>
                  <td><span className="han-text">目鏡</span><br/><span className="rom-text">m<b>a̍</b>h-gia̍ⁿ</span><br/><span className="rom-text">m<b>a̍</b>h-gia̍ⁿ</span></td>
                  <td><span className="han-text">額份</span><br/><span className="rom-text">g<b>e̍</b>h-heōng</span><br/><span className="rom-text">g<b>e̍</b>h-heōng</span></td>
                  <td><span className="han-text">蠟燭</span><br/><span className="rom-text">l<b>o̤̍</b>h-co̤h</span><br/><span className="rom-text">l<b>o̤̍</b>h-co̤h</span></td>
                  <td><span className="han-text">讀冊</span><br/><span className="rom-text">t<b>a̍</b>h-chā</span><br/><span className="rom-text">t<b>a̍</b>h-chā</span></td>
                  <td><span className="han-text">虼蚻</span><br/><span className="rom-text">g<b>o̤̍</b>h-sua̍h</span><br/><span className="rom-text">g<b>o̤</b>h-sua̍h</span></td>
                  <td><span className="han-text">目液</span><br/><span className="rom-text">m<b>a̍</b>h-sa̤u̍h</span><br/><span className="rom-text">m<b>a</b>h-sa̤u̍h</span></td>
                </tr>
                <tr>
                  <th className="sticky-col">7B</th>
                  <td><span className="han-text">著災</span><br/><span className="rom-text">da̤<b>u̍</b>h-ce̤</span><br/><span className="rom-text">d<b>ā̤</b>u-le̤</span></td>
                  <td><span className="han-text">辣頭</span><br/><span className="rom-text">lu<b>a̍</b>h-táu</span><br/><span className="rom-text">lu<b>ā</b>-láu</span></td>
                  <td><span className="han-text">白殕</span><br/><span className="rom-text">b<b>a̍</b>h-pû</span><br/><span className="rom-text">b<b>ā</b>-pû</span></td>
                  <td><span className="han-text">物配</span><br/><span className="rom-text">m<b>o̍</b>ih-po̍i</span><br/><span className="rom-text">m<b>o</b>i-wo̍i</span></td>
                  <td><span className="han-text">石卵</span><br/><span className="rom-text">sa̤<b>u̍</b>h-nē̤</span><br/><span className="rom-text">s<b>a̤̍</b>u-nē̤</span></td>
                  <td><span className="han-text">藥粕</span><br/><span className="rom-text"><b>a̤</b>u̍h-peō</span><br/><span className="rom-text"><b>a̤̍</b>u-peō</span></td>
                  <td><span className="han-text">石級</span><br/><span className="rom-text">sa̤<b>u̍</b>h-keh</span><br/><span className="rom-text">s<b>a̤̍</b>u-keh</span></td>
                  <td><span className="han-text">食食</span><br/><span className="rom-text">si<b>a̍</b>h-si̍h</span><br/><span className="rom-text">si<b>ā</b>-li̍h</span></td>
                  <td><span className="han-text">篾蓆</span><br/><span className="rom-text">b<b>i̍</b>h-cha̤u̍h</span><br/><span className="rom-text">b<b>ī</b>-la̤u̍h</span></td>
                </tr>
              </tbody>
            </table>
          </div>

          <h4>聲母類化</h4>
          <p>
            聲母類化是一個詞內後字的聲母，受到前後音節或韻母類型而發生改變的現象。
          </p>
          <p>
            莆仙話各方言的的類化規則大同小異，大致可以整理為以下。標記「<sup>鼻</sup>」者表示該後字音節為鼻化韻。w 並非平話字字母之一，而是用於表示雙唇濁擦音 [β] 而臨時引入的符號。
          </p>

          <div className="table-responsive linguistic-table-wrapper">
            <table className="example-table">
              <thead>
                <tr>
                  <th className="diagonal-header">
                    <span className="bottom-left">後</span>
                    <span className="top-right">前</span>
                  </th>
                  <th>元音尾</th>
                  <th>-ng 尾</th>
                  <th>-h 尾</th>
                  <th>鼻化韻</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>b、p</td>
                  <td>w</td>
                  <td>m</td>
                  <td rowSpan="6">不變</td>
                  <td>m</td>
                </tr>
                <tr>
                  <td>b<sup>鼻</sup>、p<sup>鼻</sup>、m</td>
                  <td>m</td>
                  <td>m</td>
                  <td>m</td>
                </tr>
                <tr>
                  <td>d、t、l、c、ch、s</td>
                  <td>l</td>
                  <td>n</td>
                  <td>n</td>
                </tr>
                <tr>
                  <td>d<sup>鼻</sup>、t<sup>鼻</sup>、c<sup>鼻</sup>、ch<sup>鼻</sup>、s<sup>鼻</sup>、n</td>
                  <td>n</td>
                  <td>n</td>
                  <td>n</td>
                </tr>
                <tr>
                  <td>g、k、h、Ø</td>
                  <td>Ø</td>
                  <td>ng</td>
                  <td>Ø</td>
                </tr>
                <tr>
                  <td>ng</td>
                  <td>ng</td>
                  <td>ng</td>
                  <td>ng</td>
                </tr>
              </tbody>
            </table>
          </div>

          <p>
            今日莆田城區口音的鼻化韻已變為口元音，因此對應的鼻化韻行列不再適用；莆田北部山區、沿海部分鄉鎮以及仙遊全境則普遍仍保有鼻化韻。莆田北部山區的類化比上表更為激進，除了前字入聲韻時後字聲母不變、前字陰聲韻時後字聲母 m、n、l、ng 不變、前字 -ng 尾時後字聲母依調音部位變為 m、n、ng 以外，其他情況都變為零聲母。
          </p>
          <p>
            詞例如下。羅馬字分為兩行，第一行為原始讀音，第二行為音變後的讀法。
          </p>

          <div className="table-responsive linguistic-table-wrapper">
            <table className="example-table">
              <thead>
                <tr>
                  <th colSpan="2" className="diagonal-header">
                    <span className="bottom-left">後</span>
                    <span className="top-right">前</span>
                  </th>
                  <th>元音尾</th>
                  <th>-ng 尾</th>
                  <th>-h 尾</th>
                  <th>鼻化韻</th>
                </tr>
              </thead>
              <tbody>
                {/* Group b */}
                <tr>
                  <td rowSpan="2">b</td>
                  <td>非鼻化</td>
                  <td><span className="han-text">後壁</span><br/><span className="rom-text">āu-<b>b</b>iā</span><br/><span className="rom-text">a̍u-<b>w</b>iā</span></td>
                  <td rowSpan="2"><span className="han-text">新婦</span><br/><span className="rom-text">sing-<b>b</b>ū</span><br/><span className="rom-text">síng-<b>m</b>ū</span></td>
                  <td rowSpan="2"><span className="han-text">目眉</span><br/><span className="rom-text">ma̍h-<b>b</b>ái</span><br/><span className="rom-text">mah-<b>b</b>ái</span></td>
                  <td rowSpan="2"><span className="han-text">洋筆</span><br/><span className="rom-text">á̤uⁿ-<b>b</b>ih</span><br/><span className="rom-text">a̤̍uⁿ-<b>m</b>ih</span></td>
                </tr>
                <tr>
                  <td>鼻化韻</td>
                  <td><span className="han-text">戲棚</span><br/><span className="rom-text">hi̍-<b>b</b>áⁿ</span><br/><span className="rom-text">hi̍-<b>m</b>á</span></td>
                </tr>

                {/* Group p */}
                <tr>
                  <td rowSpan="2">p</td>
                  <td>非鼻化</td>
                  <td><span className="han-text">廝拍</span><br/><span className="rom-text">seo-<b>p</b>ā</span><br/><span className="rom-text">seó-<b>w</b>ā</span></td>
                  <td rowSpan="2"><span className="han-text">放炮</span><br/><span className="rom-text">ba̍ng-<b>p</b>a̍u</span><br/><span className="rom-text">bang-<b>m</b>a̍u</span></td>
                  <td rowSpan="2"><span className="han-text">結疕</span><br/><span className="rom-text">geh-<b>p</b>î</span><br/><span className="rom-text">ge̍h-<b>p</b>î</span></td>
                  <td rowSpan="2"><span className="han-text">磚坯</span><br/><span className="rom-text">coiⁿ-<b>p</b>oi</span><br/><span className="rom-text">cōiⁿ-<b>m</b>oi</span></td>
                </tr>
                <tr>
                  <td>鼻化韻</td>
                  <td><span className="han-text">尻骿</span><br/><span className="rom-text">go̤ⁿ-<b>p</b>iaⁿ</span><br/><span className="rom-text">go̤ⁿ-<b>m</b>ia</span></td>
                </tr>

                {/* Group m */}
                <tr>
                  <td colSpan="2">m</td>
                  <td><span className="han-text">索麵</span><br/><span className="rom-text">seō-<b>m</b>īng</span><br/><span className="rom-text">seo̍-<b>m</b>īng</span></td>
                  <td><span className="han-text">凊糜</span><br/><span className="rom-text">chi̍ng-<b>m</b>á</span><br/><span className="rom-text">chi̍ng-<b>m</b>á</span></td>
                  <td><span className="han-text">惡物</span><br/><span className="rom-text">o̤h-<b>m</b>o̍ih</span><br/><span className="rom-text">o̤̍h-<b>m</b>o̍ih</span></td>
                  <td><span className="han-text">半暝</span><br/><span className="rom-text">bua̍ⁿ-<b>m</b>á</span><br/><span className="rom-text">bua̍ⁿ-<b>m</b>á</span></td>
                </tr>

                {/* Group d */}
                <tr>
                  <td rowSpan="2">d</td>
                  <td>非鼻化</td>
                  <td><span className="han-text">布袋</span><br/><span className="rom-text">bo̍-<b>d</b>ē̤</span><br/><span className="rom-text">bo̍-<b>l</b>ē̤</span></td>
                  <td rowSpan="2"><span className="han-text">年兜</span><br/><span className="rom-text">níng-<b>d</b>au</span><br/><span className="rom-text">nīng-<b>n</b>au</span></td>
                  <td rowSpan="2"><span className="han-text">腹肚</span><br/><span className="rom-text">bah-<b>d</b>ô</span><br/><span className="rom-text">ba̍h-<b>d</b>ô</span></td>
                  <td rowSpan="2"><span className="han-text">棚頂</span><br/><span className="rom-text">báⁿ-<b>d</b>êng</span><br/><span className="rom-text">bāⁿ-<b>n</b>êng</span></td>
                </tr>
                <tr>
                  <td>鼻化韻</td>
                  <td><span className="han-text">藥單</span><br/><span className="rom-text">a̤u̍h-<b>d</b>uaⁿ</span><br/><span className="rom-text">a̤u̍h-<b>n</b>ua</span></td>
                </tr>

                {/* Group t */}
                <tr>
                  <td rowSpan="2">t</td>
                  <td>非鼻化</td>
                  <td><span className="han-text">事體</span><br/><span className="rom-text">seō-<b>t</b>â̤</span><br/><span className="rom-text">seō-<b>l</b>â̤</span></td>
                  <td rowSpan="2"><span className="han-text">田塗</span><br/><span className="rom-text">chéng-<b>t</b>ó</span><br/><span className="rom-text">chēng-<b>n</b>ó</span></td>
                  <td rowSpan="2"><span className="han-text">賊頭</span><br/><span className="rom-text">che̍h-<b>t</b>áu</span><br/><span className="rom-text">cheh-<b>t</b>áu</span></td>
                  <td rowSpan="2"><span className="han-text">性頭</span><br/><span className="rom-text">sa̍ⁿ-<b>t</b>áu</span><br/><span className="rom-text">sa̍ⁿ-<b>n</b>áu</span></td>
                </tr>
                <tr>
                  <td>鼻化韻</td>
                  <td><span className="han-text">大廳</span><br/><span className="rom-text">duā-<b>t</b>iaⁿ</span><br/><span className="rom-text">duā-<b>n</b>ia</span></td>
                </tr>

                {/* Group n */}
                <tr>
                  <td colSpan="2">n</td>
                  <td><span className="han-text">茶箬</span><br/><span className="rom-text">dó̤-<b>n</b>á̤u</span><br/><span className="rom-text">dō̤-<b>n</b>á̤u</span></td>
                  <td><span className="han-text">嬸娘</span><br/><span className="rom-text">sîng-<b>n</b>á̤u</span><br/><span className="rom-text">síng-<b>n</b>á̤u</span></td>
                  <td><span className="han-text">惡人</span><br/><span className="rom-text">o̤h-<b>n</b>áng</span><br/><span className="rom-text">o̤̍h-<b>n</b>áng</span></td>
                  <td><span className="han-text">衫領</span><br/><span className="rom-text">so̤ⁿ-<b>n</b>iâ</span><br/><span className="rom-text">sō̤ⁿ-<b>n</b>iâ</span></td>
                </tr>

                {/* Group l */}
                <tr>
                  <td colSpan="2">l</td>
                  <td><span className="han-text">尾梨</span><br/><span className="rom-text">bôi-<b>l</b>í</span><br/><span className="rom-text">bói-<b>l</b>í</span></td>
                  <td><span className="han-text">王梨</span><br/><span className="rom-text">ó̤ng-<b>l</b>ái</span><br/><span className="rom-text">ō̤ng-<b>n</b>ái</span></td>
                  <td><span className="han-text">出納</span><br/><span className="rom-text">cheoh-<b>l</b>a̍h</span><br/><span className="rom-text">cheo̍h-<b>l</b>a̍h</span></td>
                  <td><span className="han-text">算零</span><br/><span className="rom-text">sua̍ⁿ-<b>l</b>éng</span><br/><span className="rom-text">sua̍ⁿ-<b>n</b>éng</span></td>
                </tr>

                {/* Group c */}
                <tr>
                  <td rowSpan="2">c</td>
                  <td>非鼻化</td>
                  <td><span className="han-text">利錢</span><br/><span className="rom-text">li̍-<b>c</b>íng</span><br/><span className="rom-text">li̍-<b>l</b>íng</span></td>
                  <td rowSpan="2"><span className="han-text">針黹</span><br/><span className="rom-text">ciâng-<b>c</b>î</span><br/><span className="rom-text">ciāng-<b>n</b>î</span></td>
                  <td rowSpan="2"><span className="han-text">熨枕</span><br/><span className="rom-text">eoh-<b>c</b>îng</span><br/><span className="rom-text">eo̍h-<b>c</b>îng</span></td>
                  <td rowSpan="2"><span className="han-text">鼎灶</span><br/><span className="rom-text">diâⁿ-<b>c</b>a̍u</span><br/><span className="rom-text">diāⁿ-<b>n</b>a̍u</span></td>
                </tr>
                <tr>
                  <td>鼻化韻</td>
                  <td><span className="han-text">豆漿</span><br/><span className="rom-text">dāu-<b>c</b>a̤uⁿ</span><br/><span className="rom-text">dāu-<b>n</b>a̤uⁿ</span></td>
                </tr>

                {/* Group ch */}
                <tr>
                  <td rowSpan="2">ch</td>
                  <td>非鼻化</td>
                  <td><span className="han-text">駛車</span><br/><span className="rom-text">sâi-<b>ch</b>ia</span><br/><span className="rom-text">sāi-<b>l</b>ia</span></td>
                  <td rowSpan="2"><span className="han-text">眩車</span><br/><span className="rom-text">hṳ́ng-<b>ch</b>ia</span><br/><span className="rom-text">hṳ̄ng-<b>n</b>ia</span></td>
                  <td rowSpan="2"><span className="han-text">出喙</span><br/><span className="rom-text">cheoh-<b>ch</b>u̍i</span><br/><span className="rom-text">cheo̍h-<b>ch</b>u̍i</span></td>
                  <td rowSpan="2"><span className="han-text">尻川</span><br/><span className="rom-text">go̤ⁿ-<b>ch</b>oiⁿ</span><br/><span className="rom-text">gō̤ⁿ-<b>n</b>oiⁿ</span></td>
                </tr>
                <tr>
                  <td>鼻化韻</td>
                  <td><span className="han-text">磚厝</span><br/><span className="rom-text">coiⁿ-<b>ch</b>o̍</span><br/><span className="rom-text">coiⁿ-<b>n</b>o̍</span></td>
                </tr>

                {/* Group s */}
                <tr>
                  <td rowSpan="2">s</td>
                  <td>非鼻化</td>
                  <td><span className="han-text">對時</span><br/><span className="rom-text">du̍i-<b>s</b>í</span><br/><span className="rom-text">du̍i-<b>l</b>í</span></td>
                  <td rowSpan="2"><span className="han-text">總數</span><br/><span className="rom-text">cô̤ng-<b>s</b>a̤̍u</span><br/><span className="rom-text">cō̤ng-<b>n</b>a̤̍u</span></td>
                  <td rowSpan="2"><span className="han-text">虼蚻</span><br/><span className="rom-text">go̤̍h-<b>s</b>ua̍h</span><br/><span className="rom-text">go̤h-<b>s</b>ua̍h</span></td>
                  <td rowSpan="2"><span className="han-text">兄嫂</span><br/><span className="rom-text">hiaⁿ-<b>s</b>eô</span><br/><span className="rom-text">hiāⁿ-<b>n</b>eô</span></td>
                </tr>
                <tr>
                  <td>鼻化韻</td>
                  <td><span className="han-text">收山</span><br/><span className="rom-text">siu-<b>s</b>uaⁿ</span><br/><span className="rom-text">siu-<b>n</b>ua</span></td>
                </tr>

                {/* Group g */}
                <tr>
                  <td colSpan="2">g</td>
                  <td><span className="han-text">雞角</span><br/><span className="rom-text">ga̤-<b>g</b>ah</span><br/><span className="rom-text">gá̤-ah</span></td>
                  <td><span className="han-text">凊汗</span><br/><span className="rom-text">chi̍ng-<b>g</b>uā</span><br/><span className="rom-text">chi̍ng-<b>ng</b>uā</span></td>
                  <td><span className="han-text">墨膏</span><br/><span className="rom-text">ba̍h-<b>g</b>eo</span><br/><span className="rom-text">bah-<b>g</b>eo</span></td>
                  <td><span className="han-text">倩工</span><br/><span className="rom-text">chia̍ⁿ-<b>g</b>ang</span><br/><span className="rom-text">chiaⁿ-ang</span></td>
                </tr>

                {/* Group k */}
                <tr>
                  <td colSpan="2">k</td>
                  <td><span className="han-text">鼻空</span><br/><span className="rom-text">pi̍-<b>k</b>ang</span><br/><span className="rom-text">pi-ang</span></td>
                  <td><span className="han-text">胸坎</span><br/><span className="rom-text">ho̤ng-<b>k</b>âng</span><br/><span className="rom-text">hō̤ng-<b>ng</b>âng</span></td>
                  <td><span className="han-text">出虹</span><br/><span className="rom-text">cheoh-<b>k</b>ō̤ng</span><br/><span className="rom-text">cheo̍h-<b>k</b>ō̤ng</span></td>
                  <td><span className="han-text">鼎篋</span><br/><span className="rom-text">diâⁿ-<b>k</b>ā̤</span><br/><span className="rom-text">diáⁿ-ā̤</span></td>
                </tr>

                {/* Group h */}
                <tr>
                  <td colSpan="2">h</td>
                  <td><span className="han-text">落雨</span><br/><span className="rom-text">leo̍h-<b>h</b>ō</span><br/><span className="rom-text">leo̍-ō</span></td>
                  <td><span className="han-text">蟲蟻</span><br/><span className="rom-text">táng-<b>h</b>iō̤</span><br/><span className="rom-text">ta̍ng-<b>ng</b>iō̤</span></td>
                  <td><span className="han-text">粟核</span><br/><span className="rom-text">cho̤h-<b>h</b>eo̍h</span><br/><span className="rom-text">cho̤̍h-<b>h</b>eo̍h</span></td>
                  <td><span className="han-text">歡喜</span><br/><span className="rom-text">huaⁿ-<b>h</b>î</span><br/><span className="rom-text">huāⁿ-î</span></td>
                </tr>

                {/* Group ng */}
                <tr>
                  <td colSpan="2">ng</td>
                  <td><span className="han-text">預言</span><br/><span className="rom-text">ṳ̄-<b>ng</b>é̤ng</span><br/><span className="rom-text">ṳ̄-<b>ng</b>é̤ng</span></td>
                  <td><span className="han-text">龍眼</span><br/><span className="rom-text">lé̤ng-<b>ng</b>â̤</span><br/><span className="rom-text">lē̤ng-<b>ng</b>â̤</span></td>
                  <td><span className="han-text">十五</span><br/><span className="rom-text">se̍h-<b>ng</b>ō</span><br/><span className="rom-text">se̍h-<b>ng</b>ō</span></td>
                  <td><span className="han-text">捲蔫</span><br/><span className="rom-text">gôiⁿ-<b>ng</b>eng</span><br/><span className="rom-text">gōiⁿ-<b>ng</b>eng</span></td>
                </tr>

                {/* Group Ø */}
                <tr>
                  <td colSpan="2">Ø</td>
                  <td><span className="han-text">亞鉛</span><br/><span className="rom-text">a̍-é̤ng</span><br/><span className="rom-text">a̍-é̤ng</span></td>
                  <td><span className="han-text">靈位</span><br/><span className="rom-text">léng-ūi</span><br/><span className="rom-text">le̍ng-<b>ng</b>ūi</span></td>
                  <td><span className="han-text">八音</span><br/><span className="rom-text">bah-ing</span><br/><span className="rom-text">ba̍h-ing</span></td>
                  <td><span className="han-text">聽話</span><br/><span className="rom-text">tiaⁿ-uā</span><br/><span className="rom-text">tiáⁿ-uā</span></td>
                </tr>
              </tbody>
            </table>
          </div>
          <p>
            聖經中也直接記錄了一些類化後的形式，如將「柏膠」寫成 bā-au、「葡萄」寫成 bú-leó、「衣裳」寫成 i-ná̤u 等，足以證明19世紀末就有類化現象存在。
          </p>

        </section>
      </div>
    </div>
  );
}

export default AboutLanguage;
