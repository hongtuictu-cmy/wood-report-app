import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import plotly.express as px

# --- 1. CẤU HÌNH TRANG (PHẢI LÀ LỆNH ĐẦU TIÊN) ---
st.set_page_config(page_title="Hệ Thống Quản Trị Wood-ERP", layout="wide")

# --- 2. THIẾT LẬP THÔNG TIN ĐĂNG NHẬP ---
# Admin pass: 123 | Ketoan pass: 123
credentials = {
    "usernames": {
        "admin": {
            "name": "Giám Đốc (Admin)",
            "password": "$2b$12$EpxNnlsM6C9S9mD9Z8Z8Z.h5zG6x8x8x8x8x8x8x8x8x8x8x8x8x8", 
        },
        "ketoan": {
            "name": "Kế Toán Viên",
            "password": "$2b$12$EpxNnlsM6C9S9mD9Z8Z8Z.h5zG6x8x8x8x8x8x8x8x8x8x8x8x8x8", 
        }
    }
}

# Khởi tạo bộ xác thực
authenticator = stauth.Authenticate(
    credentials,
    "wood_erp_cookie", # Tên cookie
    "signature_key_999", # Khóa bảo mật
    cookie_expiry_days=30
)

# --- 3. KIỂM TRA TRẠNG THÁI ĐĂNG NHẬP ---
# Lưu ý: Không hiển thị bất cứ thứ gì ở Sidebar hay Main Page trước khi kiểm tra
authenticator.login('main')

if st.session_state["authentication_status"] == True:
    # =========================================================================
    # KHU VỰC AN TOÀN: CHỈ CHẠY KHI ĐÃ ĐĂNG NHẬP THÀNH CÔNG
    # =========================================================================
    
    # 3.1 TẠO SIDEBAR (Chỉ hiện khi đã đăng nhập)
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/684/684831.png", width=100)
    st.sidebar.title(f"Chào {st.session_state['name']}!")
    
    # Nút đăng xuất nằm trên cùng Sidebar
    authenticator.logout('Đăng xuất hệ thống', 'sidebar')
    
    st.sidebar.markdown("---")
    menu = st.sidebar.radio(
        "DANH MỤC QUẢN TRỊ",
        ["CEO Dashboard", "Báo cáo Tài chính P&L", "Theo dõi Yield (Hao hụt)", "Quản lý Dòng tiền"]
    )

    # 3.2 NỘI DUNG TỪNG PHÂN HỆ
    if menu == "CEO Dashboard":
        st.title("📊 Tổng Quan Tình Hình Kinh Doanh")
        
        # Chỉ số KPI
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Doanh thu", "5.2 Tỷ", "+12%")
        c2.metric("Lợi nhuận gộp", "1.8 Tỷ", "34.6%")
        c3.metric("Tỷ lệ Yield", "68.5%", "Đạt mục tiêu")
        c4.metric("Đơn hàng", "24 PO", "+3")

        st.markdown("---")
        # Biểu đồ doanh thu
        df_line = pd.DataFrame({
            'Tháng': ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7'],
            'Doanh thu': [3.5, 3.8, 4.2, 3.9, 4.8, 5.0, 5.2]
        })
        fig = px.area(df_line, x='Tháng', y='Doanh thu', title="Xu hướng doanh thu (Tỷ VNĐ)")
        st.plotly_chart(fig, use_container_width=True)

    elif menu == "Báo cáo Tài chính P&L":
        st.title("📋 Báo cáo Kết quả Kinh doanh")
        pl_data = pd.DataFrame({
            "Hạng mục": ["Doanh thu thuần", "Giá vốn hàng bán (COGS)", "Lợi nhuận gộp", "Chi phí quản lý", "Lợi nhuận thuần"],
            "Số tiền (VNĐ)": ["5,200,000,000", "3,400,000,000", "1,800,000,000", "450,000,000", "1,350,000,000"],
            "% Doanh thu": ["100%", "65.4%", "34.6%", "8.6%", "26.0%"]
        })
        st.table(pl_data)

    elif menu == "Theo dõi Yield (Hao hụt)":
        st.title("🪵 Phân tích Tỷ lệ Thu hồi Gỗ")
        st.info("Chỉ số Yield = (Khối lượng gỗ phôi / Khối lượng gỗ tròn nhập) x 100")
        
        df_yield = pd.DataFrame({
            "Mã Lô Gỗ": ["LOT-A01", "LOT-A02", "LOT-B01", "LOT-C05"],
            "Loại gỗ": ["Cao su", "Tràm", "Sồi", "Thông"],
            "Yield (%)": [65.2, 68.5, 72.1, 60.8]
        })
        st.bar_chart(df_yield.set_index("Mã Lô Gỗ")["Yield (%)"])
        st.dataframe(df_yield, use_container_width=True)

    elif menu == "Quản lý Dòng tiền":
        st.title("💸 Theo dõi Dòng tiền (Cash Flow)")
        col_ar, col_ap = st.columns(2)
        with col_ar:
            st.subheader("🚩 Phải thu khách hàng (AR)")
            st.table(pd.DataFrame({"Khách": ["IKEA", "Ashley"], "Số tiền": ["850 Tr", "1.2 Tỷ"]}))
        with col_ap:
            st.subheader("🚛 Phải trả NCC (AP)")
            st.table(pd.DataFrame({"NCC": ["Lâm trường A", "Xưởng keo"], "Số tiền": ["500 Tr", "120 Tr"]}))

elif st.session_state["authentication_status"] == False:
    # HIỆN LỖI KHI NHẬP SAI
    st.error('Tên đăng nhập hoặc mật khẩu không chính xác.')
    st.info("Liên hệ Admin nếu bạn quên mật khẩu.")

elif st.session_state["authentication_status"] == None:
    # TRANG CHỜ KHI CHƯA ĐĂNG NHẬP
    st.markdown("<h2 style='text-align: center;'>HỆ THỐNG QUẢN TRỊ NỘI BỘ</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Vui lòng đăng nhập để tiếp tục sử dụng hệ thống.</p>", unsafe_allow_html=True)
    
    # Ẩn toàn bộ Sidebar bằng CSS khi chưa đăng nhập
    st.markdown("""
        <style>
            [data-testid="stSidebar"] {
                display: none;
            }
        </style>
    """, unsafe_allow_html=True)

# =========================================================================
# KẾT THÚC CODE
# =========================================================================
