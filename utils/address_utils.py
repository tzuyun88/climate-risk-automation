import re
import pandas as pd


def normalize_address_key(value: object) -> str:
    """
    將地址轉成可比對的 key，降低格式差異造成的對不到。
    - 去除空白
    - 全形空格轉半形
    - 台 → 臺
    - 移除尾部小數點編號（如 '臺北市-1.1' → '臺北市-1'）
    """
    if pd.isna(value):
        return ""

    s = str(value).strip()
    s = s.replace("　", " ")
    s = re.sub(r"\s+", "", s)
    s = s.replace("台", "臺")
    s = re.sub(r"\.\d+$", "", s)
    return s