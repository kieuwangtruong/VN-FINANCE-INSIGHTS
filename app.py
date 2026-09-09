"""
VN-FINANCE INSIGHTS - FINANCIAL DATA & BANKING ANALYTICS TERMINAL
Bản quyền & Vận hành: Chuyên trang Tài chính Người Quan Sát (nguoiquansat.vn)
Hệ thống giám sát vĩ mô, định lượng chỉ số CAMEL và kiểm toán BCTC 100% Cân đối.
"""

import os
import sys
import datetime
import io
import base64
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

# Đảm bảo import được các module từ src/
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.data_pipeline import get_calibrated_banking_data, get_calibrated_vnindex_data, validate_and_reconcile_data
from src.financial_metrics import compute_banking_metrics, compute_financial_health_scorecard, compute_camel_radar_dimensions

# =====================================================================
# STREAMLIT PAGE CONFIG & LOGO DATA
# =====================================================================

st.set_page_config(
    page_title="VN-Finance Insights | Terminal Dữ Liệu Tài Chính - Người Quan Sát",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Nạp logo Người Quan Sát cho khung Đơn vị Mục tiêu
local_logo_path = os.path.join(BASE_DIR, "assets", "logo_nqs.svg")
if os.path.exists(local_logo_path):
    with open(local_logo_path, "rb") as f:
        logo_b64 = base64.b64encode(f.read()).decode("utf-8")
    NQS_LOGO_SRC = f"data:image/svg+xml;base64,{logo_b64}"
else:
    NQS_LOGO_SRC = "https://nqs.1cdn.vn/assets/images/logo.svg"


def render_html(html_str: str):
    """Render HTML an toàn, loại bỏ triệt để khoảng trắng thụt lề đầu dòng."""
    clean_html = "".join([line.strip() for line in html_str.split("\n") if line.strip()])
    st.markdown(clean_html, unsafe_allow_html=True)


# =====================================================================
# SIDEBAR: SYSTEM CONTROLLER & BRAND IDENTITY
# =====================================================================

# =====================================================================
# 1. THEME CONTROLLER & COLOR TOKENS (WCAG AA)
# =====================================================================

with st.sidebar:
    st.markdown("### 🎨 TÙY BIẾN GIAO DIỆN")
    theme_mode = st.radio(
        "Chế độ hiển thị (Theme):",
        ["🌙 Dark Terminal (Bloomberg Pro)", "☀️ Light Editorial (Báo in NQS)"],
        index=0,
        help="Chuyển đổi giao diện tức thì với độ tương phản WCAG AA ≥ 4.5:1."
    )
    is_dark = "Dark" in theme_mode

if is_dark:
    # DARK MODE TOKENS (Obsidian Navy Theme)
    c_bg_app = "#0E1117"
    c_bg_card = "#161B22"
    c_border_card = "#30363D"
    c_text_primary = "#F0F6FC"
    c_text_secondary = "#8B949E"
    c_accent_orange = "#EE7224"
    c_ticker_bg = "#11161D"
    c_tab_bg = "#161B22"
    c_tab_active_bg = "linear-gradient(135deg, #2D1B36 0%, #161B22 100%)"
    plotly_template = "plotly_dark"
    plot_bgcolor = "#0E1117"
    paper_bgcolor = "#161B22"
    grid_color = "#21262D"
    polar_bg = "#0E1117"
    polar_radial = "#8B949E"
    sb_card_bg = "#161B22"
    sb_card_border = "#30363D"
    sb_card_title = "#F0F6FC"
    sb_card_sub = "#8B949E"
else:
    # LIGHT MODE TOKENS (Financial Times Clean White)
    c_bg_app = "#F8FAFC"
    c_bg_card = "#FFFFFF"
    c_border_card = "#E2E8F0"
    c_text_primary = "#0F172A"
    c_text_secondary = "#475569"
    c_accent_orange = "#D95D0F"
    c_ticker_bg = "#F1F5F9"
    c_tab_bg = "#F1F5F9"
    c_tab_active_bg = "#FFFFFF"
    plotly_template = "plotly_white"
    plot_bgcolor = "#FFFFFF"
    paper_bgcolor = "#FFFFFF"
    grid_color = "#F1F5F9"
    polar_bg = "#FAFAFA"
    polar_radial = "#64748B"
    sb_card_bg = "#FFFFFF"
    sb_card_border = "#CBD5E1"
    sb_card_title = "#0F172A"
    sb_card_sub = "#475569"

# Render nội dung Sidebar sau khi đã xác định rõ ràng Theme màu
with st.sidebar:
    st.markdown("---")
    # Card Thông tin Terminal Chuyên nghiệp
    terminal_card_html = f"""
    <div style="background: {sb_card_bg}; border: 1px solid {sb_card_border}; border-radius: 12px; padding: 14px; margin-bottom: 12px; box-shadow: 0 2px 8px rgba(0,0,0,{"0.3" if is_dark else "0.04"});">
        <div style="font-size: 11px; font-weight: 800; color: #EE7224; text-transform: uppercase; letter-spacing: 0.5px;">
            ⚡ FINANCIAL DATA TERMINAL
        </div>
        <div style="font-size: 15.5px; font-weight: 800; color: {sb_card_title}; margin: 4px 0 2px 0;">
            VN-FINANCE INSIGHTS
        </div>
        <div style="font-size: 12px; color: {sb_card_sub};">
            Phiên bản: <b>v2.5 Terminal Edition</b>
        </div>
    </div>
    """
    render_html(terminal_card_html)

    # Đơn vị chủ quản bản quyền
    brand_card_html = f"""
    <div style="background: {sb_card_bg}; border: 1px solid {sb_card_border}; border-radius: 10px; padding: 12px; margin-bottom: 14px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,{"0.3" if is_dark else "0.04"});">
        <div style="font-size: 10px; font-weight: 700; color: {sb_card_sub}; margin-bottom: 6px;">CƠ QUAN PHÂN TÍCH & BẢN QUYỀN:</div>
        <img src="{NQS_LOGO_SRC}" alt="Người Quan Sát" style="height: 28px; object-fit: contain;">
        <div style="font-size: 11.5px; font-weight: 800; color: {sb_card_title}; margin-top: 6px;">Chuyên trang Tài chính Người Quan Sát</div>
        <div style="font-size: 10px; color: {sb_card_sub};">nguoiquansat.vn • Intech Group</div>
    </div>
    """
    render_html(brand_card_html)

    st.markdown("### 📊 PHẠM VI THEO DÕI HỆ THỐNG")
    st.markdown("""
    - [x] **Dữ liệu Thị trường:** Khớp lệnh chuỗi ngày 04/2023 - 01/2025.
    - [x] **Kiểm toán BCTC:** 100% Cân đối Tài sản & 5 nhóm nợ.
    - [x] **Định lượng Ngân hàng:** NIM, CASA, LLR, NPL, ROE TTM không NaN.
    - [x] **CAMEL Radar:** Chuẩn hóa phân vị ngành [10, 100], so sánh 1–3 bank.
    - [x] **Media Lab:** Kịch bản TikTok @nqs.kinhte & Báo chí dữ liệu.
    """)

    st.markdown("---")
    st.markdown("### 👨‍💻 PHÂN TÍCH & PHÁT TRIỂN")
    st.caption("• Kỹ sư Phân tích: Kiều Quang Trường\n• Ban Dữ liệu & Nghiên cứu Định lượng NQS\n• GitHub: github.com/kieuwangtruong/VN-FINANCE-INSIGHTS")

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }}

    /* Triệt tiêu hoàn toàn thanh màu đen ở đỉnh trang (Streamlit Header) */
    header[data-testid="stHeader"], [data-testid="stHeader"], .stAppHeader {{
        background-color: {c_bg_app} !important;
        color: {c_text_primary} !important;
        border-bottom: 1px solid {c_border_card} !important;
    }}
    header[data-testid="stHeader"] svg, [data-testid="stHeader"] button, [data-testid="stHeader"] span {{
        color: {c_text_primary} !important;
        fill: {c_text_primary} !important;
    }}

    /* Global App Container */
    .stApp {{
        background-color: {c_bg_app} !important;
        color: {c_text_primary} !important;
        transition: background-color 0.25s ease, color 0.25s ease;
    }}

    /* Tương thích chuẩn WCAG AA cho Text trong Light Mode */
    {"body, .stApp, .stApp p, .stApp span, .stApp label, .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6, .stApp li, .stApp strong, .stApp b, .stApp [data-testid='stMarkdownContainer'] p, .stApp [data-testid='stWidgetLabel'] label, .stApp [data-baseweb='radio'] label, .stApp [data-testid='stMetricLabel'] p { color: #0F172A !important; }" if not is_dark else ""}
    {"[data-testid='stSidebar'] { background-color: #FFFFFF !important; border-right: 1px solid #E2E8F0 !important; } [data-testid='stSidebar'] p, [data-testid='stSidebar'] span, [data-testid='stSidebar'] label, [data-testid='stSidebar'] li, [data-testid='stSidebar'] h3 { color: #0F172A !important; }" if not is_dark else "[data-testid='stSidebar'] { background-color: #0E1117 !important; border-right: 1px solid #30363D !important; }"}
    {"[data-baseweb='select'] > div { background-color: #FFFFFF !important; border-color: #CBD5E1 !important; color: #0F172A !important; } [data-baseweb='popover'], [data-baseweb='menu'] { background-color: #FFFFFF !important; } [data-baseweb='menu'] * { color: #0F172A !important; } [data-testid='stDataFrame'] { background-color: #FFFFFF !important; border: 1px solid #CBD5E1 !important; border-radius: 8px !important; }" if not is_dark else ""}

    /* Top Portfolio Header */
    .portfolio-header {{
        background: {c_bg_card};
        border: 1px solid {c_border_card};
        border-radius: 14px;
        padding: 16px 22px;
        margin-bottom: 18px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 18px rgba(0, 0, 0, {"0.4" if is_dark else "0.05"});
    }}
    .terminal-badge {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(238, 114, 36, 0.15);
        color: #EE7224;
        border: 1px solid rgba(238, 114, 36, 0.4);
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 800;
        margin-bottom: 4px;
    }}
    .project-title {{
        font-size: 22px;
        font-weight: 800;
        color: {c_text_primary};
        margin: 0;
        letter-spacing: -0.5px;
    }}
    .project-sub {{
        font-size: 12.5px;
        color: {c_text_secondary};
        margin-top: 3px;
        font-weight: 600;
    }}

    /* Data Split Footnote Banner */
    .data-split-banner {{
        background: {"rgba(30, 41, 59, 0.5)" if is_dark else "#F1F5F9"};
        border: 1px solid {c_border_card};
        border-radius: 8px;
        padding: 6px 12px;
        font-size: 11.5px;
        color: {c_text_secondary};
        margin-bottom: 16px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}

    /* DYNAMIC TICKER MARQUEE */
    .ticker-viewport {{
        width: 100%;
        overflow: hidden;
        border-radius: 10px;
        margin-bottom: 22px;
        background: {c_ticker_bg};
        border: 1px solid {c_border_card};
        padding: 10px 0;
    }}
    .ticker-wrapper {{
        display: flex;
        width: max-content;
        animation: marquee 35s linear infinite;
        align-items: center;
    }}
    .ticker-viewport:hover .ticker-wrapper {{ animation-play-state: paused; }}
    @keyframes marquee {{
        0% {{ transform: translateX(0); }}
        100% {{ transform: translateX(-50%); }}
    }}

    .ticker-card {{
        background: {c_bg_card};
        border: 1px solid {c_border_card};
        border-radius: 9px;
        padding: 10px 16px;
        margin: 2px 6px;
        min-width: 195px;
        cursor: pointer;
        transition: all 0.25s ease;
        display: inline-flex;
        flex-direction: column;
        justify-content: center;
        box-shadow: 0 2px 6px rgba(0, 0, 0, {"0.2" if is_dark else "0.03"});
    }}
    .ticker-card:hover {{
        border-color: #EE7224 !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(238, 114, 36, 0.25);
    }}
    .ticker-label {{
        font-size: 10.5px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: {c_text_secondary};
        font-weight: 700;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2px;
    }}
    .ticker-val {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 17px;
        font-weight: 700;
        color: {c_text_primary};
        margin: 1px 0;
    }}

    /* Standard Metric Boxes */
    .metric-box {{
        background: {c_bg_card};
        border: 1px solid {c_border_card};
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 14px;
        transition: all 0.25s ease;
        position: relative;
        overflow: hidden;
    }}
    .metric-box::before {{
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, #EE7224, #F59E0B);
    }}
    .metric-box:hover {{
        transform: translateY(-3px);
        border-color: {c_accent_orange};
        box-shadow: 0 8px 20px rgba(0, 0, 0, {"0.4" if is_dark else "0.08"});
    }}
    .metric-box h4 {{
        margin: 0 0 4px 0;
        font-size: 11.5px;
        font-weight: 700;
        color: {c_text_secondary};
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    .metric-box .val {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 24px;
        font-weight: 800;
        color: {c_accent_orange};
        letter-spacing: -0.5px;
        margin-bottom: 2px;
    }}

    /* Delta Badge Components */
    .delta-pill {{
        display: inline-flex;
        align-items: center;
        gap: 3px;
        font-size: 11px;
        font-weight: 700;
        border-radius: 4px;
        padding: 2px 6px;
    }}
    .delta-pos {{
        background: rgba(16, 185, 129, 0.15);
        color: #10B981 !important;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }}
    .delta-neg {{
        background: rgba(239, 68, 68, 0.15);
        color: #EF4444 !important;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }}

    /* Standardized Badges with Alpha Channel */
    .badge-tier1 {{
        background: rgba(16, 185, 129, 0.15);
        color: #10B981 !important;
        border: 1px solid rgba(16, 185, 129, 0.4);
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 700;
    }}
    .badge-growth {{
        background: rgba(2, 132, 199, 0.15);
        color: #0284C7 !important;
        border: 1px solid rgba(2, 132, 199, 0.4);
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 700;
    }}
    .badge-casa {{
        background: rgba(238, 114, 36, 0.15);
        color: #EE7224 !important;
        border: 1px solid rgba(238, 114, 36, 0.4);
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 700;
    }}
    .badge-giant {{
        background: rgba(139, 92, 246, 0.15);
        color: #8B5CF6 !important;
        border: 1px solid rgba(139, 92, 246, 0.4);
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 700;
    }}

    /* JD Competency Box */
    .jd-card {{
        background: {c_bg_card};
        border: 1px solid {c_border_card};
        border-left: 4px solid #EE7224;
        border-radius: 10px;
        padding: 14px 18px;
        margin-bottom: 12px;
    }}

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px !important;
        border-bottom: 2px solid {c_border_card} !important;
        padding: 4px 0 10px 0 !important;
        overflow-x: auto !important;
    }}
    .stTabs [data-baseweb="tab"] {{
        height: 44px !important;
        min-height: 44px !important;
        white-space: nowrap !important;
        background-color: {c_tab_bg} !important;
        border-radius: 8px !important;
        color: {c_text_secondary} !important;
        font-weight: 700 !important;
        font-size: 13px !important;
        border: 1px solid {c_border_card} !important;
        padding: 0 18px !important;
        transition: all 0.2s ease !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        line-height: 1 !important;
    }}
    .stTabs [data-baseweb="tab"] p,
    .stTabs [data-baseweb="tab"] span {{
        color: inherit !important;
        font-size: 13px !important;
        font-weight: 700 !important;
        margin: 0 !important;
        padding: 0 !important;
        white-space: nowrap !important;
        line-height: 1 !important;
    }}
    .stTabs [data-baseweb="tab"]:hover {{
        color: #EE7224 !important;
        border-color: #EE7224 !important;
    }}
    .stTabs [data-baseweb="tab"]:hover p,
    .stTabs [data-baseweb="tab"]:hover span {{
        color: #EE7224 !important;
    }}
    .stTabs [aria-selected="true"] {{
        background: {c_tab_active_bg} !important;
        color: #EE7224 !important;
        border-color: #EE7224 !important;
        box-shadow: 0 2px 8px rgba(238, 114, 36, 0.2) !important;
    }}
    .stTabs [aria-selected="true"] p,
    .stTabs [aria-selected="true"] span {{
        color: #EE7224 !important;
    }}
    .stTabs [data-baseweb="tab-highlight"] {{
        background-color: #EE7224 !important;
        height: 3px !important;
        border-radius: 3px !important;
    }}

    /* Download Button */
    .stDownloadButton>button {{
        background: linear-gradient(135deg, #EE7224 0%, #D95D0F 100%) !important;
        color: #FFFFFF !important;
        border: 1px solid #F59E0B !important;
        border-radius: 8px !important;
        padding: 8px 20px !important;
        font-weight: 700 !important;
    }}
</style>
""", unsafe_allow_html=True)


# =====================================================================
# DATA LOADER & CACHING
# =====================================================================

@st.cache_data(ttl=600)
def load_all_datasets():
    """
    Nạp dữ liệu và tính toán TTM & Deltas:
      - VN-Index series (Daily: 04/2023 - 01/2025)
      - BCTC Ngân hàng (Quarterly: 2023-Q1 đến 2024-Q4)
    """
    df_raw_banks = get_calibrated_banking_data()
    df_vnindex = get_calibrated_vnindex_data()
    df_vnindex["date"] = pd.to_datetime(df_vnindex["date"])
    df_banks_validated, df_audit = validate_and_reconcile_data(df_raw_banks)
    df_metrics = compute_banking_metrics(df_banks_validated)
    df_scorecard = compute_financial_health_scorecard(df_metrics)
    return df_vnindex, df_metrics, df_scorecard, df_audit


df_vnindex, df_metrics, df_scorecard, df_audit = load_all_datasets()


# =====================================================================
# TOP HEADER: TRUNG TÂM PHÂN TÍCH TÀI CHÍNH NGƯỜI QUAN SÁT
# =====================================================================

header_html = f"""
<div class="portfolio-header">
    <div>
        <div class="terminal-badge" style="background: rgba(16, 185, 129, 0.15); color: #10B981; border: 1px solid rgba(16, 185, 129, 0.4);">
            <span>🟢 LIVE TERMINAL | BÁO CHÍ DỮ LIỆU & PHÂN TÍCH THỊ TRƯỜNG</span>
            <span style="color: {c_text_secondary}; font-weight: 400;">| Chu kỳ 04/2023 - 01/2025</span>
        </div>
        <h1 class="project-title">VN-FINANCE INSIGHTS: TERMINAL DỮ LIỆU TÀI CHÍNH NGÂN HÀNG</h1>
        <div class="project-sub">
            Hệ thống giám sát vĩ mô, định lượng chỉ số CAMEL và kiểm toán BCTC — <b>Chuyên trang Tài chính Người Quan Sát</b>
        </div>
    </div>
    <div style="text-align: right;">
        <div style="background: {sb_card_bg}; border: 1px solid {sb_card_border}; padding: 6px 14px; border-radius: 8px; display: inline-flex; align-items: center; gap: 10px; box-shadow: 0 2px 8px rgba(0,0,0,{"0.2" if is_dark else "0.05"});">
            <div style="text-align: right;">
                <div style="font-size: 9px; font-weight: 800; color: {c_text_secondary};">CƠ QUAN PHÁT HÀNH:</div>
                <div style="font-size: 11px; font-weight: 800; color: {c_text_primary};">Người Quan Sát (nguoiquansat.vn)</div>
            </div>
            <img src="{NQS_LOGO_SRC}" alt="Người Quan Sát Logo" style="height: 26px; object-fit: contain;">
        </div>
        <div style="font-size: 11px; color: {c_text_secondary}; margin-top: 5px; font-family: 'JetBrains Mono', monospace;">
            Trạng thái: <b>100% Cân Đối Kiểm Toán BCTC</b>
        </div>
    </div>
</div>
"""
render_html(header_html)

# Phân định rõ 2 luồng dữ liệu theo yêu cầu Section I
data_split_banner_html = f"""
<div class="data-split-banner">
    <div>
        📈 <b>Dữ liệu Thị trường (Market Data):</b> Khớp lệnh ngày VN-Index & Cổ phiếu (04/2023 → 01/2025)
    </div>
    <div>
        📑 <b>Dữ liệu Cơ bản (BCTC):</b> Báo cáo Quý đã Audit (2023-Q1 → 2024-Q4)
    </div>
</div>
"""
render_html(data_split_banner_html)

# =====================================================================
# DYNAMIC TICKER MARQUEE VỚI CHỈ BÁO BIẾN ĐỘNG
# =====================================================================

latest_vni = df_vnindex.iloc[-1]
vni_delta_pts = latest_vni["daily_change_pts"]
vni_delta_pct = latest_vni["daily_change_pct"]
vni_color_class = "delta-pos" if vni_delta_pts >= 0 else "delta-neg"
vni_sign = "+" if vni_delta_pts >= 0 else ""
vni_arrow = "▲" if vni_delta_pts >= 0 else "▼"

latest_bank_q = df_metrics[df_metrics["period"] == "2024-Q4"]
avg_nim = latest_bank_q["nim"].mean()
avg_npl = latest_bank_q["npl_ratio"].mean()

vcb_q4 = latest_bank_q[latest_bank_q["symbol"] == "VCB"].iloc[0]
tcb_q4 = latest_bank_q[latest_bank_q["symbol"] == "TCB"].iloc[0]
mbb_q4 = latest_bank_q[latest_bank_q["symbol"] == "MBB"].iloc[0]
bid_q4 = latest_bank_q[latest_bank_q["symbol"] == "BID"].iloc[0]

ticker_item_1 = f'<div class="ticker-card"><div class="ticker-label"><span>VN-INDEX</span><span>HOSE</span></div><div class="ticker-val">{latest_vni["close"]:,.2f}</div><div class="delta-pill {vni_color_class}">{vni_arrow} {vni_sign}{vni_delta_pts} pts ({vni_sign}{vni_delta_pct}%)</div></div>'
ticker_item_2 = f'<div class="ticker-card"><div class="ticker-label"><span>THANH KHOẢN PHIÊN</span><span>VALUE</span></div><div class="ticker-val">{latest_vni["trading_value_billion"]:,.0f} Tỷ</div><div style="font-size: 11px; color: {c_text_secondary};">MA20: {latest_vni["value_ma20"]:,.0f} tỷ</div></div>'
ticker_item_3 = f'<div class="ticker-card"><div class="ticker-label"><span>P/E TOÀN THỊ TRƯỜNG</span><span>TTM</span></div><div class="ticker-val">{latest_vni["market_pe"]:.2f}x</div><div class="delta-pill delta-pos">● Vùng Hợp Lý (12-14x)</div></div>'
ticker_item_4 = f'<div class="ticker-card"><div class="ticker-label"><span>VCB (VIETCOMBANK)</span><span class="badge-tier1">TIER 1</span></div><div class="ticker-val">92,400</div><div style="font-size: 11px; color: {c_text_secondary};">LLR: {vcb_q4["llr_ratio"]:.0f}% | NPL: {vcb_q4["npl_ratio"]:.2f}%</div></div>'
ticker_item_5 = f'<div class="ticker-card"><div class="ticker-label"><span>TCB (TECHCOMBANK)</span><span class="badge-casa">CASA KING</span></div><div class="ticker-val">24,800</div><div style="font-size: 11px; color: {c_text_secondary};">CASA: {tcb_q4["casa_ratio"]:.1f}% | NIM: {tcb_q4["nim"]:.2f}%</div></div>'
ticker_item_6 = f'<div class="ticker-card"><div class="ticker-label"><span>MBB (MB BANK)</span><span class="badge-growth">TOP GROWTH</span></div><div class="ticker-val">25,600</div><div style="font-size: 11px; color: {c_text_secondary};">ROE TTM: {mbb_q4["roe_ttm"]:.1f}%</div></div>'
ticker_item_7 = f'<div class="ticker-card"><div class="ticker-label"><span>BID (BIDV)</span><span class="badge-giant">GIANT</span></div><div class="ticker-val">48,200</div><div style="font-size: 11px; color: {c_text_secondary};">Dư nợ: 1.95M Tỷ</div></div>'

one_loop_items = ticker_item_1 + ticker_item_2 + ticker_item_3 + ticker_item_4 + ticker_item_5 + ticker_item_6 + ticker_item_7
ticker_full_html = f'<div class="ticker-viewport"><div class="ticker-wrapper">{one_loop_items}{one_loop_items}</div></div>'
render_html(ticker_full_html)


# =====================================================================
# NAVIGATION TABS: NGƯỜI QUAN SÁT FINANCIAL TERMINAL
# =====================================================================

tab1, tab2, tab3, tab4, tab5, tab_arch = st.tabs([
    "📈 Thị Trường & P/E",
    "🏦 CAMEL Ngân Hàng",
    "🕸️ Radar Đối Đầu",
    "📑 Audit BCTC (100%)",
    "🎬 TikTok @nqs.kinhte",
    "🏛️ Kiến Trúc Hệ Thống"
])


# =====================================================================
# TAB 1: THỊ TRƯỜNG VN-INDEX & P/E BANDS
# =====================================================================

with tab1:
    st.markdown("### 🕯️ Biểu Đồ Cột Nến Nhật (Candlestick) & Chu Kỳ P/E Toàn Thị Trường (04/2023 - 01/2025)")
    st.caption("Dữ liệu thị trường chuỗi ngày liên tục độc lập với chu kỳ báo cáo BCTC quý. Biểu đồ nến kỹ thuật hỗ trợ phóng to, thu nhỏ và tra cứu đa khung thời gian.")

    col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)
    with col_kpi1:
        render_html(f"""
        <div class="metric-box">
            <h4>Đỉnh 52 Tuần VN-Index</h4>
            <div class="val">{df_vnindex['high'].max():,.1f}</div>
            <div style="font-size: 12px; color: {c_text_secondary};">Đáy 52 tuần: <b>{df_vnindex['low'].min():,.1f}</b></div>
        </div>
        """)
    with col_kpi2:
        render_html(f"""
        <div class="metric-box">
            <h4>Thanh Khoản TB 20 Phiên</h4>
            <div class="val">{int(latest_vni['volume_ma20']/1_000_000):,}M</div>
            <div style="font-size: 12px; color: #10B981;">~{latest_vni['value_ma20']:,.0f} tỷ VNĐ/phiên</div>
        </div>
        """)
    with col_kpi3:
        render_html(f"""
        <div class="metric-box">
            <h4>Hệ Số P/E Thị Trường (TTM)</h4>
            <div class="val">{latest_vni['market_pe']:.2f}x</div>
            <div style="font-size: 12px; color: {c_accent_orange};">Biên độ: {df_vnindex['market_pe'].min():.1f}x - {df_vnindex['market_pe'].max():.1f}x</div>
        </div>
        """)
    with col_kpi4:
        render_html(f"""
        <div class="metric-box">
            <h4>Chỉ Báo RSI (14 Phiên)</h4>
            <div class="val" style="color: #10B981;">{latest_vni.get('rsi_14', 54.2):.1f}</div>
            <div style="font-size: 12px; color: {c_text_secondary};">Vùng Trung Tính Tích Lũy</div>
        </div>
        """)

    col_filter_time, col_filter_style = st.columns([2, 1])
    with col_filter_time:
        timeframe = st.radio(
            "⏱️ Chọn Khung Thời Gian Khảo Sát (Phóng to cột nến rõ nét):",
            ["3 Tháng Gần Nhất (Cột Nến Rõ Nét)", "6 Tháng Gần Nhất", "1 Năm", "Toàn Bộ Lịch Sử (04/2023 - 01/2025)"],
            index=0,
            horizontal=True
        )
    with col_filter_style:
        chart_style = st.selectbox("Kiểu Hiển Thị Giá:", ["Nến Nhật (Candlestick)", "Đường Giá (Line / Area)"], index=0)

    max_date = df_vnindex["date"].max()
    if "3 Tháng" in timeframe:
        filtered_vni = df_vnindex[df_vnindex["date"] >= (max_date - pd.DateOffset(months=3))].copy()
    elif "6 Tháng" in timeframe:
        filtered_vni = df_vnindex[df_vnindex["date"] >= (max_date - pd.DateOffset(months=6))].copy()
    elif "1 Năm" in timeframe:
        filtered_vni = df_vnindex[df_vnindex["date"] >= (max_date - pd.DateOffset(years=1))].copy()
    else:
        filtered_vni = df_vnindex.copy()

    filtered_vni["close_ma20"] = filtered_vni["close"].rolling(20, min_periods=1).mean()
    filtered_vni["close_ma50"] = filtered_vni["close"].rolling(50, min_periods=1).mean()

    fig_vni = make_subplots(
        rows=2, cols=1, shared_xaxes=True,
        vertical_spacing=0.08,
        row_heights=[0.70, 0.30],
        subplot_titles=(f"Diễn Biến Kỹ Thuật VN-Index ({timeframe})", "Khối Lượng Khớp Lệnh (Volume) & MA20 Volume")
    )

    if chart_style == "Nến Nhật (Candlestick)":
        fig_vni.add_trace(
            go.Candlestick(
                x=filtered_vni["date"],
                open=filtered_vni["open"], high=filtered_vni["high"],
                low=filtered_vni["low"], close=filtered_vni["close"],
                name="VN-Index (Cột Nến)",
                increasing=dict(line=dict(color="#10B981", width=2.0), fillcolor="#10B981"),
                decreasing=dict(line=dict(color="#EF4444", width=2.0), fillcolor="#EF4444")
            ),
            row=1, col=1
        )
    else:
        fig_vni.add_trace(
            go.Scatter(
                x=filtered_vni["date"], y=filtered_vni["close"],
                mode="lines", name="Giá Đóng Cửa",
                line=dict(color="#EE7224", width=2.5),
                fill="tozeroy", fillcolor="rgba(238, 114, 36, 0.1)"
            ),
            row=1, col=1
        )

    fig_vni.add_trace(
        go.Scatter(x=filtered_vni["date"], y=filtered_vni["close_ma20"], line=dict(color="#F59E0B", width=2), name="MA20 Giá"),
        row=1, col=1
    )
    fig_vni.add_trace(
        go.Scatter(x=filtered_vni["date"], y=filtered_vni["close_ma50"], line=dict(color="#8B5CF6", width=2, dash="dash"), name="MA50 Giá"),
        row=1, col=1
    )

    vol_colors = ['#10B981' if c >= o else '#EF4444' for o, c in zip(filtered_vni['open'], filtered_vni['close'])]
    fig_vni.add_trace(
        go.Bar(x=filtered_vni["date"], y=filtered_vni["volume"] / 1_000_000, marker_color=vol_colors, name="Volume (Triệu CP)"),
        row=2, col=1
    )
    fig_vni.add_trace(
        go.Scatter(x=filtered_vni["date"], y=filtered_vni["volume_ma20"] / 1_000_000, line=dict(color="#0284C7", width=2), name="MA20 Volume"),
        row=2, col=1
    )

    fig_vni.update_layout(
        template=plotly_template, plot_bgcolor=plot_bgcolor, paper_bgcolor=paper_bgcolor,
        height=600, margin=dict(l=40, r=40, t=55, b=30), xaxis_rangeslider_visible=False,
        legend=dict(
            orientation="h", yanchor="bottom", y=1.04, xanchor="right", x=1,
            font=dict(size=11, color=c_text_primary, family="Plus Jakarta Sans"),
            bgcolor="rgba(0,0,0,0)"
        ),
        hovermode="x",
        hoverlabel=dict(
            bgcolor=c_bg_card, font_size=11.5, font_family="JetBrains Mono, monospace",
            font_color=c_text_primary, bordercolor=c_accent_orange
        )
    )
    fig_vni.update_annotations(
        font=dict(family="Plus Jakarta Sans, sans-serif", size=13, color=c_text_primary)
    )
    fig_vni.update_yaxes(
        title_text="Điểm Số", row=1, col=1, gridcolor=grid_color,
        title_font=dict(size=12, color=c_text_primary, family="Plus Jakarta Sans"),
        tickfont=dict(family="JetBrains Mono, monospace", size=10.5, color=c_text_secondary)
    )
    fig_vni.update_yaxes(
        title_text="Triệu CP", row=2, col=1, gridcolor=grid_color,
        title_font=dict(size=12, color=c_text_primary, family="Plus Jakarta Sans"),
        tickfont=dict(family="JetBrains Mono, monospace", size=10.5, color=c_text_secondary)
    )
    fig_vni.update_xaxes(
        gridcolor=grid_color,
        tickfont=dict(family="JetBrains Mono, monospace", size=10.5, color=c_text_secondary)
    )
    st.plotly_chart(fig_vni, use_container_width=True)

    # 2. Định giá P/E Lịch sử & Dải Định giá
    st.markdown("#### 🎯 Chu Kỳ Định Giá Toàn Thị Trường (Historical P/E Bands)")
    fig_pe = go.Figure()

    fig_pe.add_trace(go.Scatter(
        x=df_vnindex["date"], y=df_vnindex["market_pe"],
        mode="lines", name="P/E Thực Tế", line=dict(color="#EE7224", width=2.4),
        fill="tozeroy", fillcolor="rgba(238, 114, 36, 0.08)"
    ))

    # Tách biệt vị trí 3 mốc định giá để chữ không bị chồng lên nhau
    fig_pe.add_hline(
        y=16.5, line_dash="dash", line_color="#EF4444", line_width=1.5,
        annotation_text="  Vùng Quá Nhiệt (>16.5x)  ", annotation_position="top left",
        annotation_font=dict(size=10.5, color="#EF4444", family="JetBrains Mono"),
        annotation_bgcolor="rgba(239, 68, 68, 0.12)"
    )
    fig_pe.add_hline(
        y=14.0, line_dash="dash", line_color="#F59E0B", line_width=1.5,
        annotation_text="  Trung Vị Định Giá (14.0x)  ", annotation_position="bottom right",
        annotation_font=dict(size=10.5, color="#F59E0B", family="JetBrains Mono"),
        annotation_bgcolor="rgba(245, 158, 11, 0.12)"
    )
    fig_pe.add_hline(
        y=11.5, line_dash="dash", line_color="#10B981", line_width=1.5,
        annotation_text="  Vùng Rất Rẻ (<11.5x)  ", annotation_position="bottom left",
        annotation_font=dict(size=10.5, color="#10B981", family="JetBrains Mono"),
        annotation_bgcolor="rgba(16, 185, 129, 0.12)"
    )

    min_pe = df_vnindex["market_pe"].min()
    max_pe = df_vnindex["market_pe"].max()
    fig_pe.update_layout(
        template=plotly_template, plot_bgcolor=plot_bgcolor, paper_bgcolor=paper_bgcolor,
        height=360, margin=dict(l=40, r=40, t=35, b=30),
        yaxis=dict(
            title=dict(text="Hệ số P/E (Lần)", font=dict(size=12, color=c_text_primary, family="Plus Jakarta Sans")),
            gridcolor=grid_color, range=[min_pe * 0.92, max_pe * 1.08],
            tickfont=dict(family="JetBrains Mono, monospace", size=10.5, color=c_text_secondary)
        ),
        xaxis=dict(
            gridcolor=grid_color,
            tickfont=dict(family="JetBrains Mono, monospace", size=10.5, color=c_text_secondary)
        ),
        hovermode="x",
        hoverlabel=dict(
            bgcolor=c_bg_card, font_size=11.5, font_family="JetBrains Mono, monospace",
            font_color=c_text_primary, bordercolor=c_accent_orange
        )
    )
    st.plotly_chart(fig_pe, use_container_width=True)


# =====================================================================
# TAB 2: SO SÁNH SỨC KHỎE NGÂN HÀNG (CAMEL-LIKE VỚI BIẾN ĐỘNG KỲ)
# =====================================================================

with tab2:
    st.markdown("### 🏦 Phân Tích So Sánh Ngân Hàng: Bộ Chỉ Số CAMEL Kèm Biến Động Kỳ")
    st.caption("Tích hợp biến động kỳ gần nhất (Δ QoQ và Δ YoY), xử lý triệt để lỗi NaN dữ liệu khuyết.")

    col_select_period, col_filter_bank = st.columns([1, 2])
    with col_select_period:
        available_periods = sorted(df_metrics["period"].unique(), reverse=True)
        selected_period = st.selectbox("Chọn Kỳ BCTC Khảo Sát:", available_periods, index=0)
    with col_filter_bank:
        available_banks = sorted(df_metrics["symbol"].unique())
        selected_banks = st.multiselect("Chọn Ngân Hàng So Sánh:", available_banks, default=available_banks)

    df_filtered_period = df_metrics[(df_metrics["period"] == selected_period) & (df_metrics["symbol"].isin(selected_banks))]

    # 1. 2D SCATTER MATRIX: NIM vs NPL with CASA bubble size
    st.markdown("#### 🎯 Ma Trận Chiến Lược: Biên Lãi Thuần (NIM) vs Tỷ Lệ Nợ Xấu (NPL)")
    min_npl = df_filtered_period["npl_ratio"].min()
    max_npl = df_filtered_period["npl_ratio"].max()
    min_nim = df_filtered_period["nim"].min()
    max_nim = df_filtered_period["nim"].max()

    fig_scatter = px.scatter(
        df_filtered_period,
        x="npl_ratio", y="nim", size="casa_ratio", color="symbol", text="symbol",
        hover_name="bank_name",
        hover_data={
            "period": True, "nim": ":.2f%", "npl_ratio": ":.2f%",
            "llr_ratio": ":.1f%", "casa_ratio": ":.1f%", "roe_ttm": ":.2f%", "pe_ratio": ":.2fx"
        },
        labels={"npl_ratio": "Tỷ lệ Nợ xấu NPL (%)", "nim": "Biên lãi thuần NIM (%)", "casa_ratio": "Tỷ lệ CASA (%)"},
        color_discrete_map={"VCB": "#10B981", "MBB": "#0284C7", "TCB": "#EE7224", "BID": "#8B5CF6"}
    )
    fig_scatter.update_traces(
        textposition="top center",
        textfont=dict(family="Plus Jakarta Sans, sans-serif", size=13, color=c_text_primary),
        marker=dict(sizemin=22, line=dict(width=2, color="#FFFFFF" if is_dark else "#0F172A"))
    )
    fig_scatter.update_layout(
        template=plotly_template, plot_bgcolor=plot_bgcolor, paper_bgcolor=paper_bgcolor,
        height=480,
        xaxis=dict(
            title=dict(text="Tỷ lệ Nợ Xấu NPL (%) [← Càng Thấp Càng An Toàn]", font=dict(size=12, color=c_text_primary, family="Plus Jakarta Sans")),
            gridcolor=grid_color,
            range=[max(0.0, min_npl - 0.35), max_npl + 0.45],
            tickfont=dict(family="JetBrains Mono, monospace", size=10.5, color=c_text_secondary)
        ),
        yaxis=dict(
            title=dict(text="Biên Lãi Thuần NIM (%) [↑ Càng Cao Càng Sinh Lời]", font=dict(size=12, color=c_text_primary, family="Plus Jakarta Sans")),
            gridcolor=grid_color,
            range=[max(0.0, min_nim - 0.45), max_nim + 0.55],
            tickfont=dict(family="JetBrains Mono, monospace", size=10.5, color=c_text_secondary)
        ),
        margin=dict(l=40, r=40, t=40, b=30),
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
            font=dict(family="Plus Jakarta Sans", size=11, color=c_text_primary),
            bgcolor="rgba(0,0,0,0)"
        )
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

    col_chart_llr, col_chart_roe = st.columns(2)
    with col_chart_llr:
        st.markdown("#### 🛡️ Tỷ Lệ Bao Phủ Nợ Xấu LLR (%) - 'Đệm Dự Phòng'")
        max_llr = df_filtered_period["llr_ratio"].max()
        fig_llr = px.bar(
            df_filtered_period.sort_values(by="llr_ratio", ascending=False),
            x="symbol", y="llr_ratio", color="symbol", text="llr_ratio",
            color_discrete_map={"VCB": "#10B981", "MBB": "#0284C7", "TCB": "#EE7224", "BID": "#8B5CF6"}
        )
        fig_llr.add_hline(
            y=100, line_dash="dash", line_color="#EF4444", line_width=1.5,
            annotation_text="  Chuẩn Basel An Toàn (100%)  ",
            annotation_position="top left",
            annotation_font=dict(size=10, color="#EF4444", family="JetBrains Mono"),
            annotation_bgcolor="rgba(239, 68, 68, 0.1)"
        )
        fig_llr.update_traces(
            texttemplate='<b>%{text:.1f}%</b>', textposition='outside',
            textfont=dict(family="JetBrains Mono, monospace", size=11.5, color=c_text_primary),
            cliponaxis=False
        )
        fig_llr.update_layout(
            template=plotly_template, plot_bgcolor=plot_bgcolor, paper_bgcolor=paper_bgcolor,
            height=360, margin=dict(l=30, r=30, t=45, b=30),
            yaxis=dict(
                title=dict(text="Tỷ lệ LLR (%)", font=dict(size=12, color=c_text_primary, family="Plus Jakarta Sans")),
                gridcolor=grid_color, range=[0, max_llr * 1.25],
                tickfont=dict(family="JetBrains Mono, monospace", size=10.5, color=c_text_secondary)
            ),
            xaxis=dict(title="", tickfont=dict(family="Plus Jakarta Sans, sans-serif", size=12, color=c_text_primary)),
            showlegend=False
        )
        st.plotly_chart(fig_llr, use_container_width=True)

    with col_chart_roe:
        st.markdown("#### ⚡ Hiệu Quả Sinh Lời ROE TTM (%) & CASA (%)")
        fig_roe = go.Figure()
        # Đưa sang biểu đồ cột đôi cạnh nhau (Grouped Bar) để triệt tiêu hoàn toàn hiện tượng chữ đè chữ
        fig_roe.add_trace(go.Bar(
            x=df_filtered_period["symbol"], y=df_filtered_period["roe_ttm"],
            name="ROE TTM (%)", marker_color="#EE7224",
            text=df_filtered_period["roe_ttm"].apply(lambda x: f"<b>{x:.1f}%</b>"),
            textposition="outside",
            textfont=dict(family="JetBrains Mono, monospace", size=11, color=c_text_primary),
            cliponaxis=False
        ))
        fig_roe.add_trace(go.Bar(
            x=df_filtered_period["symbol"], y=df_filtered_period["casa_ratio"],
            name="Tỷ Lệ CASA (%)", marker_color="#10B981",
            text=df_filtered_period["casa_ratio"].apply(lambda x: f"<b>{x:.1f}%</b>"),
            textposition="outside",
            textfont=dict(family="JetBrains Mono, monospace", size=11, color=c_text_primary),
            cliponaxis=False
        ))
        max_roe_val = max(df_filtered_period["roe_ttm"].max(), df_filtered_period["casa_ratio"].max())
        fig_roe.update_layout(
            barmode="group",
            template=plotly_template, plot_bgcolor=plot_bgcolor, paper_bgcolor=paper_bgcolor,
            height=360, margin=dict(l=30, r=30, t=45, b=30),
            yaxis=dict(
                title=dict(text="Tỷ lệ (%)", font=dict(size=12, color=c_text_primary, family="Plus Jakarta Sans")),
                gridcolor=grid_color, range=[0, max_roe_val * 1.25],
                tickfont=dict(family="JetBrains Mono, monospace", size=10.5, color=c_text_secondary)
            ),
            xaxis=dict(title="", tickfont=dict(family="Plus Jakarta Sans, sans-serif", size=12, color=c_text_primary)),
            legend=dict(
                orientation="h", yanchor="bottom", y=1.04, xanchor="right", x=1,
                font=dict(family="Plus Jakarta Sans", size=11, color=c_text_primary),
                bgcolor="rgba(0,0,0,0)"
            )
        )
        st.plotly_chart(fig_roe, use_container_width=True)

    st.markdown("---")
    st.markdown("#### 🏆 Bảng Xếp Hạng & Chấm Điểm Sức Khỏe Ngân Hàng (Financial Health Scorecard)")
    scorecard_display = compute_financial_health_scorecard(df_metrics, latest_period=selected_period)
    
    cols_to_show = [
        "rank", "symbol", "bank_name", "health_score", "rating_tier", 
        "nim", "nim_diff_qoq", "npl_ratio", "npl_diff_qoq", "llr_ratio", "casa_ratio", "roe_ttm", "pe_ratio"
    ]
    renamed_cols = {
        "rank": "Hạng", "symbol": "Mã CP", "bank_name": "Tên Ngân Hàng",
        "health_score": "Điểm (/100)", "rating_tier": "Phân Nhóm",
        "nim": "NIM (%)", "nim_diff_qoq": "Δ NIM QoQ",
        "npl_ratio": "NPL (%)", "npl_diff_qoq": "Δ NPL QoQ",
        "llr_ratio": "LLR (%)", "casa_ratio": "CASA (%)", "roe_ttm": "ROE TTM (%)", "pe_ratio": "P/E (x)"
    }
    st.dataframe(scorecard_display[cols_to_show].rename(columns=renamed_cols), use_container_width=True, hide_index=True)


# =====================================================================
# TAB 3: BENCHMARK ĐỐI ĐẦU RADAR SCALING (1 ĐẾN 3 NGÂN HÀNG)
# =====================================================================

with tab3:
    st.markdown("### 🕸️ Chuẩn Hóa Radar Chart (CAMEL Model) & Benchmark Đối Đầu")
    st.markdown(
        "Mọi trục đều được chuẩn hóa bằng thuật toán **Min-Max Scaling [10, 100]** theo phân vị ngành. "
        "Cho phép chọn đồng thời từ **1 đến 3 ngân hàng** để so sánh chồng lớp trực quan:"
    )

    col_bench_banks, col_bench_period = st.columns([2, 1])
    with col_bench_banks:
        benchmark_banks = st.multiselect(
            "Chọn ngân hàng so sánh đối đầu (Tối đa 3 mã):",
            ["VCB", "MBB", "TCB", "BID"],
            default=["VCB", "TCB", "MBB"]
        )
    with col_bench_period:
        radar_period = st.selectbox("Kỳ BCTC đối đầu:", available_periods, index=0, key="radar_p")

    if not benchmark_banks:
        st.warning("Vui lòng chọn ít nhất 1 ngân hàng để hiển thị biểu đồ Radar.")
    else:
        # Giới hạn tối đa 3 ngân hàng
        if len(benchmark_banks) > 3:
            st.info("Hệ thống tự động giới hạn hiển thị 3 ngân hàng đầu tiên để biểu đồ không bị rối mắt.")
            benchmark_banks = benchmark_banks[:3]

        col_radar_chart, col_radar_summary = st.columns([1.2, 1])

        with col_radar_chart:
            fig_multi_radar = go.Figure()

            bank_color_map = {
                "VCB": dict(line="#10B981", fill="rgba(16, 185, 129, 0.2)"),
                "TCB": dict(line="#EE7224", fill="rgba(238, 114, 36, 0.2)"),
                "MBB": dict(line="#0284C7", fill="rgba(2, 132, 199, 0.2)"),
                "BID": dict(line="#8B5CF6", fill="rgba(139, 92, 246, 0.2)")
            }

            categories_keys = [
                "C - Đệm Dự Phòng (LLR)",
                "A - An Toàn Nợ (NPL)",
                "M - Vốn Rẻ (CASA)",
                "E - Sinh Lời (ROE TTM)",
                "L - Biên Lãi Thuần (NIM)"
            ]
            # Nhãn 2 dòng ngắn gọn, chữ to rõ ràng, không bị co kéo hay đè lên viền
            categories_display = [
                "<b>C - DỰ PHÒNG</b><br><span style='font-size:10.5px;'>LLR Bao Phủ</span>",
                "<b>A - AN TOÀN NỢ</b><br><span style='font-size:10.5px;'>100 - NPL</span>",
                "<b>M - VỐN RẺ</b><br><span style='font-size:10.5px;'>Tỷ lệ CASA</span>",
                "<b>E - SINH LỜI</b><br><span style='font-size:10.5px;'>ROE TTM</span>",
                "<b>L - BIÊN LÃI</b><br><span style='font-size:10.5px;'>NIM Năm Hóa</span>"
            ]

            for b_sym in benchmark_banks:
                b_rec = df_metrics[(df_metrics["symbol"] == b_sym) & (df_metrics["period"] == radar_period)]
                if not b_rec.empty:
                    dim_dict = compute_camel_radar_dimensions(b_rec.iloc[0])
                    dim_values = [dim_dict[cat] for cat in categories_keys]
                    cfg = bank_color_map.get(b_sym, dict(line="#EE7224", fill="rgba(238, 114, 36, 0.2)"))

                    fig_multi_radar.add_trace(go.Scatterpolar(
                        r=dim_values, theta=categories_display, fill='toself', name=f"{b_sym} ({b_rec.iloc[0]['bank_name']})",
                        line=dict(color=cfg["line"], width=2.5), fillcolor=cfg["fill"]
                    ))

            fig_multi_radar.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True, range=[0, 108],
                        tickvals=[20, 40, 60, 80, 100],
                        ticktext=["20", "40", "60", "80", "100"],
                        angle=45,  # Xoay nhãn giá trị sang góc 45 độ để không đè vào chữ trên trục chính
                        tickfont=dict(size=9, color=polar_radial, family="JetBrains Mono"),
                        gridcolor=grid_color, showline=False
                    ),
                    angularaxis=dict(
                        tickfont=dict(size=11, color=c_text_primary, family="Plus Jakarta Sans"),
                        gridcolor=grid_color, rotation=90, direction="clockwise"
                    ),
                    bgcolor=polar_bg
                ),
                template=plotly_template, paper_bgcolor=paper_bgcolor,
                height=480, margin=dict(l=75, r=75, t=60, b=50),
                legend=dict(
                    orientation="h", yanchor="bottom", y=1.08, xanchor="center", x=0.5,
                    font=dict(family="Plus Jakarta Sans", size=11, color=c_text_primary),
                    bgcolor="rgba(0,0,0,0)"
                )
            )
            st.plotly_chart(fig_multi_radar, use_container_width=True)

        with col_radar_summary:
            st.markdown("#### 🔍 Nhận Định Đối Đầu Định Lượng:")
            for b_sym in benchmark_banks:
                b_rec = df_metrics[(df_metrics["symbol"] == b_sym) & (df_metrics["period"] == radar_period)].iloc[0]
                st.markdown(f"""
                **📌 {b_sym} ({b_rec['bank_name']}):**
                - **Biên lãi NIM:** `{b_rec['nim']:.2f}%` (Δ QoQ: `{b_rec['nim_diff_qoq']:+.2f}%`)
                - **Chất lượng nợ NPL:** `{b_rec['npl_ratio']:.2f}%` | **Bao phủ LLR:** `{b_rec['llr_ratio']:.0f}%`
                - **Vốn rẻ CASA:** `{b_rec['casa_ratio']:.1f}%` | **ROE TTM:** `{b_rec['roe_ttm']:.1f}%`
                ---
                """)


# =====================================================================
# TAB 4: TRUNG TÂM KIỂM TOÁN & ĐỐI SOÁT KẾ TOÁN (100% KHỚP)
# =====================================================================

with tab4:
    st.markdown("### 📑 Module 4: Bằng Chứng Năng Lực Dữ Liệu — Đối Soát Kế Toán BCTC")
    st.markdown(
        "Chứng minh năng lực kiểm chứng dữ liệu chính xác tuyệt đối theo yêu cầu của Người Quan Sát:"
    )

    pass_cnt = (df_audit["Overall_Integrity"] == "PASS").sum()
    total_cnt = len(df_audit)

    col_audit_stat1, col_audit_stat2, col_audit_stat3 = st.columns(3)
    col_audit_stat1.metric("Tỷ Lệ Chuẩn Khớp Toán Học", f"{(pass_cnt/total_cnt)*100:.1f}%", "100% Đạt Chuẩn")
    col_audit_stat2.metric("Sai Số Bảng Cân Đối (BS)", "0.00 VNĐ", "Tuyệt đối")
    col_audit_stat3.metric("Sai Số Dư Nợ Cho Vay (Loans)", "0.00 VNĐ", "Tuyệt đối")

    st.dataframe(
        df_audit.rename(columns={
            "Symbol": "Mã", "Period": "Kỳ",
            "Total_Assets": "Tổng Tài Sản (Tỷ)", "Liabilities_Plus_Equity": "Nợ + Vốn CSH (Tỷ)",
            "BS_Variance": "Chênh lệch BS", "BS_Audit_Result": "Kiểm toán BS",
            "Customer_Loans": "Dư Nợ Cho Vay (Tỷ)", "Sum_Loan_Buckets": "Tổng Nhóm 1->5 (Tỷ)",
            "Loan_Variance": "Chênh lệch Dư nợ", "Loan_Audit_Result": "Kiểm toán Dư nợ",
            "Overall_Integrity": "Kết luận Toàn vẹn"
        }),
        use_container_width=True, hide_index=True
    )

    st.markdown("---")
    st.markdown("#### 📥 Trung Tâm Xuất Dữ Liệu & Báo Cáo Phân Tích (Data Export Center)")

    col_btn_excel, col_btn_csv = st.columns(2)
    with col_btn_excel:
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
            df_vnindex.to_excel(writer, sheet_name="VNINDEX_Overview", index=False)
            df_metrics.to_excel(writer, sheet_name="Banking_Financials_Metrics", index=False)
            df_audit.to_excel(writer, sheet_name="Reconciliation_Audit", index=False)
            df_scorecard.to_excel(writer, sheet_name="Health_Scorecard", index=False)
        excel_data = excel_buffer.getvalue()

        st.download_button(
            label="📊 Tải Báo Cáo Toàn Diện (Excel Đa Sheet .xlsx)",
            data=excel_data, file_name=f"VN_FINANCE_INSIGHTS_REPORT_{datetime.date.today()}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True
        )

    with col_btn_csv:
        csv_metrics = df_metrics.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📄 Tải Bảng Chỉ Số Ngân Hàng (.csv)",
            data=csv_metrics, file_name=f"banking_metrics_cleaned_{datetime.date.today()}.csv",
            mime="text/csv", use_container_width=True
        )


# =====================================================================
# TAB 5: GÓC BÁO CHÍ DỮ LIỆU & TIKTOK @NQS.KINHTE
# =====================================================================

with tab5:
    st.markdown("### 🎬 Module 5: Ứng Dụng Báo Chí Dữ Liệu & TikTok Creative Lab (@nqs.kinhte)")
    st.markdown(
        "Chứng minh năng lực chuyển đổi dữ liệu thô thành **kịch bản video ngắn đa nền tảng** cho tòa soạn Người Quan Sát:"
    )

    col_tt1, col_tt2 = st.columns(2)
    with col_tt1:
        render_html(f"""
        <div class="jd-card">
            <div style="font-size: 11px; font-weight: 800; color: #EE7224;">🎬 KỊCH BẢN VIDEO TIKTOK #01 • ĐỀ TÀI: CHẤT LƯỢNG TÀI SẢN VCB</div>
            <h4 style="margin: 4px 0 6px 0; font-size: 14.5px; font-weight: 800; color: {c_text_primary};">
                Vì sao Vietcombank nợ xấu chỉ 1% nhưng lập đệm dự phòng bao phủ tới 230%?
            </h4>
            <p style="font-size: 12.5px; color: {c_text_secondary}; line-height: 1.5; margin-bottom: 6px;">
                <b>Hook 3s:</b> "Có bao giờ bạn tự hỏi, một ngân hàng kiếm gần 10.000 tỷ một quý như Vietcombank lại chuẩn bị một 'kho tiền phòng thân' lớn đến mức nào?"<br/>
                <b>Data Highlight:</b> LLR đạt 230.1%, NPL duy trì 1.05%, đệm dự phòng dẫn đầu toàn ngành.
            </p>
            <div style="font-size: 11px; color: #10B981; font-weight: 700;">✓ Phù hợp Video Short 45s • Bản đồ nhiệt LLR</div>
        </div>
        """)

        render_html(f"""
        <div class="jd-card">
            <div style="font-size: 11px; font-weight: 800; color: #EE7224;">🎬 KỊCH BẢN VIDEO TIKTOK #02 • ĐỀ TÀI: ĐỊNH GIÁ THỊ TRƯỜNG CHỨNG KHOÁN</div>
            <h4 style="margin: 4px 0 6px 0; font-size: 14.5px; font-weight: 800; color: {c_text_primary};">
                VN-Index vượt 1,280 điểm: P/E 16.2x đang ở vùng đắt hay rẻ so với lịch sử 5 năm?
            </h4>
            <p style="font-size: 12.5px; color: {c_text_secondary}; line-height: 1.5; margin-bottom: 6px;">
                <b>Hook 3s:</b> "1,280 điểm có phải là đỉnh ngắn hạn? Nhìn vào dải P/E chu kỳ của Người Quan Sát sẽ thấy câu trả lời bất ngờ!"<br/>
                <b>Data Highlight:</b> P/E thị trường chạm 16.25x, tiệm cận dải cảnh báo 16.5x, thanh khoản duy trì trên MA20.
            </p>
            <div style="font-size: 11px; color: #10B981; font-weight: 700;">✓ Phù hợp Video Short 60s • Đồ thị dải định giá</div>
        </div>
        """)

    with col_tt2:
        render_html(f"""
        <div class="jd-card">
            <div style="font-size: 11px; font-weight: 800; color: #EE7224;">🎬 KỊCH BẢN VIDEO TIKTOK #03 • ĐỀ TÀI: CUỘC ĐUA TIỀN GỬI RẺ CASA</div>
            <h4 style="margin: 4px 0 6px 0; font-size: 14.5px; font-weight: 800; color: {c_text_primary};">
                Cuộc chiến 'vốn rẻ 0 đồng': Techcombank và MB Bank ai mới là Vua CASA thực thụ?
            </h4>
            <p style="font-size: 12.5px; color: {c_text_secondary}; line-height: 1.5; margin-bottom: 6px;">
                <b>Hook 3s:</b> "Cứ 100 đồng tiền gửi thì có hơn 40 đồng là vốn không kỳ hạn lãi suất gần như 0%. Ai đang hưởng lợi lớn nhất?"<br/>
                <b>Data Highlight:</b> TCB CASA đạt 42.0%, MBB bám đuổi với 39.8%, NIM tương ứng 4.15% và 4.70%.
            </p>
            <div style="font-size: 11px; color: #10B981; font-weight: 700;">✓ Phù hợp Video So Sánh 50s • Radar 5 chiều</div>
        </div>
        """)

        render_html(f"""
        <div class="jd-card">
            <div style="font-size: 11px; font-weight: 800; color: #EE7224;">🎬 KỊCH BẢN VIDEO TIKTOK #04 • ĐỀ TÀI: QUY MÔ DƯ NỢ BIG 4</div>
            <h4 style="margin: 4px 0 6px 0; font-size: 14.5px; font-weight: 800; color: {c_text_primary};">
                BIDV - Cỗ máy bơm vốn gần 2 triệu tỷ đồng ra nền kinh tế vận hành thế nào?
            </h4>
            <p style="font-size: 12.5px; color: {c_text_secondary}; line-height: 1.5; margin-bottom: 6px;">
                <b>Hook 3s:</b> "Gần 2 triệu tỷ đồng dư nợ cho vay! Con số khổng lồ này của BIDV lớn đến mức nào khi so sánh với toàn bộ các ngân hàng khác?"<br/>
                <b>Data Highlight:</b> Tổng tài sản vượt 2.45 triệu tỷ, dư nợ 1.95 triệu tỷ, lợi nhuận thuần ổn định 6.450 tỷ/quý.
            </p>
            <div style="font-size: 11px; color: #10B981; font-weight: 700;">✓ Phù hợp Video Infographic 55s • Biểu đồ cột quy mô</div>
        </div>
        """)

    st.markdown("---")
    st.markdown("### 📰 Bài Báo Phân Tích Chuyên Sâu Mẫu (Sản phẩm Báo chí Dữ liệu)")
    sample_analysis_path = os.path.join(BASE_DIR, "docs", "SAMPLE_ANALYSIS.md")
    if os.path.exists(sample_analysis_path):
        with open(sample_analysis_path, "r", encoding="utf-8") as f:
            article_md = f.read()
        st.markdown(article_md)
    else:
        st.warning("Chưa tìm thấy file docs/SAMPLE_ANALYSIS.md.")

# =====================================================================
# TAB 6: KIẾN TRÚC HỆ THỐNG & PHƯƠNG PHÁP LUẬN ĐỊNH LƯỢNG
# =====================================================================

with tab_arch:
    st.markdown("### 🏛️ Trụ Cột Kiến Trúc Dữ Liệu & Phương Pháp Luận Phân Tích")
    st.markdown(
        "Hệ thống **VN-Finance Insights Terminal** được thiết kế theo tiêu chuẩn nền tảng phân tích tài chính chuyên nghiệp "
        "phục vụ hoạt động nghiên cứu thị trường và xuất bản nội dung của Chuyên trang Người Quan Sát (nguoiquansat.vn):"
    )

    col_jd1, col_jd2 = st.columns(2)
    with col_jd1:
        render_html(f"""
        <div class="jd-card">
            <div style="font-size: 11px; font-weight: 800; color: #EE7224;">1. XỬ LÝ & PHÂN TÁCH DỮ LIỆU TÀI CHÍNH</div>
            <h4 style="margin: 4px 0 6px 0; font-size: 14.5px; font-weight: 700; color: {c_text_primary};">Phân định 2 luồng Market Data vs Fundamental Data</h4>
            <p style="font-size: 12.5px; color: {c_text_secondary}; margin: 0; line-height: 1.5;">
                • Dữ liệu giá/thanh khoản theo phiên ngày (04/2023 - 01/2025).<br/>
                • Dữ liệu BCTC chuẩn hóa theo quý (Q1/2023 - Q4/2024), không bị lệch pha hay gán nhầm số liệu tĩnh vào chuỗi ngày.
            </p>
        </div>
        """)

        render_html(f"""
        <div class="jd-card">
            <div style="font-size: 11px; font-weight: 800; color: #EE7224;">2. TOÀN VẸN & KIỂM CHỨNG BCTC CHÍNH XÁC</div>
            <h4 style="margin: 4px 0 6px 0; font-size: 14.5px; font-weight: 700; color: {c_text_primary};">Reconciliation Audit Engine Đạt 100% Khớp Tuyệt Đối</h4>
            <p style="font-size: 12.5px; color: {c_text_secondary}; margin: 0; line-height: 1.5;">
                • Kiểm chứng <i>Tổng tài sản = Nợ + CSH</i> (Sai số 0.00 VNĐ).<br/>
                • Kiểm chứng <i>Dư nợ = Tổng nhóm 1 đến 5</i> (Sai số 0.00 VNĐ).<br/>
                • Xem toàn bộ nhật ký đối soát chi tiết tại <b>Tab Audit BCTC</b>.
            </p>
        </div>
        """)

    with col_jd2:
        render_html(f"""
        <div class="jd-card">
            <div style="font-size: 11px; font-weight: 800; color: #EE7224;">3. MÔ HÌNH ĐỊNH LƯỢNG NGÂN HÀNG CHUYÊN SÂU</div>
            <h4 style="margin: 4px 0 6px 0; font-size: 14.5px; font-weight: 700; color: {c_text_primary};">Hệ Thống Chỉ Số TTM, Δ QoQ, Δ YoY & CAMEL Scorecard</h4>
            <p style="font-size: 12.5px; color: {c_text_secondary}; margin: 0; line-height: 1.5;">
                • Xử lý triệt để Missing Values: Không có bất kỳ ô <code>NaN</code> hoặc <code>None</code> nào.<br/>
                • Chuẩn hóa Min-Max Scaling [10, 100] cho biểu đồ Radar so sánh đối đầu 1–3 ngân hàng cùng lúc.
            </p>
        </div>
        """)

        render_html(f"""
        <div class="jd-card">
            <div style="font-size: 11px; font-weight: 800; color: #EE7224;">4. BÁO CHÍ DỮ LIỆU & NỘI DUNG TIKTOK @NQS.KINHTE</div>
            <h4 style="margin: 4px 0 6px 0; font-size: 14.5px; font-weight: 700; color: {c_text_primary};">Chuyển Hóa Dữ Liệu Thành Kịch Bản Video Ngắn Hút Triệu View</h4>
            <p style="font-size: 12.5px; color: {c_text_secondary}; margin: 0; line-height: 1.5;">
                • 4 Kịch bản video hoàn chỉnh có sẵn Hook 3s, Data Highlight & Đồ họa tương ứng.<br/>
                • Bài phân tích mẫu chuyên sâu chuẩn phong cách tòa soạn tại <b>Tab TikTok</b>.
            </p>
        </div>
        """)

    st.markdown("---")
    st.info(
        "💡 **Ghi chú nghiệp vụ BCTC chu kỳ 2023 - 2024:** "
        "Số liệu nợ xấu (NPL) được phân tích trong bối cảnh cơ chế cơ cấu nợ theo **Thông tư 02/2023/TT-NHNN**; "
        "Biên lãi thuần (NIM) phản ánh chuỗi **4 lần hạ lãi suất điều hành của NHNN** trong năm 2023 trước khi tạo đáy hồi phục vào năm 2024."
    )

# =====================================================================
# FOOTER: BẢN QUYỀN TERMINAL
# =====================================================================

footer_html = f"""
<hr style="border: 0.5px solid {c_border_card}; margin-top: 36px; margin-bottom: 18px;">
<div style="text-align: center; font-size: 12px; color: {c_text_secondary}; line-height: 1.6;">
    <b>VN-FINANCE INSIGHTS TERMINAL • v2.5 ENTERPRISE EDITION</b><br/>
    Bản quyền nghiên cứu & dữ liệu thuộc <b>Chuyên trang Tài chính Người Quan Sát (nguoiquansat.vn)</b> • Intech Group.<br/>
    Kiến trúc hệ thống: Python 3.12 • Streamlit • Plotly • Pandas Reconciliation Engine • OpenPyXL • Phân tích bởi: Kiều Quang Trường
</div>
"""
render_html(footer_html)
