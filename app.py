import streamlit as st
from streamlit_calendar import calendar
import json
import os

# Cấu hình trang - Bắt buộc phải có để tối ưu giao diện màn hình
st.set_page_config(page_title="Lịch Công Việc Mobile", page_icon="📅", layout="wide")

# CSS tối ưu riêng cho giao diện điện thoại (Ẩn các khoảng trống thừa, fix tràn lịch)
st.markdown("""
    <style>
    /* Giảm khoảng cách viền trên điện thoại */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
    /* Ép lịch không được tràn quá màn hình dọc */
    .fc {
        max-width: 100% !important;
        font-size: 12px !important; /* Thu nhỏ chữ trên lịch một chút để vừa màn hình đt */
    }
    .fc .fc-toolbar {
        flex-direction: column !important;
        gap: 5px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📅 Lịch Trình Cá Nhân")

DATA_FILE = "data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            try: return json.load(f)
            except: return []
    return []

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if "events" not in st.session_state:
    st.session_state.events = load_data()

# --- GIẢI PHÁP FIX LỖI ĐIỆN THOẠI: Dùng tab thay vì chia cột ngang ---
# Trên máy tính sẽ nhìn thấy 2 Tab, trên điện thoại các tab này bấm chuyển đổi cực kỳ mượt mà không bị tràn màn hình.
tab_them, tab_lich = st.tabs(["➕ Thêm & Quản lý", "🗓️ Xem Lịch Trình"])

with tab_them:
    st.subheader("Thêm Công Việc Mới")
    with st.form("event_form", clear_on_submit=True):
        title = st.text_input("Tên công việc:", placeholder="Ví dụ: Họp nhóm, Đi chợ...")
        
        # Chia cột nhỏ cho ngày (chỉ chia 2 cột nên điện thoại vẫn hiển thị tốt)
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            start_date = st.date_input("Từ ngày:")
        with col_date2 if 'col_date2' in locals() else col_d2:
            end_date = st.date_input("Đến ngày:")
            
        color = st.color_picker("Chọn màu hiển thị:", "#00F29D")
        submit = st.form_submit_button("Thêm vào lịch")
        
        if submit and title:
            new_event = {
                "title": title,
                "start": start_date.strftime("%Y-%m-%d"),
                "end": end_date.strftime("%Y-%m-%d"),
                "backgroundColor": color,
                "borderColor": color,
                "textColor": "#FFFFFF"
            }
            st.session_state.events.append(new_event)
            save_data(st.session_state.events)
            st.success("Đã thêm thành công!")
            st.rerun()

    st.subheader("🗑️ Danh sách đã thêm")
    if st.session_state.events:
        for idx, ev in enumerate(st.session_state.events):
            col_t, col_b = st.columns([4, 1])
            col_t.write(f"🎨 {ev['title']} ({ev['start']})")
            if col_b.button("Xóa", key=f"del_{idx}"):
                st.session_state.events.pop(idx)
                save_data(st.session_state.events)
                st.rerun()
    else:
        st.caption("Chưa có công việc nào.")

with tab_lich:
    st.subheader("Lịch Trình")
    
    # Cấu hình lịch thông minh: Mặc định xem theo Tháng, nhưng rút gọn các nút trên điện thoại
    calendar_options = {
        "editable": True,
        "selectable": True,
        "headerToolbar": {
            "left": "prev,next today",
            "center": "title",
            "right": "dayGridMonth,timeGridDay", # Chỉ để lại chế độ Tháng và Ngày cho gọn
        },
        "initialView": "dayGridMonth",
    }
    
    calendar(events=st.session_state.events, options=calendar_options, key="calendar_mobile")

# --- THÔNG TIN BẢN QUYỀN Ở GÓC DƯỚI TRÁI ---
st.markdown(
    """
    <style>
    .copyright-footer {
        position: fixed;
        bottom: 5px;
        left: 5px;
        background-color: rgba(0, 0, 0, 0.7);
        color: #ffffff;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 10px;
        z-index: 9999;
        pointer-events: none;
    }
    </style>
    <div class="copyright-footer">© 2026 kendev</div>
    """,
    unsafe_allow_html=True
)
