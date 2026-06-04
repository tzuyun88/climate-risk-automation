# Climate Risk Assessment Automation

![Python](https://img.shields.io/badge/Python-3.12-blue.svg)
![Pandas](https://img.shields.io/badge/Pandas-Data_Processing-orange.svg)
![python-docx](https://img.shields.io/badge/python--docx-Report_Generation-green.svg)

---

## Motivation & Overview 
企業在進行ESG氣候風險盤查時，往往需要針對大量場址彙整自然災害風險數據。
* **傳統痛點**：原始下載資料龐雜，需透過人工逐一比對數據、地址來手動製作 Word 報告。
* **解決方案**：本專案開發一套 Python 自動化腳本，實現「資料清洗、地址對應、高風險篩選到報告產出」，一鍵生成風險評估報告書。

---

## Tech Stack 
* **Python 3.12**：主要開發語言
* **pandas & openpyxl**：Excel 資料讀取、清洗與多維度整合分析
* **python-docx**：Word 模板動態標籤取代、表格繪製與圖片插入

---

## Architecture
專案採用模組化設計，由 `main.py` 作為核心驅動，分工如下：
* `data/`：負責原始資料與地址對應表的讀取與轉換。
* `utils/`：提供地址比對用的最小格式轉換。
* `report/`：將處理完的 DataFrame 與圖檔精準填入 Word 模板中的 `{{placeholder}}`。

---


### What This Project Is
* **地址對應**：依地址對應表，將輸入資料中的地址轉換為場址名稱。
* **高風險區域自動標記**：以「世紀中」最大風險值為依據，篩選 $\ge 4$ 級之高風險場址並製表。(原始設定)
* **動態圖文渲染**：將多張圖表，按模板標籤自動排版、填入並輸出。

### What This Project Is Not
* **非原始數據爬蟲**：本專案專注於「資料處理與報告自動化生成」，不包含前端網站的原始數據爬取與收集。
* **非視覺化互動網頁**：本工具為後端批次處理腳本，直接產出標準 Word 報告檔案，非網頁端 Dashboard。

---

## Core Mechanics

### 1. 跨來源地址編號格式不一致
* **挑戰**：TEJESG.xlsx 輸出的地址可能帶有 Excel 產生的尾端小數點編號。
* **解法**：於 `utils/address_utils.py` 僅保留必要的尾端編號修正，避免改動公司原始地址文字，再進行場址名稱對應。

### 2. Word Python-docx Run 區塊斷裂問題
* **挑戰**：Word 模板中的 `{{placeholder}}` 文字常被 `python-docx` 拆分成多個不同的 `run` 物件，導致直接搜尋字串時失效。
* **解法**：在走訪段落時，先將同一個段落內的 `run` 文字進行邏輯合併，定位後再進行取代，確保標籤完全清除。

### 3. 檔案鎖定不中斷流程
* **挑戰**：當使用者開啟 `output.docx` 時，程式執行會因 `PermissionError` 中斷。
* **解法**：加入 `try-except` 機制，若遇鎖定則自動改存為 `output_new.docx`，以生產報告為首，再來進行修正。

---

## Setup & Execution

### 1. Setup (環境準備)
確保你的電腦已安裝 Python 3.x，並在專案資料夾下執行以下指令安裝所需依賴套件：
```bash
pip install -r requirements.txt
