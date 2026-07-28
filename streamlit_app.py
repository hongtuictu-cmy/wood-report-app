import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import plotly.express as px

# 1. CẤU HÌNH TRANG
st.set_page_config(page_title="Hệ Thống Wood-ERP", layout="wide")

# 2. THÔNG TIN ĐĂNG NHẬP (Mã băm chuẩn của mật khẩu '123')
# Password '123' tương ứng với dãy hash dưới đây
hashed_password = '$2b$12$6pXvH0O/8.pYyS9R7U.mFuC3yWJ6XpG1vUoI6p/8X3R9M2W7V3U1i'

credentials = {
    "usernames": {
        "admin": {
            "name": "Giám Đốc (Admin)",
            "password": hashed_password
        },
        "ketoan": {
            "name": "Kế Toán Viên",
            "password": hashed_password
        }
    }
}

# Khởi tạo Authenticator với phiên bản mới nhất
authenticator = stauth.Authenticate(
    credentials,
    "wood_erp_cookie_2024",
    "signature_key_secret",
    cookie_expiry_days=30
)

# 3. GIAO DIỆN ĐĂNG NHẬP
# Cố định form đăng nhập ở giữa màn hình
name, authentication_status, username = authenticator.login(location='main')

# 4. XỬ LÝ TRẠNG THÁI ĐĂNG NHẬP
if st.session_state["authentication_status"]:
    # --- ĐĂNG NHẬP THÀNH CÔNG ---
    authenticator.logout('Đăng xuất', 'sidebar')
    
    st.sidebar.title(f"Xin chào, {st.session_state['name']}!")
    menu = st.sidebar.radio("CHỨC NĂNG QUẢN TRỊ", 
                           ["CEO Dashboard", "Báo cáo P&L", "Quản lý Yield Gỗ"])

    if menu == "CEO Dashboard":
        st.title("📊 Dashboard Quản Trị Nhà Máy Gỗ")
        col1, col2, col3 = st.columns(3)
        col1.metric("Doanh thu tháng", "5.2 Tỷ", "+10%")
        col2.metric("Lợi nhuận gộp", "1.8 Tỷ", "34%")
        col3.metric("Tỷ lệ Yield", "68.5%", "Đạt")
        
        df = pd.DataFrame({'Tháng': ['T5', 'T6', 'T7'], 'Doanh thu': [4.8, 5.0, 5.2]})
        st.plotly_chart(px.area(df, x='Tháng', y='Doanh thu'), use_container_width=True)

    elif menu == "Báo cáo P&L":
        st.title("📋 Báo cáo Kết quả Kinh doanh")
        st.table(pd.DataFrame({
            "Chỉ tiêu": ["Doanh thu thuần", "Giá vốn hàng bán", "Lợi nhuận gộp"],
            "Số tiền": ["5,200,000,000", "3,400,000,000", "1,800,000,000"]
        }))

    elif menu == "Quản lý Yield Gỗ":
        st.title("🪵 Theo dõi tỷ lệ thu hồi gỗ")
        st.write("Dữ liệu chi tiết các lô gỗ xẻ...")

elif st.session_state["authentication_status"] is False:
    st.error('Tên đăng nhập hoặc mật khẩu không đúng.')
    st.info('Gợi ý: admin / 123')

elif st.session_state["authentication_status"] is None:
    # Ẩn Sidebar khi chưa đăng nhập bằng CSS
    st.markdown("""<style>[data-testid="stSidebar"] {display: none;}</style>""", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>HỆ THỐNG QUẢN TRỊ GỖ ABC</h2>", unsafe_allow_html=True)
    st.info("Vui lòng sử dụng tài khoản được cấp để đăng nhập.")
