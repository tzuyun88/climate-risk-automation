import re
import pandas as pd


def normalize_address_key(value: object) -> str:
    """
    將地址轉成比對用 key。

    保留原始地址文字，只移除 Excel 產生的尾部小數點編號
    （如 '臺北市-1.1' -> '臺北市-1'）。
    """
    if pd.isna(value):
        return ""

    s = str(value).strip()
    s = re.sub(r"\.\d+$", "", s)
    return s
