# 授權說明 Licensing Notice

本專案由不同授權的成分組成，請依成分分別適用。
This project is made of components under different licenses. Apply them per component.

| 成分 Component | 授權 License |
|---|---|
| 程式碼（`website/src/`、`scripts/`、設定檔）Source code | [MIT](LICENSE) |
| 經文轉寫與衍生資料 Transcribed text & derived data | CC BY 4.0 |
| 原書掃描影像 Scanned page images | 見下方 See below |
| 內建字型 Bundled fonts | SIL OFL 1.1 / Bitstream Vera |

---

## 經文轉寫與衍生資料 Transcribed Text & Derived Data

適用於 `data/` 目錄下的文本與 JSON、以及 `website/public/` 中由它們產生的資料檔
（`bible_data.json`、`romToHanDict.json`、`homophoneData.json`、`bookList.json` 等）。

Applies to the texts and JSON under `data/`, and the data files generated from them
in `website/public/`.

**授權 License**: [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/)

1912 年出版的原始經文本身早已進入公有領域。本專案主張權利的範圍僅限於轉寫、
校對、漢字對照、切分標記等編輯性成果；請以「興化語聖經數位化專案」及貢獻者姓名標示出處。

The 1912 source text is long in the public domain. What this project claims is only the
editorial work -- transcription, proofreading, Han-character correspondence, tokenization.
Attribute to the Hinghua Bible Digital Project and its contributors.

選擇 CC BY 而非 CC BY-SA，是為了讓這批語料能無障礙地用於訓練模型等下游用途；
相同條款（share-alike）在這類場景會造成授權範圍的爭議。

CC BY rather than CC BY-SA, so the corpus can be used downstream -- for training models,
among other things -- without share-alike raising questions about the scope of the license.

## 原書掃描影像 Scanned Page Images

`website/public/images/` 中的 1485 張影像來自下列典藏。原書出版於 1912 年，
著作權保護期間已屆滿；但掃描影像的使用條款依各典藏機構規定，再散布前請自行確認。

The 1485 images in `website/public/images/` come from the archives below. The 1912 work
itself is out of copyright; terms for the scans are set by the holding institutions, so
check with them before redistributing.

- [臺灣大學圖書館數位典藏 NTU Library Digital Archives](https://dl.lib.ntu.edu.tw/s/westrare/item/129333)
- [HathiTrust Digital Library](https://hdl.handle.net/2027/uc1.31822025315045)

## 內建字型 Bundled Fonts

`website/src/assets/fonts/` 隨附下列字型。各字型的完整授權條文內嵌於字型檔本身的
name table（nameID 13）。

The fonts below ship in `website/src/assets/fonts/`. Each font file carries its full
license text internally, in its name table (nameID 13).

| 字型 Font | 版權 Copyright | 授權 License |
|---|---|---|
| Noto Sans TC | © 2014–2021 Adobe, with Reserved Font Name 'Source' | [SIL OFL 1.1](https://scripts.sil.org/OFL) |
| TauhuOo (寶島宋體) | © 2014–2020 Adobe / TSNG, with Reserved Font Name 'Source' | [SIL OFL 1.1](https://scripts.sil.org/OFL) |
| DejaVu Sans | © 2003 Bitstream, Inc.; © 2006 Tavmjong Bah；DejaVu 的修改部分為公有領域 | [Bitstream Vera / DejaVu License](https://dejavu-fonts.github.io/License.html) |

OFL 字型不得單獨販售，且衍生字型必須沿用 OFL 授權。將字型與本專案（MIT）一同散布是
OFL 明文允許的。

OFL fonts may not be sold on their own, and derivative fonts must stay under OFL. Bundling
them alongside MIT-licensed software is explicitly permitted by the OFL.

## 相依套件 Dependencies

`website/package.json` 中的全部執行期與開發相依套件（React、React Router、Vite、ESLint 及
其型別定義）皆為 MIT 授權，與本專案的授權相容。

Every runtime and development dependency in `website/package.json` -- React, React Router,
Vite, ESLint and their type definitions -- is MIT licensed, compatible with this project.
