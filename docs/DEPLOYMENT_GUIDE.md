# HƯỚNG DẪN TRIỂN KHAI HỆ THỐNG VN-FINANCE INSIGHTS LÊN INTERNET

Tài liệu hướng dẫn chi tiết các phương án đưa **VN-FINANCE INSIGHTS (Financial Terminal)** từ môi trường cục bộ (Localhost) lên môi trường trực tuyến (Web/Cloud) để gửi đối tác, nhà tuyển dụng, hoặc độc giả trang tin tài chính **Người Quan Sát**.

---

## CÁC FILE CẤU HÌNH ĐÃ ĐƯỢC THIẾT LẬP SẴN TRONG PROJECT

Dự án đã được trang bị đầy đủ bộ tệp triển khai tiêu chuẩn:
- `requirements.txt`: Khai báo các thư viện Python (streamlit, pandas, numpy, plotly, openpyxl...).
- `.streamlit/config.toml`: Cấu hình giao diện Dark Terminal Bloomberg và thiết lập bảo mật/headless server.
- `Procfile`: Phục vụ triển khai trên PaaS (Render, Railway, Heroku).
- `Dockerfile` & `.dockerignore`: Triển khai bằng Docker Container trên VPS/Cloud Server.

---

## PHƯƠNG ÁN 1: TRIỂN KHAI LÊN STREAMLIT COMMUNITY CLOUD (KHUYÊN DÙNG — 100% MIỄN PHÍ & NHANH NHẤT)

Đây là nền tảng điện toán đám mây chính thức của Streamlit, hoàn toàn **miễn phí**, kết nối trực tiếp với GitHub và tự động cập nhật khi bạn push code mới.

### Bước 1: Đưa Code Lên GitHub
Mở Terminal / PowerShell tại thư mục dự án `d:\VN-FINANCE INSIGHTS`:
```bash
# 1. Khởi tạo Git repository (nếu chưa có)
git init

# 2. Thêm toàn bộ source code
git add .

# 3. Commit
git commit -m "feat: VN-Finance Insights Terminal with Bloomberg Dark UI"

# 4. Đổi tên branch thành main
git branch -M main

# 5. Liên kết với GitHub repo của bạn (thay username và repo-name thực tế)
git remote add origin https://github.com/<YOUR_GITHUB_USERNAME>/vn-finance-insights.git

# 6. Đẩy code lên GitHub
git push -u origin main
```

### Bước 2: Deploy Trên Streamlit Cloud
1. Truy cập trang: **[https://share.streamlit.io](https://share.streamlit.io)**
2. Đăng nhập bằng tài khoản **GitHub**.
3. Nhấp vào nút **"New app"** (hoặc "Create app").
4. Điền các trường thông tin:
   - **Repository:** Chọn repository `vn-finance-insights` vừa push.
   - **Branch:** `main`
   - **Main file path:** `app.py`
   - **App URL:** Bạn có thể tùy chỉnh subdomain (ví dụ: `vn-finance-insights.streamlit.app`).
5. Nhấp nút **"Deploy!"**.
6. Quá trình cài đặt tự động mất khoảng **1 - 2 phút**. Sau đó bạn sẽ có một đường link công khai:
   👉 `https://vn-finance-insights.streamlit.app` có thể truy cập mượt mà trên cả máy tính và điện thoại.

---

## PHƯƠNG ÁN 2: TRIỂN KHAI LÊN RENDER.COM HOẶC RAILWAY.APP (PAAS)

Nếu bạn muốn chạy trên hạ tầng PaaS chuyên nghiệp:

### 1. Triển khai trên Render.com (Free Tier):
1. Đăng ký tài khoản tại [https://render.com](https://render.com).
2. Chọn **"New +"** $\rightarrow$ **"Web Service"**.
3. Kết nối với repo GitHub `vn-finance-insights`.
4. Cấu hình:
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
5. Nhấn **"Create Web Service"**.

---

## PHƯƠNG ÁN 3: TRIỂN KHAI BẰNG DOCKER TRÊN VPS RIÊNG (DIGITALOCEAN, AWS, LINODE, VIETTEL IDC)

Dành cho doanh nghiệp hoặc máy chủ riêng:

```bash
# 1. Build image từ Dockerfile đã tạo sẵn
docker build -t vn-finance-insights:latest .

# 2. Chạy container ở background với cổng 8501
docker run -d -p 8501:8501 --name vn-finance-app --restart always vn-finance-insights:latest
```

Sau đó trỏ tên miền (domain) về IP máy chủ và cấu hình Nginx Reverse Proxy kèm chứng chỉ SSL miễn phí (Let's Encrypt).

---

## KIỂM TRA & BẢO TRÌ

- **Kiểm tra trạng thái chạy cục bộ:** `streamlit run app.py` $\rightarrow$ Truy cập `http://localhost:8501`.
- **Cập nhật dữ liệu:** Khi cập nhật số liệu BCTC quý mới vào `src/data_pipeline.py`, chỉ cần `git push`, bản web trên Cloud sẽ tự động nạp dữ liệu mới.
