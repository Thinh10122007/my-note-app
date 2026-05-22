import streamlit as st
from streamlit_calendar import calendar
import json
import os

st.set_page_config(page_title="Lịch Công Việc", page_icon="📅", layout="wide")

st.title("📅 Lịch Trình & Công Việc")

# Đường dẫn đến file lưu dữ liệu
DATA_FILE = "data.json"

# --- HÀM ĐỌC VÀ GHI DATA TỪ FILE ---
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Khởi tạo danh sách công việc từ file vào Session State khi chạy app lần đầu
if "events" not in st.session_state:
    st.session_state.events = load_data()

# --- GIAO DIỆN APP ---
col_input, col_calendar = st.columns([1, 2])

with col_input:
    st.subheader("➕ Thêm Công Việc")
    with st.form("event_form", clear_on_submit=True):
        title = st.text_input("Tên công việc:", placeholder="Ví dụ: Họp nhóm, Đi chợ...")
        
        col_date1, col_date2 = st.columns(2)
        with col_date1:
            start_date = st.date_input("Từ ngày:")
        with col_date2:
            end_date = st.date_input("Đến ngày:")
            
        color = st.color_picker("Chọn màu hiển thị trên lịch:", "#00F29D")
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
            # Thêm vào bộ nhớ tạm
            st.session_state.events.append(new_event)
            # Lưu ngay vào file data.json
            save_data(st.session_state.events)
            st.success("Đã thêm và lưu vào file!")
            st.rerun()

    st.subheader("🗑️ Quản lý danh sách")
    if st.session_state.events:
        for idx, ev in enumerate(st.session_state.events):
            col_t, col_b = st.columns([3, 1])
            col_t.write(f"🎨 {ev['title']} ({ev['start']})")
            if col_b.button("Xóa", key=f"del_{idx}"):
                st.session_state.events.pop(idx)
                # Cập nhật lại file data.json sau khi xóa
                save_data(st.session_state.events)
                st.rerun()
    else:
        st.caption("Chưa có công việc nào.")

with col_calendar:
    st.subheader("🗓️ Lịch Trình Của Bạn")
    calendar_options = {
        "editable": True,
        "selectable": True,
        "headerToolbar": {
            "left": "today prev,next",
            "center": "title",
            "right": "dayGridMonth,dayGridWeek,timeGridDay",
        },
        "initialView": "dayGridMonth",
    }
    
    calendar(events=st.session_state.events, options=calendar_options, key="calendar_component")

# --- THÔNG TIN BẢN QUYỀN Ở GÓC DƯỚI TRÁI ---
st.markdown(
    """
    <style>
    .copyright-footer {
        position: fixed;
        bottom: 10px;
        left: 10px;
        background-color: rgba(0, 0, 0, 0.6);
        color: #ffffff;
        padding: 5px 10px;
        border-radius: 5px;
        font-size: 12px;
        font-family: Arial, sans-serif;
        z-index: 9999;
        pointer-events: none;
    }
    </style>
    <div class="copyright-footer">
        © 2026 Powered by Thinh
    </div>
    """,
    unsafe_allow_html=True
)
