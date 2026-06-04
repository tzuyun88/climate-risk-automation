# ============ 路徑與常數設定 ============

EXCEL_PATH      = r"inputs/TEJESG.xlsx"
TEMPLATE_PATH   = r"inputs/template0.docx"
OUTPUT_PATH     = r"output.docx"           
ADDRESS_EXCEL   = r"inputs/address.xlsx"
PICTURE_DIR     = r"inputs"

# 主要工作表名稱列表
SHEET_NAMES = [
    "總表",
    "淹水_基期", "淹水_世紀中", "淹水_世紀末",
    "坡地_基期", "坡地_世紀中", "坡地_世紀末",
    "乾旱_基期", "乾旱_世紀中", "乾旱_世紀末",
]

# Word 模板中的 placeholder 對應
SHEET_PLACEHOLDERS = [
    ("總表",       "{{系統風險等級結果}}"),
    ("淹水_基期",  "{{淹水風險基期}}"),
    ("淹水_世紀中","{{淹水風險世紀中}}"),
    ("淹水_世紀末","{{淹水風險世紀末}}"),
    ("坡地_基期",  "{{坡地風險基期}}"),
    ("坡地_世紀中","{{坡地風險世紀中}}"),
    ("坡地_世紀末","{{坡地風險世紀末}}"),
    ("乾旱_基期",  "{{乾旱風險基期}}"),
    ("乾旱_世紀中","{{乾旱風險世紀中}}"),
    ("乾旱_世紀末","{{乾旱風險世紀末}}"),
]

RISK_LEVEL_PLACEHOLDERS = {
    "淹水": "{{淹水風險等級(基期、世紀中、世紀末)}}",
    "坡地": "{{坡地風險等級(基期、世紀中、世紀末)}}",
    "乾旱": "{{乾旱風險等級(基期、世紀中、世紀末)}}",
}

HIGH_RISK_PLACEHOLDER  = "{{高風險區域(4、5級)}}"
SITE_TABLE_PLACEHOLDER = "{{場址}}"

# 高風險閾值
HIGH_RISK_THRESHOLD = 4

# 圖片搜尋範圍
PICTURE_COUNT = 10