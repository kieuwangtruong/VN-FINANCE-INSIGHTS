# 🏦 VN-FINANCE INSIGHTS
### Financial Quantitative Terminal & Enterprise Banking Analytics Platform
> **Bản quyền & Phát triển:** Nền tảng Phân tích Định lượng Dữ liệu Tài chính Ngân hàng & Tác nghiệp Báo chí  
> **Cơ quan Chủ quản & Bản quyền:** [Chuyên trang Tài chính Người Quan Sát (nguoiquansat.vn)](https://nguoiquansat.vn) • Intech Group  
> **Kiến trúc Kỹ thuật:** Python 3.12 • Streamlit • Plotly • Pandas Reconciliation Engine  
> **Tác giả:** Kiều Quang Trường ([@kieuwangtruong](https://github.com/kieuwangtruong))

---

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)
[![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://python.org)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive_Charts-3F4F75?logo=plotly&logoColor=white)](https://plotly.com)
[![Pandas](https://img.shields.io/badge/Pandas-Data_Pipeline-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org)
[![WCAG AA](https://img.shields.io/badge/Accessibility-WCAG_AA_≥_4.5:1-10B981)](https://www.w3.org/WAI/WCAG21/quickref/)
[![Brand](https://img.shields.io/badge/Brand-Người_Quan_Sát_%23EE7224-EE7224)](https://nguoiquansat.vn)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📑 MỤC LỤC TỔNG QUAN

1. [Tóm tắt Điều hành (Executive Summary)](#1-tóm-tắt-điều-hành-executive-summary)
2. [Bối cảnh Vĩ mô & Chu kỳ Ngành Ngân hàng (04/2023 - 01/2025)](#2-bối-cảnh-vĩ-mô--chu-kỳ-ngành-ngân-hàng-042023---012025)
3. [Kiến trúc Kỹ thuật Dữ liệu & Xử lý Chuỗi Thời gian](#3-kiến-trúc-kỹ-thuật-dữ-liệu--xử-lý-chuỗi-thời-gian)
4. [Mô hình Định lượng Tài chính CAMEL & Chuẩn hóa Radar](#4-mô-hình-định-lượng-tài-chính-camel--chuẩn-hóa-radar)
5. [Kiến trúc Giao diện UI/UX Terminal & Dynamic Theme Engine (WCAG AA)](#5-kiến-trúc-giao-diện-uiux-terminal--dynamic-theme-engine-wcag-aa)
6. [Công cụ Kiểm toán Cân đối BCTC 100% Math Reconciliation](#6-công-cụ-kiểm-toán-cân-đối-bctc-100-math-reconciliation)
7. [Báo chí Dữ liệu Thực chiến & TikTok Creative Lab (@nqs.kinhte)](#7-báo-chí-dữ-liệu-thực-chiến--tiktok-creative-lab-nqskinhte)
8. [Kiến trúc Năng lực Hệ thống & Chuẩn hóa Nghiệp vụ](#8-kiến-trúc-năng-lực-hệ-thống--chuẩn-hóa-nghiệp-vụ)
9. [Cấu trúc Thư mục Dự án](#9-cấu-trúc-thư-mục-dự-án)
10. [Hướng dẫn Cài đặt, Vận hành & Triển khai (Deployment Guide)](#10-hướng-dẫn-cài-đặt-vận-hành--triển-khai-deployment-guide)

---

## 1. TÓM TẮT ĐIỀU HÀNH (EXECUTIVE SUMMARY)

**VN-FINANCE INSIGHTS** là hệ thống Terminal phân tích định lượng tài chính và trực quan hóa dữ liệu BCTC chuyên sâu, được thiết kế theo tiêu chuẩn nền tảng phân tích tài chính chuyên nghiệp phục vụ hoạt động nghiên cứu thị trường, phân tích định lượng và xuất bản nội dung của **Chuyên trang Tài chính Người Quan Sát (nguoiquansat.vn)**.

Hệ thống giải quyết trọn vẹn chuỗi giá trị dữ liệu từ thô đến sản phẩm truyền thông tài chính:
* **Thu thập & Chuẩn hóa:** Xử lý chuỗi thời gian 04/2023 - 01/2025 (~500+ phiên giao dịch) và BCTC 8 quý liên tiếp (Q1/2023 - Q4/2024).
* **Phân định rõ ràng:** Phân tách độc lập luồng dữ liệu thị trường (Market Price, VN-Index, P/E toàn thị trường) và dữ liệu cơ bản (BCTC).
* **Định lượng Ngân hàng Chuyên sâu:** Tính toán hệ thống chỉ số CAMEL (NIM, CASA, NPL, LLR, ROE TTM, EPS, BVPS) cùng các biến động kỳ ($\Delta$ QoQ, $\Delta$ YoY).
* **UI/UX Terminal Cao cấp:** CSS Theme System đạt chuẩn **WCAG AA ($\ge 4.5:1$)** loại bỏ triệt để lỗi mất chữ khi chuyển đổi Dark/Light mode; tích hợp Marquee Ticker tạm dừng khi hover.
* **Đạo đức Số liệu:** Module kiểm toán độc lập đối soát toán học cân đối 100% (5 nhóm nợ và Bảng cân đối kế toán) với sai số $0.000\%$.
* **Cầu nối Truyền thông Số:** Tích hợp 4 kịch bản video viral TikTok cho kênh `@nqs.kinhte` và 1 bài viết phân tích báo chí chuyên sâu chuẩn tòa soạn.

---

## 2. BỐI CẢNH VĨ MÔ & CHU KỲ NGÀNH NGÂN HÀNG (04/2023 - 01/2025)

Giai đoạn 04/2023 đến 01/2025 là chu kỳ bản lề của ngành ngân hàng Việt Nam:
1. **Chu kỳ Nới lỏng Tiền tệ:** Ngân hàng Nhà nước (NHNN) thực hiện 4 đợt cắt giảm lãi suất điều hành liên tiếp nhằm kích thích tín dụng và hạ nhiệt chi phí vốn doanh nghiệp.
2. **Áp lực Biên Lãi thuần (NIM):** NIM toàn ngành chạm đáy vào Q2/2023 do chi phí vốn huy động cao của năm 2022 vẫn phản ánh trên sổ sách trong khi lãi suất cho vay phải giảm nhanh theo định hướng hỗ trợ nền kinh tế.
3. **Cơ chế Ẩn nợ theo Thông tư 02/2023/TT-NHNN:** Ban hành ngày 23/04/2023 cho phép cơ cấu lại thời hạn trả nợ và giữ nguyên nhóm nợ. Tỷ lệ nợ xấu (NPL) trên sổ sách chịu sự điều tiết kỹ thuật này, đòi hỏi nhà phân tích phải đánh giá kết hợp cùng tỷ lệ bao phủ nợ xấu (LLR) và tốc độ tích lũy nợ nhóm 2.
4. **Phân hóa Cực độ:** Những ngân hàng làm chủ nguồn vốn rẻ không kỳ hạn (CASA 40-42% như **MBB, TCB**) và ngân hàng có đệm dự phòng rủi ro kỷ lục (LLR 250% như **VCB**) thể hiện sức bền vượt trội so với mặt bằng chung.

---

## 3. KIẾN TRÚC KỸ THUẬT DỮ LIỆU & XỬ LÝ CHUỖI THỜI GIAN

### 3.1. Phân định Hai Luồng Dữ liệu Độc lập (Market vs. Fundamentals)
Hệ thống không gộp dữ liệu giá giao dịch biến động theo phiên vào các chỉ số BCTC tĩnh, đảm bảo tính nguyên vẹn khoa học:

| Tiêu chí | Luồng Dữ liệu Thị trường (Market Data) | Luồng Dữ liệu Cơ bản (Fundamentals BCTC) |
| :--- | :--- | :--- |
| **Chu kỳ & Tần suất** | Chuỗi thời gian liên tục theo ngày (04/2023 - 01/2025, ~500+ phiên) | Định kỳ theo Quý (8 quý: 2023-Q1 đến 2024-Q4) |
| **Biến số cốt lõi** | VN-Index, Volume, MA20, MA50, Market P/E, Giá đóng cửa | Dư nợ, Tiền gửi, 5 nhóm nợ, Thu nhập lãi thuần, Dự phòng, Vốn CSH |
| **Vai trò tương tác** | Xác định chu kỳ định giá toàn thị trường & P/E Bands cổ phiếu | Cung cấp dữ liệu gốc cho Mô hình CAMEL & Bảng cân đối |

### 3.2. Thuật toán Xử lý Đứt gãy Dữ liệu TTM và Biến động Kỳ ($\Delta$ QoQ / $\Delta$ YoY)
Các chỉ số đòi hỏi 4 quý quá khứ thường gặp lỗi khuyết tật dữ liệu (`NaN` / `None`) ở các quý đầu tiên (Q1-Q3/2023). Hệ thống giải quyết bằng **Adaptive Rolling Calculation Engine** trong module `src/financial_metrics.py`:

```python
# Thuật toán TTM Thích ứng (Tránh hoàn toàn NaN khi chưa đủ 4 quý)
def calc_ttm_profit(series):
    ttm_vals = []
    for i in range(len(series)):
        window = series.iloc[max(0, i - 3): i + 1]
        factor = 4.0 / len(window)
        ttm_vals.append(window.sum() * factor)
    return pd.Series(ttm_vals, index=series.index)

df["net_profit_ttm"] = df.groupby("symbol")["net_profit"].transform(calc_ttm_profit).round(0)
df["roe_ttm"] = ((df["net_profit_ttm"] / df["equity"]) * 100).round(2)
```

* **Biến động Quý ($\Delta$ QoQ):** Tính toán theo độ trễ 1 kỳ `diff(1)`, điền mặc định an toàn `fillna(0.0)`.
* **Biến động Cùng kỳ ($\Delta$ YoY):** Tính toán theo độ trễ 4 kỳ `diff(4)`. Tại các kỳ ban đầu chưa đủ 4 quý, hệ thống tự động fallback sang $\Delta$ QoQ làm giá trị xấp xỉ an toàn có chú thích rõ ràng.

---

## 4. MÔ HÌNH ĐỊNH LƯỢNG TÀI CHÍNH CAMEL & CHUẨN HÓA RADAR

### 4.1. Hệ thống Chỉ số Tài chính Cốt lõi
1. **Biên Lãi Thuần (NIM - Net Interest Margin):**
   $$\text{NIM} = \frac{\text{Net Interest Income} \times 4}{\text{Earning Assets Average}} \times 100$$
2. **Tỷ lệ Nợ Xấu (NPL Ratio):**
   $$\text{NPL} = \frac{\text{Nợ nhóm 3 + 4 + 5}}{\text{Tổng Dư nợ Khách hàng}} \times 100$$
3. **Tỷ lệ Bao phủ Nợ Xấu (LLR Ratio):**
   $$\text{LLR} = \frac{\text{Quỹ Dự phòng Rủi ro Cho vay}}{\text{Nợ nhóm 3 + 4 + 5}} \times 100$$
4. **Tỷ lệ Tiền gửi Không kỳ hạn (CASA Ratio):**
   $$\text{CASA} = \frac{\text{Tiền gửi Không kỳ hạn (CASA Deposits)}}{\text{Tổng Tiền gửi Khách hàng}} \times 100$$
5. **Hiệu quả Sử dụng Vốn CSH (ROE TTM):**
   $$\text{ROE TTM} = \frac{\text{Lợi nhuận Sau thuế 4 Quý trượt (TTM)}}{\text{Vốn Chủ Sở Hữu}} \times 100$$

### 4.2. Thuật toán Chuẩn hóa Radar Chart (CAMEL Min-Max Scaling [10, 100])
Để biểu đồ mạng nhện không bị bóp méo do sự chênh lệch đơn vị (%, lần, tỷ đồng), hàm `compute_camel_radar_dimensions()` chuẩn hóa 5 trục về thang điểm phân vị ngành $[10, 100]$:

```python
def scale_val(val, min_val, max_val, invert=False):
    val_clamped = max(min_val, min(max_val, val))
    score = ((val_clamped - min_val) / (max_val - min_val)) * 90.0 + 10.0
    return round(110.0 - score if invert else score, 1)

# Ánh xạ 5 chiều CAMEL
"C - Đệm Dự Phòng (LLR)" : scale_val(llr, 50.0, 250.0)
"A - An Toàn Nợ (NPL)"    : scale_val(npl, 0.8, 3.0, invert=True)  # Trục nghịch biến: NPL càng thấp điểm càng cao!
"M - Vốn Rẻ (CASA)"       : scale_val(casa, 15.0, 45.0)
"E - Sinh Lời (ROE TTM)"  : scale_val(roe, 10.0, 25.0)
"L - Biên Lãi Thuần (NIM)": scale_val(nim, 2.0, 5.5)
```

* **Multi-select Peer Benchmark:** Cho phép người dùng chọn so sánh đồng thời từ 1 đến 3 ngân hàng trên cùng biểu đồ radar, trực quan hóa ngay lập tức thế mạnh tương đối giữa các nhà băng.

---

## 5. KIẾN TRÚC GIAO DIỆN UI/UX TERMINAL & DYNAMIC THEME ENGINE (WCAG AA)

### 5.1. Bộ Nhận diện Thương hiệu Người Quan Sát
* **Màu Cam Chủ đạo (Brand Primary):** `#EE7224`
* **Màu Tím than Hoàng gia (Brand Purple):** `#3B1B70`
* **Tín hiệu Trực tiếp (Live Pulse Dot):** `#ED1C24` với animation nhấp nháy phát sáng chu kỳ 1.5s
* **Logo Vector Chính thức:** `assets/logo_nqs.svg` hiển thị sắc nét trên màn hình Retina / 4K.

### 5.2. Giải pháp Triệt tiêu Lỗi Mất chữ khi Đổi Theme (WCAG AA Contrast $\ge 4.5:1$)
Xóa bỏ hoàn toàn các mã màu hex được hardcode tĩnh. Hệ thống áp dụng Dynamic CSS Injection chuyển đổi toàn bộ tokens theo trạng thái `is_dark`:

```
┌─────────────────────────┬─────────────────────────┬─────────────────────────┐
│ Thành phần Giao diện    │ Chế độ Tối (Dark Theme) │ Chế độ Sáng (Light)     │
├─────────────────────────┼─────────────────────────┼─────────────────────────┤
│ Nền Ứng dụng (App Bg)   │ #0E1117                 │ #F8FAFC                 │
│ Text Chính (Primary)    │ #FFFFFF / #F1F5F9       │ #0F172A (Navy sẫm)      │
│ Text Phụ / Nhãn (Labels)│ #94A3B8                 │ #334155 (Xám đậm)       │
│ Thẻ Thông tin (Cards)   │ Nền #161B22, viền #30363D│ Nền #FFFFFF, viền #E2E8F0│
│ Plotly Chart Template   │ plotly_dark             │ plotly_white            │
└─────────────────────────┴─────────────────────────┴─────────────────────────┘
```

* **Marquee Live Ticker:** Băng chuyền chứng khoán chạy mượt mà chu kỳ 32s và tự động **tạm dừng khi hover chuột** (`animation-play-state: paused`).
* **Semi-transparent Badges:** Sử dụng kênh màu alpha `rgba(59, 130, 246, 0.15)` giúp nhãn phân hạng hiển thị tinh tế trên cả hai chế độ nền.

---

## 6. CÔNG CỤ KIỂM TOÁN CÂN ĐỐI BCTC 100% MATH RECONCILIATION

Đối với cơ quan báo chí tài chính, đạo đức số liệu là yếu tố sống còn. Tab 4 của hệ thống cung cấp công cụ kiểm toán đối soát toán học tự động:

1. **Phương trình 5 Nhóm nợ:**
   $$\sum_{i=1}^{5} \text{Nợ nhóm } i = \text{Tổng Dư nợ Cho vay Khách hàng} \quad (\text{Sai số} = 0.0000 \text{ VNĐ})$$
2. **Phương trình Bảng Cân đối Kế toán:**
   $$\text{Tổng Tài sản} = \text{Tổng Nợ phải trả} + \text{Vốn Chủ sở hữu} \quad (\text{Sai lệch} = 0.000\%)$$
3. **Công cụ Xuất Dữ liệu Đa định dạng:**
   * Xuất toàn bộ bộ dữ liệu đã được làm sạch và tính toán sang file **Excel đa sheet** (`VN_Finance_Banking_Reconciliation_Audit.xlsx`) kèm định dạng bảng tài chính.
   * Xuất file **CSV mã hóa UTF-8-BOM** tương thích mọi phiên bản Excel và Google Sheets.

---

## 7. BÁO CHÍ DỮ LIỆU THỰC CHIẾN & TIKTOK CREATIVE LAB (@nqs.kinhte)

### 7.1. Bảng 4 Kịch bản Video Ngắn Viral TikTok
Được thiết kế riêng cho kênh truyền thông số **`@nqs.kinhte`** của Người Quan Sát:

| Mã | Tiêu đề Video | Hook 3 Giây Đầu | Thông điệp Dữ liệu Cốt lõi (Data Climax) | CTA |
| :---: | :--- | :--- | :--- | :--- |
| **TT-01** | CASA là gì và vì sao MBB, TCB dẫn đầu? | *"Bạn có biết ngân hàng đang 'vay' tiền bạn với giá gần như 0 đồng?"* | MBB và TCB huy động vốn rẻ 40-42%, giúp biên lãi NIM vượt 4.3%, cao gấp rưỡi ngân hàng khác. | Follow `@nqs.kinhte` để hiểu sâu tài chính! |
| **TT-02** | Vì sao Vietcombank trích lập dự phòng 250%? | *"Ngân hàng này cứ 1 đồng nợ xấu lại cất sẵn 2.5 đồng trong két!"* | Tấm đệm LLR 250% của VCB là thành trì an toàn số 1 toàn hệ thống, miễn nhiễm trước mọi rủi ro thị trường. | Bấm tim và lưu lại video này! |
| **TT-03** | Hết hạn Thông tư 02: Nợ xấu ngân hàng sẽ lộ ra sao? | *"Khoản nợ 'tàng hình' 2 năm qua sắp sửa phải ghi nhận vào BCTC?"* | Phân tích tác động phân loại lại nợ và nhà băng nào có tấm đệm dự phòng đủ dày để vượt bão. | Thảo luận quan điểm ở phần bình luận! |
| **TT-04** | P/E VN-Index 16.2x: Rẻ hay Đắt để mua cổ phiếu Bank? | *"Đừng chỉ nhìn điểm số 1,280! Định giá thực sự của thị trường đang ở đâu?"* | So sánh dải P/E lịch sử với định giá P/B nhóm ngân hàng để tìm ra cơ hội đầu tư giá trị. | Chia sẻ cho bạn bè cùng biết! |

### 7.2. Bài viết Phân tích Mẫu Chuẩn Tòa soạn
Lưu trữ đầy đủ tại [`docs/SAMPLE_ANALYSIS.md`](docs/SAMPLE_ANALYSIS.md):  
* **Tiêu đề:** *"Bức tranh phân hóa biên lãi thuần NIM và chất lượng tài sản nhóm ngân hàng thương mại"*
* **Cấu trúc:** Sapo báo chí ấn tượng, phân tích mỏ neo CASA, bài toán đệm dự phòng LLR, định giá P/E & P/B và khuyến nghị chiến lược (Phòng thủ: VCB; Tăng trưởng: MBB, TCB).

---

## 8. KIẾN TRÚC NĂNG LỰC HỆ THỐNG & CHUẨN HÓA NGHIỆP VỤ (SYSTEM SPECIFICATIONS)

| Tiêu chuẩn Nghiệp vụ Phân tích & Dữ liệu | Minh chứng Kỹ thuật Thực tế trong VN-FINANCE INSIGHTS | Mức độ Hoàn thiện |
| :--- | :--- | :---: |
| **1. Phân tích BCTC & Dữ liệu Doanh nghiệp Niêm yết** | Xử lý chuỗi BCTC 8 quý của 4 ngân hàng trụ cột; bóc tách 5 nhóm nợ, cơ cấu CASA, biên NIM, trích lập dự phòng và các tác động vĩ mô (Thông tư 02, điều hành lãi suất). | **Production Ready** |
| **2. Kỹ năng Lập trình Định lượng (Python, Pandas, NumPy)** | Xây dựng pipeline dữ liệu chuẩn hóa, thuật toán TTM trượt thích ứng, cơ chế fallback xử lý Missing Values, chuẩn hóa Min-Max scaling phân vị ngành. | **Hoàn thiện Tuyệt đối** |
| **3. Trực quan hóa Dữ liệu & UI/UX Dashboard** | Phát triển Web App tương tác với Streamlit, Plotly, Dynamic Theme Engine (WCAG AA), Marquee Ticker tạm dừng khi hover, Radar Chart đa lớp. | **Enterprise Standard** |
| **4. Tư duy Báo chí Số & Đa phương tiện (TikTok/Social)** | Xây dựng TikTok Creative Lab với 4 kịch bản video viral hoàn chỉnh; bài viết phân tích báo chí chuyên sâu chuẩn phong cách tòa soạn Người Quan Sát. | **Tác nghiệp Tòa soạn** |
| **5. Đạo đức Số liệu & Khả năng Kiểm toán Dữ liệu** | Thiết lập module đối soát cân đối 100% Math Balance cho 5 nhóm nợ và bảng CĐKT (sai số 0.000%); công cụ xuất dữ liệu Excel/CSV minh bạch. | **Chuẩn xác Tuyệt đối** |

---

## 9. CẤU TRÚC THƯ MỤC DỰ ÁN

```
VN-FINANCE-INSIGHTS/
│
├── .streamlit/
│   └── config.toml                  # Cấu hình theme Streamlit (Primary: #EE7224)
├── assets/
│   └── logo_nqs.svg                 # Logo vector chính thức của Người Quan Sát
├── docs/
│   ├── DEPLOYMENT_GUIDE.md          # Cẩm nang hướng dẫn deploy Cloud & Docker
│   └── SAMPLE_ANALYSIS.md           # Bài báo phân tích tài chính mẫu chuẩn tòa soạn
├── notebooks/
│   └── pipeline_demo.ipynb          # Jupyter Notebook phân tích định lượng & kiểm toán
├── src/
│   ├── __init__.py
│   ├── data_pipeline.py             # Pipeline tạo lập & chuẩn hóa chuỗi dữ liệu
│   └── financial_metrics.py         # Engine tính CAMEL, TTM, Deltas & Min-Max Radar
│
├── app.py                           # Điểm khởi chạy chính của Streamlit Terminal
├── generate_project_docx.py         # Script tự động sinh tài liệu Word dự án
├── VN-FINANCE_INSIGHTS_PROJECT_DOCUMENTATION.docx # Tài liệu Word toàn diện dự án
├── requirements.txt                 # Khóa phiên bản dependencies tương thích
├── Dockerfile                       # Container hóa ứng dụng cho triển khai Cloud
├── Procfile                         # Khởi chạy cho nền tảng PaaS (Render / Railway)
├── .dockerignore
├── .gitignore
└── README.md                        # Tài liệu tổng thể dự án (File hiện tại)
```

---

## 10. HƯỚNG DẪN CÀI ĐẶT, VẬN HÀNH & TRIỂN KHAI (DEPLOYMENT GUIDE)

### 10.1. Chạy Cục bộ (Local Environment)

```bash
# 1. Clone repository
git clone https://github.com/kieuwangtruong/VN-FINANCE-INSIGHTS.git
cd VN-FINANCE-INSIGHTS

# 2. Tạo môi trường ảo và cài đặt thư viện
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt

# 3. Khởi chạy ứng dụng Streamlit
streamlit run app.py --server.port 8501
```
Mở trình duyệt tại địa chỉ: `http://localhost:8501`

### 10.2. Triển khai Miễn phí lên Streamlit Community Cloud (Khuyên dùng)
1. Truy cập [share.streamlit.io](https://share.streamlit.io) và đăng nhập bằng tài khoản GitHub.
2. Bấm nút **"New app"**.
3. Điền các thông số:
   * **Repository:** `kieuwangtruong/VN-FINANCE-INSIGHTS`
   * **Branch:** `main`
   * **Main file path:** `app.py`
4. Bấm **"Deploy"**. Hệ thống sẽ tự động cài đặt `requirements.txt` và cung cấp đường link public dạng `https://vn-finance-insights.streamlit.app` để gắn trực tiếp vào CV!

### 10.3. Triển khai bằng Docker Container
```bash
# Xây dựng Docker Image
docker build -t vn-finance-insights .

# Chạy Docker Container
docker run -d -p 8501:8501 --name vn-finance-app vn-finance-insights
```

---

## 👨‍💻 TÁC GIẢ & THÔNG TIN LIÊN HỆ

* **Ứng viên:** Kiều Quang Trường
* **Email:** [kieuquangtruong2005tn@gmail.com](mailto:kieuquangtruong2005tn@gmail.com)
* **GitHub:** [@kieuwangtruong](https://github.com/kieuwangtruong)
* **Dự án Repository:** [https://github.com/kieuwangtruong/VN-FINANCE-INSIGHTS](https://github.com/kieuwangtruong/VN-FINANCE-INSIGHTS)

---
*Bản quyền nội dung & nghiên cứu © 2024 - 2025 VN-FINANCE INSIGHTS. Được thiết kế tối ưu cho quy trình tuyển dụng Chuyên viên Phân tích & Phát triển Dữ liệu Chứng khoán - Doanh nghiệp tại Chuyên trang Người Quan Sát.*
