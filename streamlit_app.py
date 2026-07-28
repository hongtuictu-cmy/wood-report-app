import streamlit as st
import pandas as pd
import plotly.express as px

# Cấu hình
st.set_page_config(page_title="Wood Management", layout="wide")

st.title("🌲 Hệ Thống Quản Trị Ngành Gỗ")

# Chỉ số nhanh
c1, c2, c3 = st.columns(3)
c1.metric("Doanh thu tháng", "2.5 Tỷ", "+10%")
c2.metric("Tỷ lệ thu hồi (Yield)", "68%", "Tốt")
c3.metric("Đơn hàng chờ", "15 PO", "-2")

# Dữ liệu mẫu
df = pd.DataFrame({
    "Giai đoạn": ["Xẻ", "Sấy", "Tinh chế", "Đóng gói"],
    "Khối lượng (m3)": [1200, 850, 600, 580]
})

st.subheader("Biểu đồ dòng chảy sản xuất")
fig = px.bar(df, x="Giai đoạn", y="Khối lượng (m3)", color="Giai đoạn")
st.plotly_chart(fig, use_container_width=True)

st.info("Hệ thống đang hoạt động bình thường.")
