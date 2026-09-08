"""
VN-FINANCE INSIGHTS - FINANCIAL METRICS ENGINE
Tác giả: Chuyên viên Phân tích & Phát triển Dữ liệu Chứng khoán - Người Quan Sát
Mô tả:
  - Tính toán các chỉ số định giá thị trường: P/E, P/B, biến động thanh khoản MA20
  - Tính toán Trailing Twelve Months (TTM) & Biến động kỳ (Δ QoQ, Δ YoY) cho BCTC
  - Xử lý triệt để Missing Values / NaN trong các kỳ so sánh gốc
  - Chuẩn hóa Radar CAMEL 5 chiều bằng Min-Max Scaling chuẩn phân vị ngành
  - Thuật toán chấm điểm và xếp hạng Sức khỏe Tài chính Ngân hàng (CAMEL Scorecard)
"""

import os
import sys
import logging
import numpy as np
import pandas as pd

# Thiết lập mã hóa UTF-8 cho console Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("FinancialMetrics")


# =====================================================================
# 1. CORE BANKING & FINANCIAL METRICS (TTM & QoQ / YoY DELTAS)
# =====================================================================

def compute_banking_metrics(df_bank: pd.DataFrame) -> pd.DataFrame:
    """
    Tính toán các chỉ số tài chính ngân hàng chuyên sâu với TTM và Delta QoQ / YoY:
      1. NIM (Net Interest Margin - % năm): (Thu nhập lãi thuần * 4) / Tài sản sinh lời bình quân
      2. NPL (Tỷ lệ nợ xấu - %): Nợ nhóm 3,4,5 / Tổng dư nợ
      3. LLR (Tỷ lệ bao phủ nợ xấu - %): Dự phòng rủi ro / Nợ xấu nhóm 3,4,5
      4. CASA (Tỷ lệ tiền gửi không kỳ hạn - %): Tiền gửi không kỳ hạn / Tổng tiền gửi KH
      5. ROE Annualized & ROE TTM: Tính trên 4 quý trượt gần nhất
      6. ROA (% năm hóa): (Lợi nhuận sau thuế * 4) / Tổng tài sản
      7. Tăng trưởng tín dụng & biến động kỳ (Δ QoQ, Δ YoY)
    """
    df = df_bank.copy()

    # Sắp xếp theo mã ngân hàng và thời gian để tính toán chuỗi trượt
    df = df.sort_values(by=["symbol", "period"]).reset_index(drop=True)

    # 1. Biên lãi thuần NIM (Annualized Net Interest Margin)
    df["nim"] = ((df["net_interest_income"] * 4) / df["earning_assets_avg"]) * 100
    df["nim"] = df["nim"].round(2)

    # 2. Tỷ lệ nợ xấu NPL (Non-Performing Loan Ratio)
    df["npl_ratio"] = (df["npl_group_3_4_5"] / df["customer_loans"]) * 100
    df["npl_ratio"] = df["npl_ratio"].round(2)

    # 3. Tỷ lệ bao phủ nợ xấu LLR (Loan Loss Reserve Ratio)
    df["llr_ratio"] = (df["loan_loss_provision"] / df["npl_group_3_4_5"]) * 100
    df["llr_ratio"] = df["llr_ratio"].round(1)

    # 4. Tỷ lệ tiền gửi không kỳ hạn CASA (Current Account Savings Account)
    df["casa_ratio"] = (df["casa_deposits"] / df["customer_deposits"]) * 100
    df["casa_ratio"] = df["casa_ratio"].round(2)

    # 5. Lợi nhuận 12 tháng gần nhất (Trailing Twelve Months - TTM)
    # Xử lý khuyết tật dữ liệu: nếu chưa đủ 4 quý, nhân hệ số tương ứng để không bị NaN/None
    def calc_ttm_profit(series):
        ttm_vals = []
        for i in range(len(series)):
            window = series.iloc[max(0, i - 3): i + 1]
            factor = 4.0 / len(window)
            ttm_vals.append(window.sum() * factor)
        return pd.Series(ttm_vals, index=series.index)

    df["net_profit_ttm"] = df.groupby("symbol")["net_profit"].transform(calc_ttm_profit).round(0)

    # 6. ROE Annualized & ROE TTM
    df["roe"] = ((df["net_profit"] * 4) / df["equity"]) * 100
    df["roe"] = df["roe"].round(2)

    df["roe_ttm"] = ((df["net_profit_ttm"] / df["equity"]) * 100).round(2)

    # 7. ROA (% năm hóa)
    df["roa"] = ((df["net_profit"] * 4) / df["total_assets"]) * 100
    df["roa"] = df["roa"].round(2)

    # 8. Định giá P/E và P/B
    df["pe_ratio"] = (df["market_price"] / df["eps"]).round(2)
    df["pb_ratio"] = (df["market_price"] / df["book_value"]).round(2)

    # 9. TÍNH TOÁN BIẾN ĐỘNG KỲ (Δ QoQ & Δ YoY) — Xử lý triệt để Missing Values
    # Biến động QoQ (so với quý liền trước)
    df["nim_diff_qoq"] = df.groupby("symbol")["nim"].diff().fillna(0.0).round(2)
    df["npl_diff_qoq"] = df.groupby("symbol")["npl_ratio"].diff().fillna(0.0).round(2)
    df["casa_diff_qoq"] = df.groupby("symbol")["casa_ratio"].diff().fillna(0.0).round(2)
    df["llr_diff_qoq"] = df.groupby("symbol")["llr_ratio"].diff().fillna(0.0).round(1)
    df["loans_growth_qoq"] = (df.groupby("symbol")["customer_loans"].pct_change() * 100).fillna(0.0).round(2)

    # Biến động YoY (so với cùng kỳ 4 quý trước). Nếu là các quý đầu tiên, dùng QoQ làm xấp xỉ an toàn
    df["nim_diff_yoy"] = df.groupby("symbol")["nim"].diff(4)
    df["nim_diff_yoy"] = df["nim_diff_yoy"].fillna(df["nim_diff_qoq"]).round(2)

    df["npl_diff_yoy"] = df.groupby("symbol")["npl_ratio"].diff(4)
    df["npl_diff_yoy"] = df["npl_diff_yoy"].fillna(df["npl_diff_qoq"]).round(2)

    df["casa_diff_yoy"] = df.groupby("symbol")["casa_ratio"].diff(4)
    df["casa_diff_yoy"] = df["casa_diff_yoy"].fillna(df["casa_diff_qoq"]).round(2)

    df["llr_diff_yoy"] = df.groupby("symbol")["llr_ratio"].diff(4)
    df["llr_diff_yoy"] = df["llr_diff_yoy"].fillna(df["llr_diff_qoq"]).round(1)

    df["loans_growth_yoy"] = (df.groupby("symbol")["customer_loans"].pct_change(4) * 100)
    df["loans_growth_yoy"] = df["loans_growth_yoy"].fillna(df["loans_growth_qoq"]).round(2)

    logger.info("Hoàn tất tính toán các chỉ số Core Banking Metrics (TTM & QoQ/YoY Deltas).")
    return df


# =====================================================================
# 2. CHUẨN HÓA RADAR CHART (CAMEL-LIKE MIN-MAX SCALING)
# =====================================================================

def compute_camel_radar_dimensions(df_record: pd.Series) -> dict:
    """
    Chuẩn hóa 5 trục CAMEL theo thang điểm Min-Max [10, 100] theo phân vị ngành:
      - C (Capital Buffer): LLR Ratio [50% -> 250%]
      - A (Asset Quality): 100 - NPL Ratio [NPL 0.8% -> 3.0%]
      - M (Management & Cheap Fund): CASA Ratio [15% -> 45%]
      - E (Earnings): ROE TTM [10% -> 25%]
      - L (Liquidity & Margins): NIM [2.0% -> 5.5%]
    """
    def scale_val(val, min_val, max_val, invert=False):
        val_clamped = max(min_val, min(max_val, val))
        score = ((val_clamped - min_val) / (max_val - min_val)) * 90.0 + 10.0
        return round(110.0 - score if invert else score, 1)

    llr = df_record.get("llr_ratio", 150.0)
    npl = df_record.get("npl_ratio", 1.5)
    casa = df_record.get("casa_ratio", 30.0)
    roe = df_record.get("roe_ttm", df_record.get("roe", 18.0))
    nim = df_record.get("nim", 3.5)

    return {
        "C - Đệm Dự Phòng (LLR)": scale_val(llr, 50.0, 250.0),
        "A - An Toàn Nợ (NPL)": scale_val(npl, 0.8, 3.0, invert=True),
        "M - Vốn Rẻ (CASA)": scale_val(casa, 15.0, 45.0),
        "E - Sinh Lời (ROE TTM)": scale_val(roe, 10.0, 25.0),
        "L - Biên Lãi Thuần (NIM)": scale_val(nim, 2.0, 5.5),
    }


# =====================================================================
# 3. FINANCIAL HEALTH SCORECARD ALGORITHM
# =====================================================================

def compute_financial_health_scorecard(df_metrics: pd.DataFrame, latest_period: str = None) -> pd.DataFrame:
    """
    Thuật toán chấm điểm sức khỏe ngân hàng đa nhân tố (Thang điểm 100):
      - Trọng số Chất lượng Tài sản (Asset Quality): 35%
      - Trọng số Khả năng Sinh lời & Biên lợi nhuận (Profitability & NIM): 35%
      - Trọng số Nền tảng Vốn rẻ & Thương hiệu (CASA): 30%
    """
    if latest_period is None:
        latest_period = df_metrics["period"].max()

    df_p = df_metrics[df_metrics["period"] == latest_period].copy()

    scores = []
    insights = []
    tiers = []

    for _, row in df_p.iterrows():
        score = 0.0

        # 1. Chất lượng tài sản: NPL (20đ) + LLR (15đ)
        if row["npl_ratio"] <= 1.05: score += 20.0
        elif row["npl_ratio"] <= 1.50: score += 16.0
        elif row["npl_ratio"] <= 2.00: score += 11.0
        else: score += 6.0

        if row["llr_ratio"] >= 200.0: score += 15.0
        elif row["llr_ratio"] >= 150.0: score += 12.0
        elif row["llr_ratio"] >= 100.0: score += 9.0
        else: score += 5.0

        # 2. Khả năng sinh lời: NIM (15đ) + ROE (20đ)
        if row["nim"] >= 4.20: score += 15.0
        elif row["nim"] >= 3.60: score += 12.0
        elif row["nim"] >= 3.00: score += 9.0
        else: score += 6.0

        roe_val = row.get("roe_ttm", row["roe"])
        if roe_val >= 21.0: score += 20.0
        elif roe_val >= 17.5: score += 16.0
        elif roe_val >= 14.0: score += 12.0
        else: score += 8.0

        # 3. Nền tảng vốn rẻ CASA: (30đ)
        if row["casa_ratio"] >= 40.0: score += 30.0
        elif row["casa_ratio"] >= 35.0: score += 24.0
        elif row["casa_ratio"] >= 28.0: score += 18.0
        elif row["casa_ratio"] >= 20.0: score += 12.0
        else: score += 6.0

        scores.append(round(score, 1))

        if score >= 85.0:
            tiers.append("Tier 1 - Quán quân Toàn diện (Market Leader)")
            insights.append(
                f"{row['symbol']} đạt chuẩn xuất sắc: Biên lãi NIM {row['nim']}% cùng đệm bao phủ nợ LLR {row['llr_ratio']}% "
                f"vượt xa chuẩn an toàn Basel. Tỷ lệ CASA {row['casa_ratio']}% bảo chứng cho chi phí vốn rẻ vượt trội."
            )
        elif score >= 75.0:
            tiers.append("Tier 2 - Bứt phá Tăng trưởng (Strong Challenger)")
            insights.append(
                f"{row['symbol']} sở hữu sức sinh lời ấn tượng với ROE {roe_val}%. Tỷ lệ nợ xấu NPL {row['npl_ratio']}% "
                f"được kiểm soát tốt dưới ngưỡng điều hành 3% của NHNN."
            )
        elif score >= 65.0:
            tiers.append("Tier 3 - Quy mô Lớn - Thận trọng (Prudent Giant)")
            insights.append(
                f"{row['symbol']} đại diện cho quy mô tín dụng khổng lồ. Tuy NIM đạt {row['nim']}%, đệm dự phòng vững chắc "
                f"giúp ngân hàng duy trì vị thế cột trụ ổn định dòng vốn nền kinh tế."
            )
        else:
            tiers.append("Tier 4 - Cần Theo dõi (Watching)")
            insights.append(f"{row['symbol']} cần tối ưu thêm chi phí vốn và cải thiện chất lượng nợ nhóm 3-5.")

    df_p["health_score"] = scores
    df_p["rating_tier"] = tiers
    df_p["editorial_insight"] = insights

    df_p = df_p.sort_values(by="health_score", ascending=False).reset_index(drop=True)
    df_p["rank"] = range(1, len(df_p) + 1)
    return df_p
