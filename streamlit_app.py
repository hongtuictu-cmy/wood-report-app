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

else:
    st.header("💸 Quản lý Dòng tiền (Cash Flow)")
    st.write("Chức năng đang được cập nhật...")

# 5. THÔNG BÁO HỆ THỐNG
st.sidebar.success("Trạng thái: Máy chủ đã kết nối")
