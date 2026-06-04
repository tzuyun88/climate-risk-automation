import pandas as pd
from typing import Dict, Optional
from config import SHEET_NAMES


def load_main_tables(excel_path: str) -> Dict[str, pd.DataFrame]:
    """
    讀取 TEJESG.xlsx 中所有指定工作表。
    若工作表含「正規化地址」與「原始地址」，保留正規化地址並刪除原始地址。
    """
    raw_sheets = {}

    for name in SHEET_NAMES:
        try:
            df = pd.read_excel(excel_path, sheet_name=name)

            if "正規化地址" in df.columns and "原始地址" in df.columns:
                df = df.drop(columns=["原始地址"])

            raw_sheets[name] = df
            print(f"✓ 讀取：{name}")

        except Exception:
            print(f"⚠ 無法讀取工作表：{name}")

    return raw_sheets


def load_address_mapping(excel_path: str,
                         sheet_name: str = "1") -> Optional[pd.DataFrame]:
    """
    讀取 address.xlsx 地址對應表。
    必要欄位：「場址名稱」、「地址」。
    """
    try:
        df_addr = pd.read_excel(excel_path, sheet_name=sheet_name)

        required_cols = ["場址名稱", "地址"]
        missing = [c for c in required_cols if c not in df_addr.columns]
        if missing:
            print(f"⚠ 地址對應表缺少欄位：{missing}，實際欄位：{list(df_addr.columns)}")
            return None

        print(f"✓ 讀取地址對應表：{len(df_addr)} 筆記錄")
        return df_addr

    except Exception as e:
        print(f"⚠ 無法讀取地址對應表：{e}")
        return None