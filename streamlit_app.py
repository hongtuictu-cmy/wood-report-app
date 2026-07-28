import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import plotly.express as px

# 1. CẤU HÌNH TRANG (Bắt buộc ở dòng đầu tiên)
st.set_page_config(page_title="Hệ Thống Quản Trị Gỗ Wood-ERP", layout="wide")

# 2. THIẾT LẬP TÀI KHOẢN
# Mã băm (hash) dưới đây tương ứng chính xác với mật khẩu '123'
hashed_password_123 = '$2b$12$6pXvH0O/8.pYyS9R7U.mFuC3yWJ6XpG1vUoI6p/8X3R9M2W7V3U1i'

credentials = {
    "usernames": {
        "admin": {
            "name": "Giám Đốc (Admin)",
            "password": hashed_password_123
        },
        "ketoan": {
            "name": "Kế Toán Viên",
            "password": hashed_password_123
        }
    }
}

# Khởi tạo Authenticator
authenticator = stauth.Authenticate(
    credentials,
    "wood_erp_cookie", 
    "key_secure_123", 
    cookie_expiry_days=30
)

# 3. HIỂN THỊ FORM ĐĂNG NHẬP
# Ở bản 0.3.2, hàm login không gán biến trả về trực tiếp
authenticator.login(location='main')

# 4. KIỂM TRA VÀ HIỂN THỊ NỘI DUNG BẢO MẬT
if st.session_state["authentication_status"]:
    # --- KHU VỰC DÀNH CHO NGƯỜI ĐÃ ĐĂNG NHẬP ---
    
    # Nút đăng xuất
    authenticator.logout('Đăng xuất', 'sidebar')
    
    # Giao diện chính
    st.sidebar.success(f"Chào mừng {st.session_state['name']}")
    menu = st.sidebar.selectbox("Phân hệ quản trị:", 
                               ["Tổng quan kinh doanh", "Báo cáo P&L", "Theo dõi sản xuất gỗ"])

    if menu == "Tổng quan kinh doanh":
        st.title("📊 Dashboard Quản Trị Nhà Máy Gỗ")
        c1, c2, c3 = st.columns(3)
        c1.metric("Doanh thu thực tế", "5.2 Tỷ", "+10%")
        c2.metric("Lợi nhuận gộp", "1.8 Tỷ", "34%")
        c3.metric("Tỷ lệ thu hồi (Yield)", "68.5%", "Đạt mục tiêu")
        
        # Biểu đồ mẫu
        df = pd.DataFrame({'Tháng': ['T5', 'T6', 'T7'], 'Doanh thu': [4.8, 5.0, 5.2]})
        st.plotly_chart(px.area(df, x='Tháng', y='Doanh thu', title="Tăng trưởng doanh thu"), use_container_width=True)

    elif menu == "Báo cáo P&L":
        st.title("📋 Báo Cáo Tài Chính Chi Tiết")
        df_pl = pd.DataFrame({
            "Chỉ tiêu": ["Doanh thu", "Giá vốn hàng bán", "Chi phí vận hành", "Lợi nhuận ròng"],
            "Số tiền (VNĐ)": ["5,200,000,000", "3,400,000,000", "450,000,000", "1,350,000,000"]
        })
        st.table(df_pl)

    elif menu == "Theo dõi sản xuất gỗ":
        st.title("🪵 Quản lý Lô Gỗ & Yield")
        st.info("Hệ thống đang theo dõi các lô gỗ xẻ từ xưởng tinh chế.")

elif st.session_state["authentication_status"] is False:
    st.error('Sai tài khoản hoặc mật khẩu.')
    st.info('Gợi ý: admin / 123')

elif st.session_state["authentication_status"] is None:
    # --- TRẠNG THÁI KHI CHƯA ĐĂNG NHẬP ---
    # Ẩn Sidebar hoàn toàn bằng CSS
    st.markdown("""<style>[data-testid="stSidebar"] {display: none;}</style>""", unsafe_allow_html=True)
    
    st.markdown("<h1 style='text-align: center;'>🌲 HỆ THỐNG QUẢN TRỊ WOOD-ERP</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Vui lòng đăng nhập để xem dữ liệu nội bộ.</p>", unsafe_allow_html=True)
