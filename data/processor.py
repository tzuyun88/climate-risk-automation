import pandas as pd
from typing import Dict, Optional
from utils.address_utils import normalize_address_key


def attach_site_name(df: pd.DataFrame,
                     mapping_df: Optional[pd.DataFrame],
                     address_col: str = "正規化地址",
                     site_col_name: str = "場址名稱") -> pd.DataFrame:
    """
    依地址對應表，將「場址名稱」欄位加入 DataFrame。
    - 對不到時以原始地址回填，確保欄位始終存在。
    - 成功加入後刪除地址欄，保持格式統一。
    - 場址名稱欄移到最前面。
    """
    df_result = df.copy()

    if mapping_df is None or mapping_df.empty:
        print("⚠ 未提供地址對應表，無法轉換成場址名稱")
        return df_result

    # 自動偵測地址欄位名稱
    if address_col not in df_result.columns:
        if "地址" in df_result.columns:
            address_col = "地址"
        else:
            print(f"⚠ 此表格沒有地址欄位，無法加入場址名稱")
            return df_result

    # 建立正規化地址 → 場址名稱 的映射字典
    mapping_norm = mapping_df.copy()
    mapping_norm["_addr_key"] = mapping_norm["地址"].map(normalize_address_key)
    addr_to_site = dict(zip(mapping_norm["_addr_key"], mapping_norm["場址名稱"]))

    # 比對並填入場址名稱
    addr_keys = df_result[address_col].map(normalize_address_key)
    mapped_site = addr_keys.map(addr_to_site)

    fallback_site = df_result[address_col].astype(str).where(
        df_result[address_col].notna(), ""
    )
    df_result[site_col_name] = mapped_site.fillna(fallback_site)

    # 場址名稱移到最前面
    cols = list(df_result.columns)
    cols.remove(site_col_name)
    df_result = df_result[[site_col_name] + cols]

    # 刪除地址欄
    df_result = df_result.drop(columns=[address_col])

    return df_result


def build_risk_level_tables(df_total: pd.DataFrame,
                            site_col: str = "場址名稱") -> Dict[str, pd.DataFrame]:
    """
    從總表產生三大類（淹水、坡地、乾旱）的風險等級表，
    各含「基期、世紀中、世紀末」三個時期欄位。
    """
    categories = {
        "淹水": ["淹水基期", "淹水世紀中", "淹水世紀末"],
        "坡地": ["坡地基期", "坡地世紀中", "坡地世紀末"],
        "乾旱": ["乾旱基期", "乾旱世紀中", "乾旱世紀末"],
    }

    risk_tables = {}

    for cat, cols in categories.items():
        if site_col not in df_total.columns:
            print(f"⚠ 總表缺少場址欄位 '{site_col}'，略過 {cat} 等級表")
            continue

        if not all(c in df_total.columns for c in cols):
            print(f"⚠ 總表缺少 {cat} 風險欄位 {cols}，略過")
            continue

        df_cat = df_total[[site_col] + cols].copy()
        df_cat.columns = [site_col, "風險等級基期", "風險等級世紀中", "風險等級世紀末"]

        risk_tables[cat] = df_cat
        print(f"✓ 產生 {cat} 風險等級表，{len(df_cat)} 筆記錄")

    return risk_tables


def build_high_risk_table(derived_tables: Dict[str, pd.DataFrame],
                          site_col: str = "場址名稱",
                          threshold: int = 4) -> pd.DataFrame:
    """
    產生高風險區域表（風險等級 >= threshold 標記為 Y）。
    以「世紀中」時期的最大風險值為判斷依據。
    """
    if not derived_tables:
        print("⚠ 未提供風險等級表，無法產生高風險區域表")
        return pd.DataFrame()

    # 蒐集所有場址
    all_sites = set()
    for df_cat in derived_tables.values():
        if site_col in df_cat.columns:
            all_sites.update(df_cat[site_col].dropna().unique())

    high_df = pd.DataFrame({site_col: sorted(list(all_sites))})

    for cat in ["淹水", "坡地", "乾旱"]:
        col_name = f"{cat}高風險"
        df_cat = derived_tables.get(cat)

        if df_cat is None or site_col not in df_cat.columns:
            high_df[col_name] = ""
            continue

        if "風險等級世紀中" not in df_cat.columns:
            high_df[col_name] = ""
            continue

        df_cat_copy = df_cat.copy()
        df_cat_copy["風險等級世紀中"] = pd.to_numeric(
            df_cat_copy["風險等級世紀中"], errors="coerce"
        )

        # 同一場址取最大風險值，避免 duplicate index 錯誤
        df_cat_indexed = (
            df_cat_copy
            .groupby(site_col, as_index=True)["風險等級世紀中"]
            .max()
            .to_frame()
        )

        flags = (
            df_cat_indexed["風險等級世紀中"]
            .reindex(high_df[site_col])
            .fillna(0) >= threshold
        )
        high_df[col_name] = ["Y" if v else "" for v in flags.values]

    print(f"✓ 產生高風險區域表，{len(high_df)} 筆記錄")
    return high_df