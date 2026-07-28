import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import plotly.express as px

# 1. CẤU HÌNH TRANG
st.set_page_config(page_title="Wood ERP System", layout="wide")

# 2. THIẾT LẬP TÀI KHOẢN (Mật khẩu mặc định: 123)
# Chúng ta sử dụng Hasher để tự động tạo mã băm chính xác 100% cho số 123
passwords_to_hash = ['123', '123']
hashed_passwords = stauth.Hasher(passwords_to_hash).generate()

credentials = {
    "usernames": {
        "admin": {
            "name": "Giám Đốc (Admin)",
            "password": hashed_passwords[0]
        },
        "ketoan": {
            "name": "Kế Toán Viên",
            "password": hashed_passwords[1]
        }
    }
}

# Khởi tạo Authenticator
authenticator = stauth.Authenticate(
    credentials,
    "wood_erp_cookie_v3",   # Tên cookie mới để tránh xung đột cũ
    "key_secure_999", 
    cookie_expiry_days=30
)

# 3. HIỂN THỊ FORM ĐĂNG NHẬP
# Ở phiên bản 0.3.2, hàm login không trả về giá trị, nó lưu thẳng vào session_state
authenticator.login(location='main')

# 4. KIỂM TRA VÀ HIỂN THỊ NỘI DUNG
if st.session_state["authentication_status"]:
    # --- ĐĂNG NHẬP THÀNH CÔNG ---
    authenticator.logout('Đăng xuất', 'sidebar')
    
    st.sidebar.success(f"Chào mừng {st.session_state['name']}")
    menu = st.sidebar.selectbox("Lựa chọn báo cáo:", 
                               ["Dashboard Tổng Quan", "Báo Cáo Tài Chính", "Theo Dõi Sản Xuất"])

    if menu == "Dashboard Tổng Quan":
        st.title("📊 Dashboard Quản Trị Nhà Máy")
        c1, c2, c3 = st.columns(3)
        c1.metric("Doanh thu", "5.2 Tỷ", "+10%")
        c2.metric("Lợi nhuận", "1.8 Tỷ", "+5%")
        c3.metric("Yield (Hao hụt)", "68.5%", "Đạt")
        
        # Biểu đồ mẫu
        df = pd.DataFrame({'Tháng': ['T5', 'T6', 'T7'], 'Doanh thu': [4.8, 5.0, 5.2]})
        st.plotly_chart(px.bar(df, x='Tháng', y='Doanh thu', title="Doanh thu theo tháng"), use_container_width=True)

    elif menu == "Báo Cáo Tài Chính":
        st.title("📋 Báo Cáo P&L Chi Tiết")
        st.table(pd.DataFrame({
            "Chỉ tiêu": ["Doanh thu", "Giá vốn", "Lợi nhuận gộp"],
            "Giá trị": ["5.200.000.000", "3.400.000.000", "1.800.000.000"]
        }))

    elif menu == "Theo Dõi Sản Xuất":
        st.title("🪵 Quản lý Lô Gỗ & Yield")
        st.info("Dữ liệu xẻ gỗ thực tế từ các phân xưởng...")

elif st.session_state["authentication_status"] is False:
    st.error('Sai tài khoản hoặc mật khẩu. Vui lòng thử lại.')
    st.info('Gợi ý: admin / 123')

elif st.session_state["authentication_status"] is None:
    # --- TRẠNG THÁI CHỜ ĐĂNG NHẬP ---
    # Ẩn sidebar hoàn toàn
    st.markdown("""<style>[data-testid="stSidebar"] {display: none;}</style>""", unsafe_allow_html=True)
    
    st.markdown("<h1 style='text-align: center; color: #2E7D32;'>🌲 WOOD-TECH ERP SYSTEM</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Hệ thống quản trị nội bộ dành cho ngành chế biến gỗ</p>", unsafe_allow_html=True)
    st.divider()
