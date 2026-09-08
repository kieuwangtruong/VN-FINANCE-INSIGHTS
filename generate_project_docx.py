"""
Script tự động tạo file Word DOCX chuyên nghiệp:
VN-FINANCE_INSIGHTS_PROJECT_DOCUMENTATION.docx
Báo cáo Toàn diện Hệ thống Phân tích Định lượng & Dashboard Tài chính Ngân hàng
Dự án Capstone Portfolio - Chuyên viên Phân tích & Phát triển Dữ liệu Chứng khoán (Người Quan Sát)
"""

import os
import sys
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def set_cell_background(cell, fill_hex):
    """Tô màu nền cho ô trong bảng"""
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Thiết lập padding cho ô trong bảng"""
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

def set_cell_borders(cell, top=None, bottom=None, left=None, right=None):
    """Thiết lập viền tùy chỉnh cho ô"""
    tcPr = cell._element.get_or_add_tcPr()
    tcBorders = parse_xml(f'<w:tcBorders {nsdecls("w")}/>')
    borders = {'top': top, 'bottom': bottom, 'left': left, 'right': right}
    for edge, val in borders.items():
        if val:
            color, sz, val_type = val
            b_xml = parse_xml(f'<w:{edge} {nsdecls("w")} w:val="{val_type}" w:sz="{sz}" w:space="0" w:color="{color}"/>')
            tcBorders.append(b_xml)
        else:
            b_xml = parse_xml(f'<w:{edge} {nsdecls("w")} w:val="none"/>')
            tcBorders.append(b_xml)
    tcPr.append(tcBorders)

def add_callout_box(doc, title, text_paragraphs, border_color="EE7224", bg_color="F8FAFC"):
    """Tạo hộp thoại Callout chuyên nghiệp viền trái"""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, bg_color)
    set_cell_margins(cell, top=140, bottom=140, left=200, right=160)
    set_cell_borders(cell, left=(border_color, "24", "single"), top=None, bottom=None, right=None)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(4)
    run_title = p.add_run(f"📌 {title}\n")
    run_title.font.name = 'Segoe UI'
    run_title.font.size = Pt(11)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(0xEE, 0x72, 0x24) if border_color == "EE7224" else RGBColor(0x1E, 0x29, 0x3B)
    
    for i, t in enumerate(text_paragraphs):
        if i == 0:
            p_text = p
        else:
            p_text = cell.add_paragraph()
            p_text.paragraph_format.space_before = Pt(0)
            p_text.paragraph_format.space_after = Pt(4)
        run_body = p_text.add_run(t)
        run_body.font.name = 'Segoe UI'
        run_body.font.size = Pt(10)
        run_body.font.color.rgb = RGBColor(0x33, 0x41, 0x55)
    
    # Khoảng cách sau bảng
    p_spacer = doc.add_paragraph()
    p_spacer.paragraph_format.space_before = Pt(0)
    p_spacer.paragraph_format.space_after = Pt(4)

def build_project_docx(file_path: str):
    doc = Document()
    
    # 1. Cấu hình lề trang (1 inch tiêu chuẩn)
    for section in doc.sections:
        section.top_margin = Inches(0.9)
        section.bottom_margin = Inches(0.9)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
        # Header & Footer
        footer = section.footer
        p_ft = footer.paragraphs[0]
        p_ft.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        f_run = p_ft.add_run("VN-FINANCE INSIGHTS | Chuyên viên Phân tích & Phát triển Dữ liệu - Người Quan Sát")
        f_run.font.name = "Segoe UI"
        f_run.font.size = Pt(8.5)
        f_run.font.color.rgb = RGBColor(0x94, 0xA3, 0xB8)
        
        header = section.header
        p_hd = header.paragraphs[0]
        p_hd.alignment = WD_ALIGN_PARAGRAPH.LEFT
        h_run = p_hd.add_run("DỰ ÁN CAPSTONE PORTFOLIO | HỆ THỐNG TERMINAL PHÂN TÍCH ĐỊNH LƯỢNG TÀI CHÍNH")
        h_run.font.name = "Segoe UI"
        h_run.font.size = Pt(8)
        h_run.font.color.rgb = RGBColor(0x94, 0xA3, 0xB8)

    # Helper format styles
    def format_heading1(text):
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(16)
        h.paragraph_format.space_after = Pt(6)
        h.paragraph_format.keep_with_next = True
        r = h.add_run(text)
        r.font.name = 'Segoe UI'
        r.font.size = Pt(15)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)
        return h

    def format_heading2(text):
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(12)
        h.paragraph_format.space_after = Pt(4)
        h.paragraph_format.keep_with_next = True
        r = h.add_run(text)
        r.font.name = 'Segoe UI'
        r.font.size = Pt(12.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0xEE, 0x72, 0x24)  # Người Quan Sát Orange
        return h

    def format_heading3(text):
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(8)
        h.paragraph_format.space_after = Pt(2)
        h.paragraph_format.keep_with_next = True
        r = h.add_run(text)
        r.font.name = 'Segoe UI'
        r.font.size = Pt(11)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0x3B, 0x1B, 0x70)  # Người Quan Sát Purple
        return h

    def format_paragraph(text, bold_prefix="", italic=False):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.18
        if bold_prefix:
            r_b = p.add_run(bold_prefix)
            r_b.font.name = 'Segoe UI'
            r_b.font.size = Pt(10.5)
            r_b.font.bold = True
            r_b.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)
        r_t = p.add_run(text)
        r_t.font.name = 'Segoe UI'
        r_t.font.size = Pt(10.5)
        r_t.font.italic = italic
        r_t.font.color.rgb = RGBColor(0x33, 0x41, 0x55)
        return p

    def format_bullet(text, bold_prefix=""):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r_b = p.add_run(bold_prefix)
            r_b.font.name = 'Segoe UI'
            r_b.font.size = Pt(10)
            r_b.font.bold = True
            r_b.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)
        r_t = p.add_run(text)
        r_t.font.name = 'Segoe UI'
        r_t.font.size = Pt(10)
        r_t.font.color.rgb = RGBColor(0x33, 0x41, 0x55)
        return p

    # =========================================================================
    # TRANG TIÊU ĐỀ (COVER / TITLE BANNER)
    # =========================================================================
    p_banner = doc.add_paragraph()
    p_banner.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_banner.paragraph_format.space_before = Pt(10)
    p_banner.paragraph_format.space_after = Pt(4)
    r_sub = p_banner.add_run("BÁO CÁO HỒ SƠ NĂNG LỰC DỰ ÁN CAPSTONE PORTFOLIO")
    r_sub.font.name = 'Segoe UI'
    r_sub.font.size = Pt(11)
    r_sub.font.bold = True
    r_sub.font.color.rgb = RGBColor(0xEE, 0x72, 0x24)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(4)
    p_title.paragraph_format.space_after = Pt(8)
    r_title = p_title.add_run("VN-FINANCE INSIGHTS\nTERMINAL PHÂN TÍCH ĐỊNH LƯỢNG TÀI CHÍNH NGÂN HÀNG & BÁO CHÍ DỮ LIỆU THỊ TRƯỜNG")
    r_title.font.name = 'Segoe UI'
    r_title.font.size = Pt(20)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)

    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_meta.paragraph_format.space_before = Pt(0)
    p_meta.paragraph_format.space_after = Pt(18)
    r_meta = p_meta.add_run(
        "Vị trí ứng tuyển: Chuyên viên Phân tích & Phát triển Dữ liệu Chứng khoán - Doanh nghiệp\n"
        "Đơn vị áp dụng / Case Study: Chuyên trang Tài chính Người Quan Sát (nguoiquansat.vn)\n"
        "Phiên bản: v2.5 Terminal Edition | Mã nguồn: Python 3.12 / Streamlit / Plotly / Pandas"
    )
    r_meta.font.name = 'Segoe UI'
    r_meta.font.size = Pt(10)
    r_meta.font.italic = True
    r_meta.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)

    # Đường kẻ ngăn cách
    p_divider = doc.add_paragraph()
    p_divider.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_divider.paragraph_format.space_before = Pt(0)
    p_divider.paragraph_format.space_after = Pt(14)
    r_div = p_divider.add_run("―" * 50)
    r_div.font.color.rgb = RGBColor(0xCB, 0xD5, 0xE1)

    # CALLOUT SUMMARY
    add_callout_box(
        doc,
        "TÓM TẮT ĐIỀU HÀNH DỰ ÁN (EXECUTIVE SUMMARY)",
        [
            "VN-FINANCE INSIGHTS là một hệ thống Terminal phân tích định lượng tài chính và trực quan hóa dữ liệu BCTC chuyên sâu, được thiết kế đặc thù làm dự án Capstone Portfolio để ứng tuyển vị trí Chuyên viên Phân tích & Phát triển Dữ liệu Chứng khoán - Doanh nghiệp tại Chuyên trang Người Quan Sát.",
            "Dự án giải quyết trọn vẹn chuỗi giá trị dữ liệu từ: (1) Thu thập & Chuẩn hóa chuỗi thời gian 04/2023 - 01/2025; (2) Xử lý lệch pha giữa dữ liệu giá thị trường hàng ngày và BCTC quý; (3) Tính toán định lượng chuyên sâu (CAMEL, NIM, CASA, NPL, LLR, TTM, Deltas QoQ/YoY); (4) Hệ thống UI/UX Theme Engine đạt chuẩn WCAG AA; (5) Đối soát toán học 100% Math Balance; và (6) Chuyển hóa dữ liệu thành các sản phẩm báo chí truyền thông số (Kịch bản Video ngắn TikTok @nqs.kinhte & Bài viết Báo chí Chuyên sâu)."
        ],
        border_color="EE7224",
        bg_color="FFF7ED"
    )

    # =========================================================================
    # MỤC LỤC TỔNG QUAN HỆ THỐNG
    # =========================================================================
    format_heading1("MỤC LỤC TỔNG QUAN TÀI LIỆU")
    format_bullet("Bối cảnh Thị trường & Mục tiêu Chiến lược của Dự án", "Phần I: ")
    format_bullet("Kiến trúc Kỹ thuật Dữ liệu & Xử lý Chuỗi Thời gian (04/2023 - 01/2025)", "Phần II: ")
    format_bullet("Mô hình Định lượng Tài chính CAMEL & Thuật toán Chuẩn hóa Radar", "Phần III: ")
    format_bullet("Kiến trúc Giao diện UI/UX Terminal & Giải pháp Chuyển đổi Theme Dark/Light", "Phần IV: ")
    format_bullet("Công cụ Kiểm toán Cân đối BCTC 100% Math Reconciliation Engine", "Phần V: ")
    format_bullet("Truyền thông Báo chí Số & Phòng Sáng tạo TikTok (@nqs.kinhte)", "Phần VI: ")
    format_bullet("Bảng Ánh xạ Năng lực Ứng viên với Bản Mô tả Công việc (JD Mapping)", "Phần VII: ")
    format_bullet("Hướng dẫn Cài đặt, Vận hành & Triển khai Hệ thống (Deployment Guide)", "Phần VIII: ")

    # =========================================================================
    # PHẦN I: BỐI CẢNH THỊ TRƯỜNG & MỤC TIÊU CHIẾN LƯỢC
    # =========================================================================
    format_heading1("PHẦN I: BỐI CẢNH THỊ TRƯỜNG & MỤC TIÊU CHIẾN LƯỢC")
    format_heading2("1. Bối cảnh Vĩ mô và Ngành Ngân hàng Giai đoạn 04/2023 - 01/2025")
    format_paragraph(
        "Giai đoạn từ tháng 04/2023 đến tháng 01/2025 là một trong những chu kỳ bản lề và đầy biến động của thị trường tài chính Việt Nam. Ngân hàng Nhà nước (NHNN) đã thực hiện 4 đợt cắt giảm lãi suất điều hành liên tiếp nhằm hạ nhiệt chi phí vốn và kích cầu tăng trưởng kinh tế sau các cú sốc thanh khoản cuối năm 2022. "
        "Tuy nhiên, sự phục hồi của nền kinh tế diễn ra không đồng đều, đặt hệ thống ngân hàng thương mại trước các thách thức đa chiều:"
    )
    format_bullet("Biên lãi thuần (NIM) bị nén chặt trong nửa đầu năm 2023 do chi phí huy động vốn kỳ hạn cao của năm 2022 vẫn còn hiệu lực, trong khi lãi suất cho vay phải giảm nhanh theo chỉ đạo hỗ trợ doanh nghiệp.", "• Áp lực Biên lãi thuần: ")
    format_bullet("Thị trường bất động sản đóng băng và xuất khẩu suy giảm đẩy nợ xấu nội bảng và nợ tiềm ẩn tăng vọt. Ngày 23/04/2023, NHNN ban hành Thông tư 02/2023/TT-NHNN cho phép cơ cấu lại thời hạn trả nợ và giữ nguyên nhóm nợ, tạo ra một 'khoảng lặng' kế toán kỹ thuật cần được phân tích và bóc tách chuyên sâu.", "• Cơ chế Thông tư 02: ")
    format_bullet("Các ngân hàng sở hữu tỷ lệ tiền gửi không kỳ hạn (CASA) vượt trội (như MBB, TCB) và tỷ lệ bao phủ nợ xấu (LLR) dày dặn (như VCB, BID) thể hiện khả năng chống chịu và phục hồi biên lợi nhuận vượt trội so với phần còn lại của hệ thống.", "• Sự phân hóa chất lượng tài sản: ")

    format_heading2("2. Mục tiêu Xây dựng Hệ thống VN-FINANCE INSIGHTS")
    format_paragraph(
        "Hệ thống VN-FINANCE INSIGHTS được kiến tạo nhằm trả lời trọn vẹn nhu cầu tác nghiệp thực tế của một Chuyên viên Phân tích Dữ liệu Chứng khoán tại Chuyên trang Người Quan Sát, hướng tới 3 mục tiêu cốt lõi:"
    )
    format_bullet("Xây dựng kho dữ liệu tài chính ngân hàng chuẩn hóa 8 quý (Q1/2023 - Q4/2024) và chuỗi giá giao dịch thị trường hàng ngày (04/2023 - 01/2025) với 100% tính toàn vẹn toán học.", "1. Chuẩn hóa & Tự động hóa: ")
    format_bullet("Trực quan hóa đa chiều qua mô hình CAMEL, dải định giá P/E Bands, và radar chart chuẩn hóa phân vị ngành, giúp ban biên tập và độc giả nắm bắt câu chuyện doanh nghiệp chỉ trong vài giây.", "2. Phân tích Định lượng Chuyên sâu: ")
    format_bullet("Tạo cầu nối trực tiếp từ số liệu khô khan sang sản phẩm nội dung đa phương tiện, bao gồm bài viết phân tích báo chí chuyên sâu và kịch bản video ngắn TikTok đạt chuẩn xu hướng mạng xã hội.", "3. Báo chí Dữ liệu Thực chiến: ")

    # =========================================================================
    # PHẦN II: KIẾN TRÚC DỮ LIỆU & XỬ LÝ CHUỖI THỜI GIAN
    # =========================================================================
    format_heading1("PHẦN II: KIẾN TRÚC KỸ THUẬT DỮ LIỆU & XỬ LÝ CHUỖI THỜI GIAN")
    format_heading2("1. Phân định Hai Luồng Dữ liệu Độc lập (Market vs. Fundamentals)")
    format_paragraph(
        "Một trong những sai lầm phổ biến nhất của các hệ thống phân tích tài chính sơ cấp là việc gộp chung dữ liệu giá giao dịch biến động theo từng giây vào các chỉ số BCTC tĩnh. VN-FINANCE INSIGHTS phân định nghiêm ngặt 2 luồng dữ liệu độc lập:"
    )

    # Bảng phân định dữ liệu
    tbl_data = doc.add_table(rows=3, cols=4)
    tbl_data.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Đặc tính", "Luồng Dữ liệu Thị trường (Market Data)", "Luồng Dữ liệu BCTC (Fundamentals)", "Cơ chế Tương tác"]
    for j, text in enumerate(headers):
        cell = tbl_data.cell(0, j)
        set_cell_background(cell, "1E293B")
        set_cell_margins(cell, 80, 80, 100, 100)
        p = cell.paragraphs[0]
        r = p.add_run(text)
        r.font.name = "Segoe UI"
        r.font.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    data_rows = [
        ["Tần suất & Chu kỳ", "Liên tục theo ngày (04/2023 - 01/2025, ~500+ phiên)", "Chốt định kỳ theo Quý (8 quý: Q1/2023 - Q4/2024)", "Định giá P/E & P/B kết hợp giá ngày với EPS/BVPS quý gần nhất"],
        ["Biến số Cốt lõi", "VN-Index, Khối lượng giao dịch, Giá cổ phiếu, MA20, MA50", "Dư nợ, Tiền gửi, 5 nhóm nợ, Thu nhập lãi, Dự phòng, Vốn CSH", "Radar CAMEL và Bảng điểm Sức khỏe chạy hoàn toàn trên BCTC"]
    ]
    for i, row in enumerate(data_rows):
        for j, val in enumerate(row):
            cell = tbl_data.cell(i + 1, j)
            set_cell_background(cell, "F8FAFC" if i % 2 == 0 else "FFFFFF")
            set_cell_margins(cell, 70, 70, 100, 100)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.name = "Segoe UI"
            r.font.size = Pt(9)
            r.font.color.rgb = RGBColor(0x33, 0x41, 0x55)

    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(4)

    format_heading2("2. Xử lý Đứt gãy Dữ liệu TTM và Biến động Kỳ (QoQ / YoY)")
    format_paragraph(
        "Các chỉ số phân tích đòi hỏi dữ liệu quá khứ 4 quý như Lợi nhuận trượt 12 tháng (Net Profit TTM), ROE TTM, hoặc Tăng trưởng dư nợ cùng kỳ (YoY) thường gặp phải lỗi thiếu dữ liệu (Missing / NaN Values) tại các quý ban đầu (Q1-Q3/2023) nếu không có số liệu năm 2022. "
        "Hệ thống triển khai thuật toán thích ứng (Adaptive Rolling Calculation Engine) trong module `src/financial_metrics.py`:"
    )
    format_bullet(
        "Đối với các kỳ có ít hơn 4 quý lịch sử, hàm `calc_ttm_profit` tính toán tổng lợi nhuận của các quý hiện có và nhân với hệ số điều chỉnh chuẩn hóa `factor = 4.0 / len(window)`. Nhờ đó, lợi nhuận TTM luôn đại diện chính xác cho quy mô năm hóa mà không trả về giá trị None hay NaN.",
        "• Thuật toán Quy đổi TTM Thích ứng: "
    )
    format_bullet(
        "Biến động cùng kỳ `diff(4)` được thiết lập cơ chế fallback tự động: nếu chưa đủ 4 quý, hệ thống tự động gán giá trị biến động quý `diff(1)` làm ước lượng an toàn, kết hợp tiền tố cảnh báo hiển thị trên giao diện.",
        "• Cơ chế Fallback Biến động YoY: "
    )

    format_heading2("3. Tích hợp Chú thích Nghiệp vụ Chu kỳ Vĩ mô (Footnotes)")
    format_paragraph(
        "Toàn bộ bảng biểu và biểu đồ NPL, NIM, LLR trên Dashboard đều được đính kèm chú thích nghiệp vụ chuyên sâu: "
        "'*Lưu ý nghiệp vụ: Giai đoạn 2023 - 2024, tỷ lệ nợ xấu ghi nhận trên sổ sách chịu tác động điều tiết từ Thông tư 02/2023/TT-NHNN cho phép cơ cấu nợ và giữ nguyên nhóm nợ. Biên lãi thuần (NIM) chạm đáy vào Q2/2023 trước khi phục hồi theo chu kỳ giảm chi phí vốn huy động.' Điều này thể hiện tư duy định lượng gắn liền với thực tế ngành của một nhà phân tích chuyên nghiệp."
    )

    # =========================================================================
    # PHẦN III: MÔ HÌNH ĐỊNH LƯỢNG TÀI CHÍNH CAMEL & RADAR BENCHMARK
    # =========================================================================
    format_heading1("PHẦN III: MÔ HÌNH ĐỊNH LƯỢNG TÀI CHÍNH CAMEL & RADAR BENCHMARK")
    format_heading2("1. Công thức và Bản chất Kinh tế của Các Chỉ số Cốt lõi")
    format_paragraph(
        "Hệ thống tính toán và theo dõi 6 chỉ số ngân hàng cốt lõi tuân thủ nghiêm ngặt chuẩn mực tài chính quốc tế và quy định của Ngân hàng Nhà nước:"
    )

    tbl_camel = doc.add_table(rows=7, cols=4)
    tbl_camel.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_headers = ["Chỉ số", "Công thức Toán học", "Bản chất Kinh tế & Chuẩn Ngành", "Trọng số Đánh giá"]
    for j, text in enumerate(c_headers):
        cell = tbl_camel.cell(0, j)
        set_cell_background(cell, "1E293B")
        set_cell_margins(cell, 80, 80, 100, 100)
        p = cell.paragraphs[0]
        r = p.add_run(text)
        r.font.name = "Segoe UI"
        r.font.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    c_rows = [
        ["Biên lãi thuần (NIM)", "NIM = (NII * 4) / Earning Assets Avg", "Hiệu quả sinh lời của tài sản cho vay. Ngân hàng bán lẻ (MBB, TCB) thường đạt 4.0% - 4.5%; Big 4 (VCB, BID) đạt 2.8% - 3.3%.", "20%"],
        ["Tỷ lệ nợ xấu (NPL)", "NPL = (Nợ nhóm 3+4+5) / Tổng dư nợ", "Thước đo rủi ro tín dụng. Mức an toàn theo quy định NHNN là dưới 3.0%. VCB dẫn đầu thị trường với mức ~1.0%.", "20%"],
        ["Bao phủ nợ xấu (LLR)", "LLR = Quỹ Dự phòng / Nợ nhóm 3+4+5", "Tấm đệm phòng thủ tài chính. VCB đạt kỷ lục 250% (cứ 1 đồng nợ xấu có 2.5 đồng dự phòng); BID đạt ~180%.", "15%"],
        ["Tiền gửi không kỳ hạn (CASA)", "CASA = Tiền gửi KKH / Tổng tiền gửi KH", "Lợi thế chi phí vốn rẻ vượt trội (chỉ 0.2% - 0.5%/năm). MBB và TCB thống trị với CASA 40% - 42%.", "30%"],
        ["Tỷ suất sinh lời CSH (ROE)", "ROE TTM = Lợi nhuận sau thuế TTM / Vốn CSH", "Hiệu quả sử dụng vốn của cổ đông. MBB và VCB duy trì hiệu suất cao kỷ lục từ 20% đến 22%/năm.", "15%"],
        ["Định giá P/E & P/B", "P/E = Giá / EPS; P/B = Giá / BVPS", "Thước đo định giá cổ phiếu so với khả năng sinh lời và giá trị sổ sách.", "Tham chiếu định giá"]
    ]
    for i, row in enumerate(c_rows):
        for j, val in enumerate(row):
            cell = tbl_camel.cell(i + 1, j)
            set_cell_background(cell, "F8FAFC" if i % 2 == 0 else "FFFFFF")
            set_cell_margins(cell, 70, 70, 100, 100)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.name = "Segoe UI"
            r.font.size = Pt(9)
            r.font.color.rgb = RGBColor(0x33, 0x41, 0x55)

    p_sp2 = doc.add_paragraph()
    p_sp2.paragraph_format.space_before = Pt(4)

    format_heading2("2. Thuật toán Chuẩn hóa Radar Chart (Min-Max Scaling)")
    format_paragraph(
        "Một vấn đề nghiêm trọng trong các biểu đồ mạng nhện truyền thống là việc đưa trực tiếp các chỉ số có đơn vị khác nhau (%, lần, tỷ đồng) lên cùng các trục, dẫn đến việc biến số có độ lớn tuyệt đối cao (như LLR 200%) áp đảo hoàn toàn các biến số có biên độ hẹp (như NPL 1.5% hay NIM 4%). "
        "Hệ thống giải quyết triệt để bằng hàm `compute_camel_radar_dimensions()`:"
    )
    format_bullet("Mỗi chỉ số được chuẩn hóa tuyến tính về thang điểm phân vị ngành từ 10 đến 100 điểm dựa trên biên độ phân phối thực tế của ngành ngân hàng Việt Nam.", "• Min-Max Normalization: ")
    format_bullet("Đối với tỷ lệ nợ xấu (NPL), chỉ số mang tính nghịch biến (nợ xấu càng thấp thì điểm càng cao). Thuật toán tự động đảo ngược phân vị: `Score = 110.0 - Normal_Score`.", "• Xử lý Trục Nghịch biến (Inverted Axis): ")
    format_bullet("Hỗ trợ chọn đồng thời từ 1 đến 3 ngân hàng (Multi-select Peer Benchmark) để vẽ các lớp đa giác bán trong suốt chồng lên nhau, giúp người dùng so sánh trực quan thế mạnh tương đối giữa các ngân hàng ngay lập tức.", "• So sánh Chồng lớp Đa ngân hàng: ")

    format_heading2("3. Thuật toán Bảng điểm Sức khỏe Tài chính Ngân hàng (CAMEL Scorecard)")
    format_paragraph(
        "Hệ thống phân loại các ngân hàng theo 3 nhóm phân hạng rõ ràng dựa trên tổng điểm sức khỏe tài chính tổng hợp:"
    )
    format_bullet("Điểm tổng hợp $\\ge 80.0$, sở hữu tấm đệm dự phòng nợ xấu dày dặn (>180%) và tỷ lệ nợ xấu thấp vượt trội (<1.5%). Đại diện tiêu biểu: VCB.", "• TIER 1 - PHÒNG THỦ TOÀN DIỆN: ")
    format_bullet("Điểm tổng hợp từ 70.0 đến 79.9, biên lãi thuần cao (>4.0%) nhờ lợi thế tỷ lệ CASA dẫn đầu hệ thống (>38%). Đại diện: MBB, TCB.", "• CASA KING - DẪN ĐẦU VỐN RẺ: ")
    format_bullet("Quy mô tổng tài sản và dư nợ vượt 2 triệu tỷ đồng, giữ vai trò huyết mạch tín dụng của nền kinh tế. Đại diện: BID.", "• TÍN DỤNG QUY MÔ LỚN: ")

    # =========================================================================
    # PHẦN IV: KIẾN TRÚC GIAO DIỆN UI/UX TERMINAL & THEME ENGINE
    # =========================================================================
    format_heading1("PHẦN IV: KIẾN TRÚC GIAO DIỆN UI/UX TERMINAL & THEME ENGINE")
    format_heading2("1. Hệ thống Nhận diện Thương hiệu Chuyên trang Người Quan Sát")
    format_paragraph(
        "Giao diện Dashboard được thiết kế theo chuẩn mực Financial Data Terminal cao cấp (Bloomberg Terminal / FactSet style), tích hợp trọn vẹn bản sắc thương hiệu của Chuyên trang Người Quan Sát (nguoiquansat.vn):"
    )
    format_bullet("Màu cam biểu tượng của Người Quan Sát (#EE7224), sử dụng cho thanh điều hướng chính, các nút nhấn hành động, đường viền tiêu đề và các chỉ số điểm nhấn quan trọng.", "• Màu sắc Chủ đạo (Brand Primary): ")
    format_bullet("Tím than hoàng gia (#3B1B70), sử dụng cho nhãn thương hiệu, nền phụ trợ cao cấp và các badge thể loại chuyên sâu.", "• Màu sắc Thứ cấp (Brand Purple): ")
    format_bullet("Đỏ tín hiệu (#ED1C24) với hiệu ứng nhấp nháy phát sáng (pulsing glow 1.5s) cho chấm tròn 'LIVE TERMINAL', khẳng định tính thời sự và cập nhật trực tiếp của dữ liệu.", "• Tín hiệu Trực tiếp (Live Dot): ")
    format_bullet("Tích hợp trực tiếp file đồ họa vector `assets/logo_nqs.svg` với độ sắc nét hoàn hảo trên mọi độ phân giải màn hình Retina và 4K.", "• Logo Vector Chính thức: ")

    format_heading2("2. Giải quyết Triệt để Lỗi Tương phản & Xung đột Màu (WCAG AA)")
    format_paragraph(
        "Vấn đề kinh điển của các ứng dụng Streamlit khi hỗ trợ cả Dark Mode và Light Mode là việc chữ bị mất tích hoặc chìm vào nền (ví dụ chữ trắng trên nền sáng hoặc chữ đen trên nền tối) do việc hardcode tĩnh các mã màu hex trong mã nguồn HTML/CSS. "
        "VN-FINANCE INSIGHTS đã tái cấu trúc toàn diện hệ thống style theo chuẩn Dynamic Theme Engine:"
    )

    tbl_theme = doc.add_table(rows=6, cols=3)
    tbl_theme.alignment = WD_TABLE_ALIGNMENT.CENTER
    th_headers = ["Thành phần Giao diện", "Chế độ Nền Tối (Dark Terminal Mode)", "Chế độ Nền Sáng (Light Corporate Mode)"]
    for j, text in enumerate(th_headers):
        cell = tbl_theme.cell(0, j)
        set_cell_background(cell, "1E293B")
        set_cell_margins(cell, 80, 80, 100, 100)
        p = cell.paragraphs[0]
        r = p.add_run(text)
        r.font.name = "Segoe UI"
        r.font.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    th_rows = [
        ["Màu nền ứng dụng (App Background)", "#0E1117 (Deep Black Dark Theme)", "#F8FAFC (Clean Crisp Slate Light)"],
        ["Văn bản Chính (Primary Text)", "#FFFFFF / #F1F5F9 (Tương phản tuyệt đối)", "#0F172A (Navy sẫm, độ tương phản 12.5:1)"],
        ["Văn bản Phụ & Nhãn (Labels / Sub-text)", "#94A3B8 (Xám bạc sáng, tương phản 5.2:1)", "#334155 (Xám đậm, tương phản 7.1:1)"],
        ["Thẻ dữ liệu & Khung viền (Cards & Borders)", "Nền #161B22, viền #30363D", "Nền #FFFFFF, viền #E2E8F0 với bóng đổ nhẹ"],
        ["Template Biểu đồ Plotly", "plotly_dark (Nền trong suốt, lưới xám tối)", "plotly_white (Nền trong suốt, lưới mảnh sáng)"]
    ]
    for i, row in enumerate(th_rows):
        for j, val in enumerate(row):
            cell = tbl_theme.cell(i + 1, j)
            set_cell_background(cell, "F8FAFC" if i % 2 == 0 else "FFFFFF")
            set_cell_margins(cell, 70, 70, 100, 100)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.name = "Segoe UI"
            r.font.size = Pt(9)
            r.font.color.rgb = RGBColor(0x33, 0x41, 0x55)

    p_sp3 = doc.add_paragraph()
    p_sp3.paragraph_format.space_before = Pt(4)

    format_heading2("3. Thành phần Terminal Tương tác Đỉnh cao")
    format_bullet("Băng chuyền chứng khoán chạy ngang liên tục với chu kỳ 32 giây, hiển thị VN-Index, giá trị thanh khoản phiên, P/E toàn thị trường và giá cổ phiếu các ngân hàng lớn. Tự động tạm dừng (pause on hover) khi người dùng di chuột để xem chi tiết.", "• Dynamic Marquee Ticker: ")
    format_bullet("Các thẻ chỉ số, nhãn phân hạng (TIER 1, CASA KING) sử dụng kênh màu alpha (ví dụ `rgba(59, 130, 246, 0.15)`) giúp hiển thị hài hòa, nổi bật trên cả nền sáng và nền tối mà không làm nhòe văn bản.", "• Semi-transparent Metric Badges: ")

    # =========================================================================
    # PHẦN V: CÔNG CỤ KIỂM TOÁN CÂN ĐỐI BCTC 100% MATH RECONCILIATION
    # =========================================================================
    format_heading1("PHẦN V: CÔNG CỤ KIỂM TOÁN CÂN ĐỐI BCTC 100% MATH RECONCILIATION")
    format_heading2("1. Tầm quan trọng của Đạo đức Số liệu trong Báo chí Tài chính")
    format_paragraph(
        "Đối với một cơ quan báo chí tài chính uy tín như Tạp chí Người Quan Sát, sai số dữ liệu hoặc việc các khoản mục trên bảng cân đối kế toán không khớp nhau là sai phạm tối kỵ làm tổn hại uy tín thương hiệu. "
        "VN-FINANCE INSIGHTS tích hợp một module kiểm toán độc lập (Tab 4: Math Reconciliation & Data Quality Audit) nhằm xác minh tính toàn vẹn của mọi bản ghi dữ liệu trước khi xuất bản."
    )

    format_heading2("2. Hai Phương trình Kiểm toán Tuyệt đối")
    format_bullet(
        "Tổng giá trị của 5 nhóm nợ (Nhóm 1: Đủ tiêu chuẩn; Nhóm 2: Cần chú ý; Nhóm 3: Dưới tiêu chuẩn; Nhóm 4: Nghi ngờ; Nhóm 5: Có khả năng mất vốn) phải bằng chính xác 100.000% Tổng Dư nợ Cho vay Khách hàng. Sai lệch cho phép (tolerance): $0.0000$ VNĐ.",
        "• Phương trình Cân đối 5 Nhóm nợ: "
    )
    format_bullet(
        "Tổng Tài sản Bảng Cân đối Kế toán phải bằng Tổng Nợ phải trả cộng Vốn Chủ sở hữu: $\\text{Total Assets} = \\text{Total Liabilities} + \\text{Total Equity}$. Tỷ lệ chênh lệch kiểm toán bằng đúng $0.000%$.",
        "• Phương trình Bảng Cân đối Kế toán: "
    )

    format_heading2("3. Công cụ Xuất Dữ liệu Đa định dạng (Excel & CSV)")
    format_paragraph(
        "Hệ thống cung cấp tính năng xuất toàn bộ bộ dữ liệu BCTC đã được làm sạch và tính toán kèm các chỉ số phân tích sang định dạng Excel nhiều sheet (`VN_Finance_Banking_Reconciliation_Audit.xlsx`) và định dạng CSV mã hóa UTF-8-BOM. Điều này phục vụ trực tiếp cho các nhà báo, chuyên viên phân tích độc lập kiểm tra chéo và trích xuất dữ liệu làm tư liệu bài viết."
    )

    # =========================================================================
    # PHẦN VI: TRUYỀN THÔNG BÁO CHÍ SỐ & PHÒNG SÁNG TẠO TIKTOK
    # =========================================================================
    format_heading1("PHẦN VI: TRUYỀN THÔNG BÁO CHÍ SỐ & PHÒNG SÁNG TẠO TIKTOK")
    format_heading2("1. Chuyển hóa Dữ liệu thành Nội dung Viral trên Mạng Xã hội")
    format_paragraph(
        "Người Quan Sát sở hữu kênh truyền thông số phát triển mạnh mẽ trên nền tảng TikTok (@nqs.kinhte). Để thu hút thế hệ nhà đầu tư trẻ (Gen Z và Millennials), dữ liệu tài chính phức tạp cần được chuyển hóa thành các video ngắn sinh động, dễ hiểu nhưng vẫn giữ nguyên độ chính xác học thuật. "
        "Hệ thống VN-FINANCE INSIGHTS tích hợp sẵn Tab 'TikTok Creative Lab' với 4 kịch bản video viral hoàn chỉnh:"
    )

    # Bảng kịch bản TikTok
    tbl_tt = doc.add_table(rows=5, cols=4)
    tbl_tt.alignment = WD_TABLE_ALIGNMENT.CENTER
    tt_headers = ["Mã Kịch bản", "Tiêu đề Video", "Hook 3 Giây Đầu", "Thông điệp Dữ liệu Cốt lõi (Data Climax)"]
    for j, text in enumerate(tt_headers):
        cell = tbl_tt.cell(0, j)
        set_cell_background(cell, "1E293B")
        set_cell_margins(cell, 80, 80, 100, 100)
        p = cell.paragraphs[0]
        r = p.add_run(text)
        r.font.name = "Segoe UI"
        r.font.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    tt_rows = [
        ["TT-01", "CASA là gì và vì sao MBB, TCB dẫn đầu?", "Bạn có biết ngân hàng đang 'vay' tiền bạn với giá gần như 0 đồng?", "MBB và TCB huy động vốn rẻ 40-42%, giúp biên lãi NIM vượt 4.3%, cao gấp rưỡi ngân hàng khác."],
        ["TT-02", "Vì sao Vietcombank trích lập dự phòng 250%?", "Ngân hàng này cứ 1 đồng nợ xấu lại cất sẵn 2.5 đồng trong két!", "Tấm đệm LLR 250% của VCB là thành trì an toàn số 1, miễn nhiễm trước mọi rủi ro thị trường."],
        ["TT-03", "Hết hạn Thông tư 02: Nợ xấu ngân hàng sẽ lộ ra sao?", "Khoản nợ 'tàng hình' 2 năm qua sắp sửa phải ghi nhận vào BCTC?", "Phân tích tác động phân loại lại nợ và ngân hàng nào có đệm dự phòng đủ dày để vượt bão."],
        ["TT-04", "P/E VN-Index 16.2x: Rẻ hay Đắt để mua cổ phiếu Bank?", "Đừng chỉ nhìn điểm số 1,280! Định giá thực sự của thị trường đang ở đâu?", "So sánh P/E lịch sử với P/B nhóm ngân hàng để tìm ra cơ hội đầu tư giá trị."]
    ]
    for i, row in enumerate(tt_rows):
        for j, val in enumerate(row):
            cell = tbl_tt.cell(i + 1, j)
            set_cell_background(cell, "F8FAFC" if i % 2 == 0 else "FFFFFF")
            set_cell_margins(cell, 70, 70, 100, 100)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.name = "Segoe UI"
            r.font.size = Pt(9)
            r.font.color.rgb = RGBColor(0x33, 0x41, 0x55)

    p_sp4 = doc.add_paragraph()
    p_sp4.paragraph_format.space_before = Pt(4)

    format_heading2("2. Bài viết Mẫu Chuẩn Báo chí Tài chính")
    format_paragraph(
        "Hệ thống tích hợp toàn văn bài phân tích: 'Bức tranh phân hóa biên lãi thuần NIM và chất lượng tài sản nhóm ngân hàng thương mại' (lưu trữ tại `docs/SAMPLE_ANALYSIS.md`). Bài viết kết hợp hài hòa giữa sapo báo chí, bảng dữ liệu đối soát và các khuyến nghị đầu tư phòng thủ / bứt phá, chứng minh năng lực kết hợp giữa kỹ năng lập trình định lượng và văn phong báo chí sắc sảo."
    )

    # =========================================================================
    # PHẦN VII: BẢNG ÁNH XẠ NĂNG LỰC ỨNG VIÊN VỚI JD (COMPETENCY MAPPING)
    # =========================================================================
    format_heading1("PHẦN VII: BẢNG ÁNH XẠ NĂNG LỰC ỨNG VIÊN VỚI BẢN MÔ TẢ CÔNG VIỆC")
    format_paragraph(
        "Bảng dưới đây đối chiếu trực tiếp các yêu cầu tuyển dụng cốt lõi của vị trí Chuyên viên Phân tích & Phát triển Dữ liệu Chứng khoán - Doanh nghiệp tại Chuyên trang Người Quan Sát với các minh chứng thực tế được triển khai trong dự án VN-FINANCE INSIGHTS:"
    )

    tbl_jd = doc.add_table(rows=6, cols=3)
    tbl_jd.alignment = WD_TABLE_ALIGNMENT.CENTER
    jd_headers = ["Yêu cầu trong Tuyển dụng (JD Requirements)", "Minh chứng Cụ thể trong Dự án VN-FINANCE INSIGHTS", "Mức độ Đáp ứng"]
    for j, text in enumerate(jd_headers):
        cell = tbl_jd.cell(0, j)
        set_cell_background(cell, "1E293B")
        set_cell_margins(cell, 80, 80, 100, 100)
        p = cell.paragraphs[0]
        r = p.add_run(text)
        r.font.name = "Segoe UI"
        r.font.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    jd_rows = [
        ["1. Phân tích BCTC & Dữ liệu Doanh nghiệp Niêm yết", "Xử lý chuỗi dữ liệu BCTC 8 quý của 4 ngân hàng trụ cột; phân tích sâu 5 nhóm nợ, cơ cấu CASA, biên NIM, trích lập dự phòng và các chính sách vĩ mô (Thông tư 02, điều hành lãi suất).", "Vượt mức kỳ vọng (Senior Level)"],
        ["2. Kỹ năng Lập trình Định lượng (Python, Pandas, NumPy)", "Xây dựng 2 module độc lập (`data_pipeline.py`, `financial_metrics.py`), thuật toán TTM thích ứng, xử lý Missing Values, chuẩn hóa Min-Max scaling phân vị ngành.", "Hoàn toàn đáp ứng (Clean Code, PEP 8)"],
        ["3. Trực quan hóa Dữ liệu & Thiết kế Dashboard Chuyên nghiệp", "Phát triển Web App tương tác với Streamlit, Plotly, CSS Theme Engine (Dark/Light Mode đạt chuẩn WCAG AA), Marquee Ticker, Radar Chart đa lớp.", "Chuyên nghiệp (UI/UX Terminal cao cấp)"],
        ["4. Tư duy Báo chí Số & Sáng tạo Truyền thông Đa phương tiện", "Module TikTok Creative Lab với 4 kịch bản video ngắn hoàn chỉnh; bài viết phân tích báo chí chuyên sâu theo văn phong tòa soạn Người Quan Sát.", "Đặc biệt phù hợp định hướng tòa soạn"],
        ["5. Đạo đức Số liệu & Khả năng Kiểm toán Dữ liệu", "Xây dựng hệ thống đối soát 100% Math Balance cho 5 nhóm nợ và bảng CĐKT; cung cấp công cụ xuất dữ liệu Excel/CSV minh bạch.", "Tuyệt đối chuẩn xác (Zero Error)"]
    ]
    for i, row in enumerate(jd_rows):
        for j, val in enumerate(row):
            cell = tbl_jd.cell(i + 1, j)
            set_cell_background(cell, "F8FAFC" if i % 2 == 0 else "FFFFFF")
            set_cell_margins(cell, 70, 70, 100, 100)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.name = "Segoe UI"
            r.font.size = Pt(9)
            r.font.color.rgb = RGBColor(0x33, 0x41, 0x55)

    p_sp5 = doc.add_paragraph()
    p_sp5.paragraph_format.space_before = Pt(4)

    # =========================================================================
    # PHẦN VIII: HƯỚNG DẪN CÀI ĐẶT, VẬN HÀNH & TRIỂN KHAI
    # =========================================================================
    format_heading1("PHẦN VIII: HƯỚNG DẪN CÀI ĐẶT, VẬN HÀNH & TRIỂN KHAI")
    format_heading2("1. Cấu trúc Thư mục Dự án Chuẩn hóa")
    format_paragraph(
        "Mã nguồn được tổ chức theo cấu trúc phân tầng rõ ràng, sẵn sàng mở rộng và đóng gói triển khai:"
    )

    tbl_tree = doc.add_table(rows=8, cols=2)
    tbl_tree.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_headers = ["Đường dẫn Thư mục / Tập tin", "Vai trò và Chức năng Nghiệp vụ"]
    for j, text in enumerate(t_headers):
        cell = tbl_tree.cell(0, j)
        set_cell_background(cell, "1E293B")
        set_cell_margins(cell, 80, 80, 100, 100)
        p = cell.paragraphs[0]
        r = p.add_run(text)
        r.font.name = "Segoe UI"
        r.font.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    t_rows = [
        ["app.py", "Điểm khởi chạy ứng dụng Streamlit Dashboard (6 Tabs chức năng, Theme Engine, Marquee Ticker)."],
        ["src/data_pipeline.py", "Module tạo lập, kiểm toán và chuẩn hóa chuỗi dữ liệu BCTC và thị trường."],
        ["src/financial_metrics.py", "Engine tính toán chỉ số CAMEL, TTM thích ứng, biến động kỳ QoQ/YoY, và Min-Max Radar Scaling."],
        ["assets/logo_nqs.svg", "Logo vector chính thức của Chuyên trang Người Quan Sát lấy từ CDN gốc."],
        ["notebooks/pipeline_demo.ipynb", "Jupyter Notebook nghiên cứu định lượng đã thực thi đầy đủ biểu đồ trực quan hóa."],
        ["docs/DEPLOYMENT_GUIDE.md", "Hướng dẫn triển khai chi tiết lên Streamlit Cloud, Docker container và Render."],
        ["requirements.txt & Dockerfile", "Cấu hình môi trường phụ thuộc, khóa phiên bản tương thích pyarrow>=15.0.0."]
    ]
    for i, row in enumerate(t_rows):
        for j, val in enumerate(row):
            cell = tbl_tree.cell(i + 1, j)
            set_cell_background(cell, "F8FAFC" if i % 2 == 0 else "FFFFFF")
            set_cell_margins(cell, 70, 70, 100, 100)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.name = "Segoe UI"
            r.font.size = Pt(9)
            r.font.color.rgb = RGBColor(0x33, 0x41, 0x55)

    p_sp6 = doc.add_paragraph()
    p_sp6.paragraph_format.space_before = Pt(4)

    format_heading2("2. Lệnh Khởi chạy Nhanh trên Máy Cục bộ (Local Environment)")
    format_paragraph("Để khởi chạy và kiểm thử ứng dụng trên môi trường máy trạm:", bold_prefix="Bước 1: ")
    format_bullet("Cài đặt thư viện: pip install -r requirements.txt", "• ")
    format_bullet("Khởi chạy Dashboard: streamlit run app.py --server.port 8501", "• ")
    format_bullet("Truy cập trình duyệt: http://localhost:8501", "• ")

    format_heading2("3. Hướng dẫn Triển khai Trực tuyến lên Streamlit Community Cloud (Zero-Cost Hosting)")
    format_paragraph("Hệ thống đã được đóng gói hoàn hảo để triển khai công khai lên Streamlit Cloud chỉ với 3 bước:", bold_prefix="Quy trình: ")
    format_bullet("Tạo một kho lưu trữ mới trên GitHub (ví dụ: vn-finance-insights) và đẩy toàn bộ mã nguồn lên bằng các lệnh: git add . -> git commit -m 'Initial release' -> git push origin main.", "1. Đẩy mã nguồn lên GitHub: ")
    format_bullet("Đăng nhập vào share.streamlit.io bằng tài khoản GitHub, bấm 'New app', chọn kho lưu trữ, nhánh main và file khởi chạy app.py.", "2. Kết nối Streamlit Cloud: ")
    format_bullet("Hệ thống tự động cài đặt các dependencies từ requirements.txt và tạo ra đường dẫn công khai (ví dụ: https://vn-finance-insights.streamlit.app) để ứng viên đính kèm trực tiếp vào CV và thư xin việc.", "3. Nhận Link Demo Trực tiếp: ")

    # =========================================================================
    # KẾT LUẬN & CAM KẾT
    # =========================================================================
    p_div2 = doc.add_paragraph()
    p_div2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_div2.paragraph_format.space_before = Pt(14)
    p_div2.paragraph_format.space_after = Pt(10)
    r_div2 = p_div2.add_run("―" * 50)
    r_div2.font.color.rgb = RGBColor(0xCB, 0xD5, 0xE1)

    add_callout_box(
        doc,
        "LỜI KẾT VÀ CAM KẾT ĐÓNG GÓP",
        [
            "Dự án VN-FINANCE INSIGHTS không chỉ là một bài tập kỹ thuật đơn thuần, mà là lời khẳng định mạnh mẽ về năng lực thực chiến, tư duy phân tích định lượng sắc bén, và khả năng thích ứng cao của một Chuyên viên Phân tích & Phát triển Dữ liệu tương lai tại Chuyên trang Người Quan Sát.",
            "Tác giả cam kết sẵn sàng mang toàn bộ kiến trúc dữ liệu, năng lực lập trình và tư duy nội dung đa phương tiện này để đồng hành cùng ban biên tập, nâng cao vị thế dẫn đầu của Người Quan Sát trong kỷ nguyên Báo chí Dữ liệu Tài chính."
        ],
        border_color="3B1B70",
        bg_color="F5F3FF"
    )

    doc.save(file_path)
    print(f"Đã tạo thành công file Word: {file_path}")

if __name__ == "__main__":
    out_dir = r"d:\VN-FINANCE INSIGHTS"
    out_file = os.path.join(out_dir, "VN-FINANCE_INSIGHTS_PROJECT_DOCUMENTATION.docx")
    build_project_docx(out_file)
