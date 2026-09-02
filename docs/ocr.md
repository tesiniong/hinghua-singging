# 羅馬字經文 OCR

用 1912 年原書掃描頁自動辨識平話字經文，產生可填入 `data/rom.txt` 的候選文字與校對報告。
原書只有羅馬字，所以這條流程只處理羅馬字；漢字仍由人工轉寫。

## 為什麼要自己訓練

平話字約 22% 的字元是變音符號（U+0324 下圓點、U+030D、U+0304、U+0302、U+0301、U+207F）。
通用 OCR 的字元表沒有這些符號，零樣本的錯誤率有下限：

| 系統（零樣本，1,202 行人工標註，創世記 1–8 章） | CER 含符號 | CER 去符號 |
|---|---|---|
| EasyOCR en | 46.7% | 34.6% |
| PaddleOCR PP-OCRv5 server | 24.4% | 10.9% |
| PaddleOCR latin PP-OCRv5 mobile | 21.2% | 7.9% |
| Qwen2.5-VL-3B（本機視覺語言模型） | 42.8% | 32.1% |

字母骨架已達九成二，差距全在符號，所以用行圖訓練一個專用的 kraken 模型。
訓練資料不必人工標註：把 PaddleOCR 的輸出對齊到 `rom.txt` 已錄入的經文，
還原出帶符號的行標籤，與人工標註比對有八成整行一致、CER 4%。

目前的模型 `hinghua_pages2_best.mlmodel`（三階段訓練加一次重新對齊續訓，見下）在保留的測試頁
（0017–0022，標籤抄自 rom.txt 的 515 行）行級 CER 1.3%、整行全對 74%；
拿已錄入的創世記 1–20 章做端到端評估（辨識＋切節，440 節；四福音書的數字見「切節」）：

| 指標 | 貪婪解碼 | 受限 beam 解碼（現行） |
|---|---|---|
| 逐節 CER（含切節錯誤） | 3.5% | 2.0% |
| 整節完全正確 | 59% | 65% |
| 兩個字元以內可修好 | 82% | 86% |

印刷清晰的章節逐節 CER 在 1% 上下，磨損頁（創世記 6–10、18）明顯較差。

## 素材與目錄

行圖、模型、辨識結果都在 repo 外，位置可用環境變數覆寫（見 `scripts/tools/ocr/common.py`）：

| 內容 | 預設位置 | 環境變數 |
|---|---|---|
| 行圖 `<page>/<page>_line_NNNN.png`（138,334 張，kraken 版面切割） | `~/projects/buc_ocr/output/line_images/` | `HINGHUA_OCR_LINES` |
| 版面切割 JSON `<page>.json`（與行圖同序，含座標） | `~/projects/buc_ocr/output/json_results/` | `HINGHUA_OCR_SEG` |
| 工作目錄：`labels/`、`dataset/`、`models/`、`recognized/` | `~/projects/hinghua-ocr-work/` | `HINGHUA_OCR_WORK` |

環境：PaddleOCR 在 conda `base`，kraken 6 在 conda `hinghua-ocr`。
`recognize.py` 需用 `hinghua-ocr` 的 Python 執行，其餘腳本用 `base`。

## 流程

```bash
R=~/projects/hinghua-singging/scripts/tools/ocr          # 或 worktree 的路徑
K=~/miniconda3/envs/hinghua-ocr/bin                      # kraken 所在環境
cd ~/projects/hinghua-ocr-work
python $R/make_labels.py                                 # 舊行圖：PaddleOCR 對齊 rom.txt → labels/auto_labels.json
python $R/build_dataset.py                               # → dataset/{train,val,test}/、train.txt、train_digits.txt
$K/ketos -d cuda:0 --workers 4 train -f path -t dataset/train.txt -e dataset/val.txt \
    -u NFD -B 16 -r 0.001 --augment --lag 10 --min-epochs 20 -o models/hinghua     # 第一階段（約 45 分鐘）
$K/ketos -d cuda:0 --workers 4 train -i models/hinghua_best.mlmodel -f path \
    -t dataset/train_digits.txt -e dataset/val.txt -u NFD -B 16 -r 0.0003 --augment \
    --lag 5 --min-epochs 3 -o models/hinghua_ft                                     # 第二階段：加強節號數字
python $R/make_labels.py --page-crops                    # 整頁裁切版的行圖與標籤（與辨識時同一套裁法）
python $R/build_dataset.py --page-crops                  # → dataset/pages_{train,val,test}/、pages_train_digits.txt
# 有了自家模型後改用它的辨識結果對齊（需先對已錄入的頁跑過 recognize.py），能對上更多行：
python $R/make_labels.py --page-crops --from-recognized  # → labels/auto_labels_pages_recognized.json
python $R/build_dataset.py --page-crops --from-recognized
$K/ketos -d cuda:0 --workers 4 train -i models/hinghua_ft_best.mlmodel -f path \
    -t dataset/pages_train_digits.txt -e dataset/pages_val.txt -u NFD -B 16 -r 0.0003 --augment \
    --lag 5 --min-epochs 4 -o models/hinghua_pages                                  # 第三階段：適應整頁裁切
$K/python $R/recognize.py -m models/hinghua_pages2_best.mlmodel --manifest dataset/pages_test_auto.txt -o recognized/testauto.json
python $R/evaluate.py recognized/testauto.json --labels dataset/pages_test_auto_labels.json   # 標籤抄自 rom.txt 的 505 行，比較模型用這組
$K/python $R/recognize.py -m models/hinghua_pages2_best.mlmodel --manifest dataset/pages_test.txt -o recognized/test.json
python $R/evaluate.py recognized/test.json               # 前次人工標註的 454 行；少數行框與標註對不上，CER 偏高，只看整行全對
$K/python $R/recognize.py -m models/hinghua_pages2_best.mlmodel --pages 0028-0048
python $R/assemble.py --book Genesis --chapters 21-33            # 只寫報告
python $R/assemble.py --book Genesis --chapters 1-20 --evaluate  # 拿已錄入的章節做端到端評估
python $R/assemble.py --book Genesis --chapters 21-33 --write    # 填入 rom.txt 的空節，並記進 data/ocr-draft.json
python scripts/build_all.py
```

`load_rom_verses()` 預設**不含** `ocr-draft.json` 列出的草稿節，所以標籤、音節詞表與 `--evaluate`
都只用人工正本；草稿是模型自己的輸出，拿來當標籤等於把辨識錯誤學回去。

三個訓練階段各解決一件事：第一階段學字母與符號；第二階段把含數字的行重複三次，
因為上標節號是小字，只認得 89% 的節號，微調後到 99%；第三階段換成與辨識時完全相同的
整頁裁切行圖，因為前次切割的行圖與整頁裁切的分布不同，同一個模型在後者上的錯誤率高四倍。
`recognize.py` 也不再用舊行圖，而是從整頁圖裁切：偵測欄溝、塗掉欄線、把被切碎的行框合併、
拉到整欄寬、以基線撐到標準行高，再貼著墨跡裁切。前次切割偶爾整行漏掉（四福音書 141 頁裡有 13 頁，
最嚴重的一頁漏了 16 行，整章開頭就不見），所以 `page_lines` 最後有一步 `fill_line_gaps`：
同欄相鄰兩行的距離超過行距 1.7 倍時，在缺口裡對該欄做墨跡的水平投影，把有墨的段落補成行
（太高的段落依行距在墨量最少處切開）；缺口裡沒有墨（書卷結尾的空白）就不補。

## 解碼：只出合法音節

kraken 預設逐格取最大機率（貪婪解碼），會吐出 `da̤̍u̍h`（兩個調符）這種不可能的音節。
`decode.py` 改用 prefix beam search：合法音節（`data/hinghua-finals.txt` 的 230 個韻母＋聲調 × 15 個聲母
＝ 3,420 個）做成字首樹，每條路徑記住目前音節走到哪個節點，離開字首樹扣分（不是禁止：頁眉、
人名偶爾會有集合外的拼法），音節收尾時加上 `lm_weight × log P(音節 | 前一音節)`，bigram 從正本
3.7 萬個音節估（絕對折扣後退到 unigram）。每個音節另有一個插入獎勵抵銷 LM 的平均成本，否則
權重一高解碼器就會漏掉行首行尾的短音節。大小寫不管；數字、標點、空格、連字號是音節邊界。

在 515 行測試集上（bigram 排除測試頁的經節）：

| 解碼 | CER | 整行全對 |
|---|---|---|
| 貪婪 | 1.26% | 73.8% |
| 只限制合法音節（lm_weight 0） | 1.20% | 74.6% |
| 限制＋bigram，lm_weight 0.7 | 1.03% | 78.3% |

修掉的多是調符與行尾少一個字母；剩下的錯多在數字（不受限制）、人名、l／i 這類 LM 幫不上的地方。
`recognize.py` 預設用它（`--decoder greedy` 可切回），一行約 10 ms；建 bigram 時排除目標頁上已錄入的
經節，評估才不會看過答案。端到端（辨識＋切節）在馬太福音 517 節正本上：逐節 CER 2.5% → 2.3%、
整節正確 54% → 61%、兩字元內可修好 82% → 85%。

## 切節

上標節號在磨損頁面上幾乎是隨機誤讀（尤其單位數），單靠數字序列切不準。
`assemble.py` 用三個線索一起決定：

1. 頁面對應表給出本頁應出現的節號序列（起始節號到下一頁起始節號之前），章標題視為第 1 節的標記。
2. 觀察到的數字與預期序列做編輯距離對齊：數字相同 0 分、差一位數 0.5 分、後面接大寫字母較可信。
3. `han.txt` 的字數等於羅馬字的音節數（創世記 440 節中 396 節完全相等），所以切出來的每節
   長度必須符合漢字版字數；節號完全沒讀出來時，也照字數把併在一起的經文切開。

沒有漢字版的章節只剩前兩個線索，建議優先處理已有漢字版的章節。已有人工正本的節，
正本的音節數也當長度線索用（同一個機制）：馬太福音對 517 節正本的逐節 CER 由 11.5% 降到 2.5%。
但這個數字對「已知的節」偏樂觀——保留實驗（藏起偶數節的長度、只評估這些節）得到
CER 10%、整節正確 52%、兩字元內 78%，才是沒有任何長度線索的節的真實水準：多數節沒問題，
約五分之一的節切節有誤。

| 腳本 | 做什麼 |
|---|---|
| `common.py` | 路徑、NFD 叢集切分、去符號比對、向量化的半全域對齊、頁面↔經節對應、行的閱讀順序 |
| `make_labels.py` | 只處理 `rom.txt` 已有經文的頁面；對齊後吸附到詞界，行尾斷詞保留連字號；貼著缺文邊界或長度差太多的行捨棄。也把前次的人工標註分類（`ok`／`offbyone`／`bad`） |
| `build_dataset.py` | 測試集固定用人工標註過的 0017–0022 頁；其餘自動標籤隨機切 8% 當驗證集；另產生數字加重清單 |
| `recognize.py` | 逐頁辨識：偵測欄溝並塗掉欄線、把前次切割被欄線切碎的行框合併、補回切割漏掉的行、從整頁圖裁行，交給 `decode.py` 解碼，輸出每行文字與信心，並標記頁眉、頁碼、放大字母 |
| `decode.py` | 受限 CTC beam search：只走合法音節的字首樹，加正本音節 bigram；`--manifest` 模式比較貪婪與 beam 的 CER、掃參數 |
| `evaluate.py` | 含符號／去符號 CER、整行正確率、最常見混淆 |
| `assemble.py` | 丟掉頁眉頁碼、接回行尾連字號、依內文節號切節（用頁面對應表的起始節號校正、容忍上標數字誤讀）、章標題轉 `## N`，填入既有的空節號行並記進 `ocr-draft.json`；`--evaluate` 與已錄入的人工正本比對 |
| `draft.py` | 管理 `ocr-draft.json`：列出、校對完清除、找過時標記 |
| `../check_rom_syllables.py` | 正本裡不合法的音節；`--html` 附 OCR 讀法與掃描裁圖 |
| `proofread.py` | 反過來用模型校對人工正本：逐節比對 git 已提交的 `rom.txt`，差異分 A（疑似正本打錯）、B（需看圖判斷）、C（多半 OCR 錯）、D（標點空格），輸出附掃描裁圖的 HTML |

`page-ocr-results.json` 記的是每頁第一個「節號」，頁首通常還有前一節的尾巴；
對齊與組裝都已把前一節納入。

## 訓練資料從哪裡來、怎麼變多

標籤全部來自人工錄入的 `rom.txt`，圖來自兩處：第一、二階段用前次專案切好的行圖，
第三階段用整頁裁切的行圖。前次的 1,202 行人工標註只當測試集，沒有拿去訓練。
沒錄入的章節沒有標籤，所以沒用到。

對齊時只收 OCR 與正本夠像的行，所以已錄入頁面上的行也不是全都用上。
拿 PaddleOCR 的輸出對齊，123 頁得到 4,686 行；改拿自家模型的辨識結果對齊
（`make_labels.py --page-crops --from-recognized`，需先對這些頁跑過 `recognize.py`）得到 4,792 行，
只多 2%——瓶頸是已錄入的頁數，不是對齊。OCR 草稿的頁不算在內（見上）。
要再增加資料有三條路，由易到難：

1. **重新對齊**：如上，一個指令，再跑第三階段訓練即可。做過一次（4,792 行、從 `hinghua_pages_best` 續訓，
   最佳在第 1 輪）：測試 515 行 CER 1.35% → 1.26%、整行全對 73.6% → 74.0%，只是小幅改善，
   產物是 `models/hinghua_pages2_best.mlmodel`。
2. **校對過的 OCR 章節變成新正本**：每校完一章（`draft.py --clear`），它所在的頁就能產生新標籤；同時 `assemble.py` 的長度線索也需要該章的漢字版。
3. **未錄入頁面的自我訓練**：用模型的高信心輸出當假標籤。還沒做，風險是把模型的錯誤學進去，要用音節表過濾。

重訓的指令是「訓練」一節裡第三階段那兩行，把 `-i` 換成目前最好的模型即可，不必從頭訓練。

## 之後要跑新章節時

```bash
cd ~/projects/hinghua-ocr-work
K=~/miniconda3/envs/hinghua-ocr/bin; R=<repo>/scripts/tools/ocr
python -c "..."                                  # 用 assemble.pages_for 查該章節所在頁碼，或直接看 page-ocr-results.json
$K/python $R/recognize.py -m models/hinghua_pages2_best.mlmodel --pages 0049-0071
# 頁數多時分批並行（例如每 12 頁一個程序），一頁約 10 秒
python $R/assemble.py --book Genesis --chapters 34-50            # 先只看報告
python $R/assemble.py --book Genesis --chapters 34-50 --write    # 確認後填入空節
python <repo>/scripts/build_all.py
```

條件：書名已在 `scripts/book_info.py`、`page-ocr-results.json` 有那些頁的起始節號、`rom.txt`
已有該卷的書名行（章節骨架缺的會自動補）。填入後在網站上對照 📖 圖示校對，改完再 commit。

## 印刷勘誤：原書印錯、正本照規範寫

原書大寫字母上的調符常漏印（I-seh-le̍h、A-láng），也有零星印錯（ló̤ng-cô̤ng）。正本 `rom.txt`
維持規範寫法，模型則應照圖上印的讀，不能學會「補調符」。兩邊的橋是 `data/print-errata.tsv`
（書、章:節、原書印法、規範寫法；`*` 表示全部）：

- `make_labels.py` 做訓練標籤前把那些節換回印法；`proofread.py` 比對前也換回，OCR 讀到印刷的樣子就不算差異。
- 填新章節時 `assemble.py` 反過來把印法改成規範寫法：勘誤表裡 `*` 的條目直接換；大寫開頭又沒調符的音節，
  若正本從未這樣寫、且只有一種帶調符的寫法（`capital_lexicon`），就換成那個寫法，並加旗標
  「依正本詞表改成規範寫法」讓校對者知道。兩種寫法都出現過的（如 Ca̤uⁿ）不動。
- 逐節的漏調符不必一一列進勘誤表，只有 `assemble.py` 的詞表規則判斷不了、或不是大寫漏調符的才要列。

## 辨識草稿

OCR 填入的經文可以先上線，但要讓讀者看得出來它還沒校對。機制：

- `assemble.py --write` 把填入的節連同校對旗標記進 `data/ocr-draft.json`（格式見 [data-format.md](data-format.md)）。
- `bible_data.py` 據此在 `bible_data.json` 的節上加 `rom_draft`、章上加 `draft_verses`；
  網站在經文、章節選單與搜尋結果標示「OCR 辨識草稿，未經校對」，有旗標的節另加 ⚠。
- `rom_to_han_dict.py`、`homophone_table.py` 略過草稿節；`load_rom_verses()` 也不把草稿當正本。
- 換了更好的模型或解碼器想重跑已填過的章節：`assemble.py --write --overwrite-draft` 會把仍在草稿清單裡的節
  換成新結果（已校對、已從清單移除的節不動）。
- 校對流程：對照 📖 掃描頁改 `rom.txt`，改完一章就 `python scripts/tools/ocr/draft.py --clear Genesis 21`
  （也可指定個別節 `21:5 21:7-9`），再跑 `build_all.py`。`draft.py` 不帶參數列出各卷草稿數，
  `--list Genesis 21` 看該章旗標，`--check` 找出指到空節的過時標記。

沒有漢字版的書卷（四福音書幾乎都沒有）切節只剩節號序列可靠，所以「節號未辨識出」與
「節號讀作 …」這類旗標在草稿裡特別重要，校對時先看有 ⚠ 的節。

## 校對報告

`assemble.py` 在 `recognized/<書>_<章>-<章>_report.md` 列出需要注意的節：

| 旗標 | 意思 |
|---|---|
| 首節（首字放大） | 章首第一字是放大字母，切割常出問題，一律核對 |
| 節號未辨識出 | 該節經文可能併進前一節 |
| 文中出現非預期數字 | 節號可能誤讀，需核對切節位置 |
| 含詞表外音節 | 音節不在 `rom.txt` 已錄入的 1,200 個音節內，八成是辨識錯誤 |
| 低信心 | 該節某行的平均信心低於 0.6 |
| 頁面對應表預期… | 頁末所在節與 `page-ocr-results.json` 不一致，可能漏節或該表有誤 |
| rom.txt 已有內容／已有 OCR 草稿，不覆寫 | 該節已填過，本次不動；後者表示現有內容是之前的草稿 |

沒有旗標的節仍可能有錯，只是機率低；建議校對時對照 📖 圖示開啟的掃描頁。

## 已知限制

- 行框來自 `buc_ocr` 專案的切割，只在本地修補（合併碎片、補漏行）；若要整頁重切，需重跑該專案的 `batch_segmentation.py`。
- 改了 `page_lines` 之後，`recognized/<page>.json` 的行數會跟新裁法對不上，`make_labels.py --from-recognized`
  會略過那些頁並提示，要先重跑 `recognize.py`。
- 章首放大字母幾乎都要人工修。
- 原書沒有段落小標，`###` 由人工另加。
