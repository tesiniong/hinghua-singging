import React from 'react';
import './AboutLanguage.css';

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
            惟興化平話字未曾在教會以外大範圍流行，自20世紀中期便逐漸淡出世人視野，今日莆仙地區的信徒亦不再使用。
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
          
          <div className="table-responsive">
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
                  <td className="rom-text">(零聲母) ∅</td>
                  <td>-</td>
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
              <small>[3] <span className="rom-text">s</span> 在多數方言中讀作邊擦音 [ɬ]，而在仙遊縣的鐘山鎮、遊洋鎮、石蒼鄉，莆田北部的莊邊鎮、新縣鎮、大洋鄉及其以西的福清市新厝鎮鳳跡村，則讀成齒清擦音 [θ]。</small>
            </p>
          </div>

          <h3>韻母</h3>
          <p>🚧 修訂中</p>

          <h3 id="tones">聲調</h3>
          <p>🚧 修訂中</p>

          <h3>連續音變</h3>
          <p>🚧 修訂中</p>
        </section>
      </div>
    </div>
  );
}

export default AboutLanguage;