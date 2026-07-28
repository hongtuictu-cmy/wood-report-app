import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import plotly.express as px

# 1. CẤU HÌNH NGƯỜI DÙNG
# Lưu ý: Cấu trúc dictionary đã được thay đổi để khớp với bản mới
credentials = {
    "usernames": {
        "admin": {
            "name": "Giám Đốc (Admin)",
            "password": "$2b$12$EpxNnlsM6C9S9mD9Z8Z8Z.h5zG6x8x8x8x8x8x8x8x8x8x8x8x8x8", # Pass: 123
        },
        "ketoan": {
            "name": "Kế Toán Viên",
            "password": "$2b$12$EpxNnlsM6C9S9mD9Z8Z8Z.h5zG6x8x8x8x8x8x8x8x8x8x8x8x8x8", # Pass: 456 (Thay mã băm thật vào đây)
        }
    }
}

# Khởi tạo bộ xác thực
# Ở bản mới, tham số truyền vào cần cụ thể hơn
authenticator = stauth.Authenticate(
    credentials,
    "wood_dashboard_cookie", # Tên cookie
    "signature_key_123",     # Khóa chữ ký
    cookie_expiry_days=30
)

# 2. HIỂN THỊ FORM ĐĂNG NHẬP
# Ở bản mới, ta chỉ gọi hàm login(), không gán biến trả về
authenticator.login()

# 3. KIỂM TRA TRẠNG THÁI QUA SESSION STATE
if st.session_state["authentication_status"]:
    # NẾU ĐĂNG NHẬP THÀNH CÔNG
    authenticator.logout('Đăng xuất', 'sidebar')
    
    st.sidebar.title(f"Chào {st.session_state['name']}!")
    
    # Phân quyền dựa trên username
    user_role = st.session_state['username']
    
    if user_role == "admin":
        menu = st.sidebar.radio("Quản trị:", ["CEO Dashboard", "Tài chính P&L", "Dòng tiền"])
    else:
        menu = st.sidebar.radio("Nhân viên:", ["Báo cáo Yield", "Dòng tiền"])

    # --- NỘI DUNG APP (Mẫu) ---
    if menu == "CEO Dashboard":
        st.header("📊 Dashboard Quản Trị")
        st.metric("Doanh thu thực tế", "5.2 Tỷ", "+12%")
        
        # Biểu đồ mẫu
        df = pd.DataFrame({'Tháng': ['T5', 'T6', 'T7'], 'Doanh thu': [4.8, 5.0, 5.2]})
        st.plotly_chart(px.line(df, x='Tháng', y='Doanh thu'))

    elif menu == "Tài chính P&L":
        st.header("📋 Báo cáo P&L Chi Tiết")
        st.write("Dữ liệu tài chính hiển thị tại đây...")

elif st.session_state["authentication_status"] is False:
    st.error('Sai tên đăng nhập hoặc mật khẩu!')
elif st.session_state["authentication_status"] is None:
    st.warning('Vui lòng nhập thông tin để vào hệ thống.')
import streamlit as st
import pandas as pd
import plotly.express as px

# 1. CẤU HÌNH HỆ THỐNG (Phải nằm ở dòng đầu tiên)
st.set_page_config(page_title="Hệ Thống Quản Trị Tài Chính Wood-ERP", layout="wide")

# Tùy chỉnh giao diện bằng CSS
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# 2. SIDEBAR - ĐIỀU HƯỚNG
st.sidebar.title("🌲 WOOD FINANCIAL ERP")
menu = st.sidebar.radio("Phân hệ quản trị:", 
    ["Tổng quan (CEO Dashboard)", "Báo cáo P&L chi tiết", "Phân tích Giá thành & Yield", "Quản lý Dòng tiền"])

# 3. CHỨC NĂNG UPLOAD (Đã sửa lỗi hàm file_uploader)
st.sidebar.markdown("---")
uploaded_file = st.sidebar.file_uploader("Nạp dữ liệu kế toán (Excel/CSV)", type=['xlsx', 'csv'])

# 4. NỘI DUNG CÁC PHÂN HỆ
if menu == "Tổng quan (CEO Dashboard)":
    st.header("📊 Báo Cáo Sức Khỏe Doanh Nghiệp")
    
    # Chỉ số tài chính nhanh
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Doanh thu thuần", "5.2 Tỷ", "+15%")
    col2.metric("Lợi nhuận gộp", "1.8 Tỷ", "34.6%")
    col3.metric("Tồn kho", "12.4 Tỷ", "-2%", delta_color="inverse")
    col4.metric("Dòng tiền thuần", "850 Tr", "-5%")

    st.markdown("---")
    
    # Biểu đồ doanh thu vs Chi phí
    st.subheader("Biến động Doanh thu & Lợi nhuận (6 tháng gần nhất)")
    chart_data = pd.DataFrame({
        'Tháng': ['T2', 'T3', 'T4', 'T5', 'T6', 'T7'],
        'Doanh thu': [4.1, 4.5, 3.8, 5.0, 4.8, 5.2],
        'Lợi nhuận': [1.2, 1.4, 0.9, 1.7, 1.5, 1.8]
    })
    fig = px.line(chart_data, x='Tháng', y=['Doanh thu', 'Lợi nhuận'], markers=True)
    st.plotly_chart(fig, use_container_width=True)

elif menu == "Phân tích Giá thành & Yield":
    st.header("🪵 Phân tích Giá thành Sản xuất & Yield")
    
    c1, c2 = st.columns([1, 2])
    with c1:
        st.write("### Cấu thành giá vốn (COGS)")
        pie_data = pd.DataFrame({
            "Hạng mục": ["Gỗ nguyên liệu", "Nhân công", "Điện năng", "Khác"],
            "Giá trị": [65, 15, 10, 10]
        })
        fig_pie = px.pie(pie_data, values="Giá trị", names="Hạng mục", hole=0.4)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with c2:
        st.write("### Tỷ lệ thu hồi (Yield) theo lô")
        yield_data = pd.DataFrame({
            "Mã lô": ["LOT-01", "LOT-02", "LOT-03", "LOT-04"],
            "Gỗ tròn (m3)": [100, 150, 120, 200],
            "Tỷ lệ Yield (%)": [65, 71, 64, 69]
        })
        st.table(yield_data)

elif menu == "Báo cáo P&L chi tiết":
    st.header("📋 Báo cáo Kết quả Kinh doanh")
    st.info("Dữ liệu đang được lấy từ hệ thống kế toán mặc định.")
    pl_table = pd.DataFrame({
        "Chỉ tiêu": ["Doanh thu thuần", "Giá vốn hàng bán", "Lợi nhuận gộp", "Chi phí quản lý", "Lợi nhuận thuần"],
        "Tháng này (VNĐ)": ["5,200,000,000", "3,400,000,000", "1,800,000,000", "400,000,000", "1,400,000,000"],
        "% Doanh thu": ["100%", "65.4%", "34.6%", "7.7%", "26.9%"]
    })
    st.table(pl_table)

elif menu == "Quản lý Dòng tiền":
    st.header("💸 Quản lý & Dự báo Dòng tiền (Cash Flow)")

    # 1. Chỉ số dòng tiền tổng quát
    c1, c2, c3 = st.columns(3)
    cash_in = 4200000000  # 4.2 Tỷ
    cash_out = 3100000000 # 3.1 Tỷ
    c1.metric("Dòng tiền vào (Tháng này)", f"{cash_in:,.0f} VNĐ", "+5%")
    c2.metric("Dòng tiền ra (Tháng này)", f"{cash_out:,.0f} VNĐ", "+12% (Do nhập gỗ)")
    c3.metric("Số dư cuối kỳ dự kiến", f"{(cash_in - cash_out):,.0f} VNĐ", "Ổn định", delta_color="normal")

    st.markdown("---")

    # 2. Biểu đồ so sánh Thu - Chi theo tuần
    st.subheader("📊 Biến động Thu - Chi theo tuần")
    cash_flow_data = pd.DataFrame({
        'Tuần': ['Tuần 1', 'Tuần 2', 'Tuần 3', 'Tuần 4'],
        'Thu (Tiền hàng)': [1200, 800, 1500, 700],
        'Chi (Nguyên liệu/Lương)': [900, 1100, 600, 500]
    })
    fig_cf = px.bar(cash_flow_data, x='Tuần', y=['Thu (Tiền hàng)', 'Chi (Nguyên liệu/Lương)'], 
                    barmode='group', title="Đơn vị: Triệu VNĐ")
    st.plotly_chart(fig_cf, use_container_width=True)

    # 3. Quản lý Công nợ (Rất quan trọng trong ngành gỗ)
    col_ar, col_ap = st.columns(2)
    
    with col_ar:
        st.subheader("🚩 Công nợ phải thu (AR)")
        ar_data = pd.DataFrame({
            "Khách hàng": ["IKEA USA", "Ashley Furniture", "Lotte Mart"],
            "Số tiền (Triệu)": [850, 1200, 450],
            "Quá hạn": ["15 ngày", "0", "5 ngày"]
        })
        st.table(ar_data)
        st.info("💡 Tip: Ưu tiên đòi nợ IKEA USA để bù đắp dòng tiền nhập gỗ tuần tới.")

    with col_ap:
        st.subheader("🚛 Công nợ phải trả (AP)")
        ap_data = pd.DataFrame({
            "Nhà cung cấp": ["Lâm trường Gia Lai", "Công ty Keo AB", "Điện lực (EVN)"],
            "Số tiền (Triệu)": [1500, 200, 150],
            "Hạn thanh toán": ["25/07", "30/07", "20/07"]
        })
        st.table(ap_data)

    # 4. Dự báo dòng tiền 3 tháng tới
    st.subheader("🔮 Dự báo số dư tiền mặt (3 tháng tới)")
    forecast_data = pd.DataFrame({
        "Tháng": ["Tháng 8", "Tháng 9", "Tháng 10"],
        "Số dư dự kiến (Tỷ)": [1.1, 1.5, 0.8]
    })
    fig_forecast = px.area(forecast_data, x="Tháng", y="Số dư dự kiến (Tỷ)", color_discrete_sequence=['#2ecc71'])
    st.plotly_chart(fig_forecast, use_container_width=True)
    st.warning("⚠️ Chú ý: Dòng tiền tháng 10 dự kiến giảm mạnh do vào mùa cao điểm nhập kho gỗ tròn dự trữ cho tết.")

# 5. THÔNG BÁO HỆ THỐNG
st.sidebar.success("Trạng thái: Máy chủ đã kết nối")
