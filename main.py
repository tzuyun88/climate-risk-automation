import pandas as pd
from docx import Document

from config import (
    EXCEL_PATH, TEMPLATE_PATH, OUTPUT_PATH, ADDRESS_EXCEL, PICTURE_DIR,
    SHEET_PLACEHOLDERS, RISK_LEVEL_PLACEHOLDERS,
    HIGH_RISK_PLACEHOLDER, SITE_TABLE_PLACEHOLDER,
    HIGH_RISK_THRESHOLD, PICTURE_COUNT,
)
from data.loader import load_main_tables, load_address_mapping
from data.processor import attach_site_name, build_risk_level_tables, build_high_risk_table
from report.table_writer import insert_df_as_table
from report.picture_writer import find_picture_file, insert_picture_at_placeholder


def render_docx(template_path: str,
                output_path: str,
                raw_sheets: dict,
                derived_tables: dict,
                high_risk_df: pd.DataFrame,
                address_mapping_df=None,
                picture_dir: str = ".") -> None:
    """將所有資料表與圖片填入 Word 模板，輸出最終報告。"""

    doc = Document(template_path)

    # 1. 插入原始工作表
    print("\n--- 插入原始工作表 ---")
    for sheet_name, placeholder in SHEET_PLACEHOLDERS:
        if sheet_name in raw_sheets:
            insert_df_as_table(doc, placeholder, raw_sheets[sheet_name],
                               position="before", clear_placeholder=True)

    # 2. 插入三類風險等級表
    print("\n--- 插入風險等級表 ---")
    for cat, placeholder in RISK_LEVEL_PLACEHOLDERS.items():
        if cat in derived_tables:
            insert_df_as_table(doc, placeholder, derived_tables[cat],
                               position="after", clear_placeholder=True)

    # 3. 插入高風險區域表
    print("\n--- 插入高風險區域表 ---")
    if high_risk_df.empty:
        high_risk_df = pd.DataFrame(
            columns=["場址名稱", "淹水高風險", "坡地高風險", "乾旱高風險"]
        )
    insert_df_as_table(doc, HIGH_RISK_PLACEHOLDER, high_risk_df,
                       position="after", clear_placeholder=True, allow_empty=True)

    # 4. 插入場址表
    print("\n--- 插入場址表 ---")
    if address_mapping_df is not None and not address_mapping_df.empty:
        insert_df_as_table(doc, SITE_TABLE_PLACEHOLDER, address_mapping_df,
                           position="after", clear_placeholder=True)

    # 5. 插入圖片
    print("\n--- 插入圖片 ---")
    for i in range(1, PICTURE_COUNT + 1):
        placeholder = f"{{{{picture{i}}}}}"
        image_path = find_picture_file(picture_dir, i)
        if image_path is None:
            print(f"⚠ 找不到對應圖片：picture{i}")
            continue
        insert_picture_at_placeholder(doc, placeholder, image_path)

    # 6. 儲存輸出
    print("\n--- 儲存輸出檔案 ---")
    try:
        doc.save(output_path)
        print(f"✓ 成功輸出：{output_path}")
    except PermissionError:
        alt_path = output_path.replace(".docx", "_new.docx")
        try:
            doc.save(alt_path)
            print(f"✓ 原檔案被鎖定，已改存為：{alt_path}")
        except Exception as e:
            print(f"✗ 無法儲存檔案：{e}")


def main():
    print("========== 開始處理風險評估報告 ==========\n")

    # 1. 讀取原始工作表
    print("--- 讀取原始工作表 ---")
    raw_sheets = load_main_tables(EXCEL_PATH)

    if "總表" not in raw_sheets:
        print("✗ 錯誤：無法讀取總表，程式中止")
        return

    # 2. 讀取場址對應表
    print("\n--- 讀取場址表 ---")
    mapping_df = load_address_mapping(ADDRESS_EXCEL)

    # 3. 將場址名稱加入所有工作表
    print("\n--- 取代場址名稱 ---")
    if mapping_df is not None:
        for name, df in raw_sheets.items():
            raw_sheets[name] = attach_site_name(df, mapping_df, site_col_name="場址名稱")
            print(f"  - {name} 已加入場址名稱欄位")
    else:
        print("⚠ 無地址映射表，保留原始地址欄位")

    df_total = raw_sheets["總表"]
    site_col = "場址名稱" if "場址名稱" in df_total.columns else "正規化地址"

    # 4. 產生風險等級表
    print("\n--- 產生風險等級表 ---")
    derived_tables = build_risk_level_tables(df_total, site_col=site_col)

    # 5. 產生高風險區域表
    print("\n--- 產生高風險區域表 ---")
    high_risk_df = build_high_risk_table(
        derived_tables, site_col=site_col, threshold=HIGH_RISK_THRESHOLD
    )
    high_risk_df = high_risk_df.fillna("")

    # 6. 產生 Word 報告
    print("\n--- 產生 Word 文件 ---")
    render_docx(TEMPLATE_PATH, OUTPUT_PATH, raw_sheets, derived_tables,
                high_risk_df, mapping_df, picture_dir=PICTURE_DIR)

    print("\n========== 處理完成 ==========")


if __name__ == "__main__":
    main()