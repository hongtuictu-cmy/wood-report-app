import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. CẤU HÌNH HỆ THỐNG
st.set_page_config(page_title="Hệ Thống Quản Trị Tài Chính Wood-ERP", layout="wide")

# Tạo CSS tùy chỉnh để giao diện chuyên nghiệp hơn
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

# 3. CHỨC NĂNG UPLOAD (Để biến App thành công cụ thực tế)
st.sidebar.markdown("---")
uploaded_file = st.sidebar.file_upload("Nạp dữ liệu kế toán (Excel/CSV)", type=['xlsx', 'csv'])

# 4. NỘI DUNG CÁC PHÂN HỆ
if menu == "Tổng quan (CEO Dashboard)":
    st.header("📊 Báo Cáo Sức Khỏe Doanh Nghiệp")
    
    # Chỉ số tài chính nhanh
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Doanh thu thuần", "5.2 Tỷ", "+15%")
    col2.metric("Lợi nhuận gộp", "1.8 Tỷ", "34.6%", delta_color="normal")
    col3.metric("Tồn kho", "12.4 Tỷ", "Cảnh báo cao", delta_color="inverse")
    col4.metric("Dòng tiền thuần", "850 Tr", "-5%")

    # Biểu đồ doanh thu vs Chi phí
    st.subheader("Biến động Doanh thu & Lợi nhuận (6 tháng)")
    chart_data = pd.DataFrame({
        'Tháng': ['T2', 'T3', 'T4', 'T5', 'T6', 'T7'],
        'Doanh thu': [4.1, 4.5, 3.8, 5.0, 4.8, 5.2],
        'Lợi nhuận': [1.2, 1.4, 0.9, 1.7, 1.5, 1.8]
    })
    fig = px.line(chart_data, x='Tháng', y=['Doanh thu', 'Lợi nhuận'], markers=True, template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

elif menu == "Phân tích Giá thành & Yield":
    st.header("🪵 Phân tích Giá thành Sản xuất & Tỷ lệ Thu hồi")
    
    c1, c2 = st.columns([1, 2])
    with c1:
        st.write("### Cấu thành giá vốn (COGS)")
        pie_data = pd.DataFrame({
            "Hạng mục": ["Gỗ nguyên liệu", "Nhân công", "Điện năng", "Hao mòn máy", "Keo/Sơn"],
            "Giá trị": [65, 15, 8, 5, 7]
        })
        fig_pie = px.pie(pie_data, values="Giá trị", names="Hạng mục", hole=0.5)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with c2:
        st.write("### Tỷ lệ thu hồi gỗ (Yield) theo lô hàng")
        # Giả lập dữ liệu Yield
        yield_data = pd.DataFrame({
            "Mã lô": ["LOT-001", "LOT-002", "LOT-003", "LOT-004"],
            "Gỗ tròn (m3)": [100, 150, 120, 200],
            "Phôi đạt (m3)": [65, 105, 78, 140],
            "Tỷ lệ %": [65, 70, 65, 70]
        })
        st.dataframe(yield_data, use_container_width=True)
        st.info("💡 Lời khuyên: Lô LOT-001 có tỷ lệ thu hồi thấp dưới mức 68%, cần kiểm tra chất lượng gỗ đầu vào hoặc quy trình xẻ.")

elif menu == "Báo cáo P&L chi tiết":
    st.header("📋 Báo cáo Kết quả Kinh doanh (P&L)")
    # Mô phỏng bảng tài chính chuyên nghiệp
    pl_table = pd.DataFrame({
        "Chỉ tiêu": ["1. Doanh thu bán hàng", "2. Các khoản giảm trừ", "3. Doanh thu thuần", "4. Giá vốn hàng bán", "5. Lợi nhuận gộp", "6. Chi phí bán hàng", "7. Chi phí quản lý", "8. Lợi nhuận thuần"],
        "Tháng này (VNĐ)": ["5,200,000,000", "0", "5,200,000,000", "3,400,000,000", "1,800,000,000", "250,000,000", "400,000,000", "1,150,000,000"],
        "% Doanh thu": ["100%", "0%", "100%", "65.4%", "34.6%", "4.8%", "7.7%", "22.1%"]
    })
    st.table(pl_table)

# 5. THÔNG BÁO HỆ THỐNG
st.sidebar.success("Trạng thái: Máy chủ đang kết nối")
