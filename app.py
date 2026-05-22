import streamlit as st
from streamlit_calendar import calendar
import json
import os

# 1. Cấu hình trang
st.set_page_config(page_title="Lịch Công Việc", page_icon="📅", layout="wide")

# 2. CSS TỐI ƯU TOÀN DIỆN (Sửa lỗi máy tính & điện thoại)
st.markdown("""
    <style>
    /* Loại bỏ khoảng trống thừa của Streamlit */
    .block-container {
        padding: 1rem !important;
    }
    
    /* 1. SỬA LỖI TRÊN MÁY TÍNH: Mất cột cuộn dọc thừa và làm lịch gọn lại */
    .fc {
        max-width: 95% !important; /* Nhỏ lại 1 xíu so với màn hình */
        margin: 0 auto !important; /* Căn giữa lịch */
        background-color: #1e1e1e !important;
        padding: 15px;
        border-radius: 8px;
    }
    /* Khóa chiều cao cố định để không sinh ra thanh cuộn dọc (scrollbar) bên trong lịch */
    .fc-scroller {
        overflow: hidden !important; 
        height: auto !important;
    }
    .fc-scroller-harness {
        height: auto !important;
    }

    /* 2. SỬA LỖI TRÊN ĐIỆN THOẠI: Sắp xếp các nút mũi tên, today, month, day không bị đè nhau */
    @media (max-width: 768px) {
        .fc .fc-toolbar {
            display: flex !important;
            flex-direction: column !important; /* Xếp thành các dòng dọc */
            gap: 8px !important;
            align-items: center !important;
        }
        .fc .fc-toolbar-title {
            font-size: 1.2rem !important; /* Thu nhỏ tiêu đề tháng/năm */
            margin: 4px 0;
        }
        .fc .fc-button {
            padding: 4px 8px !important; /* Thu nhỏ kích thước nút */
            font-size: 11px !important;
        }
        .fc-header-toolbar .fc-toolbar-chunk {
            display: flex !important;
            justify-content: center !important;
            width: 100% !important;
        }
    }

    /* Màu chữ hiển thị ngày tháng */
    .fc a { color: #ffffff !important; }
    .fc-theme-standard td, .fc-theme-standard th { border: 1px solid #444444 !important; }
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

# --- CHIA TAB GIAO DIỆN ---
tab_them, tab_lich = st.tabs(["➕ Thêm & Quản lý", "🗓️ Xem Lịch Trình"])

with tab_them:
    st.subheader("Thêm Công Việc Mới")
    with st.form("event_form", clear_on_submit=True):
        title = st.text_input("Tên công việc:", placeholder="Ví dụ: Họp nhóm...")
        
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            start_date = st.date_input("Từ ngày:")
        with col_d2:
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
            st.success("Đã thêm công việc thành công!")
            st.rerun()

    st.subheader("🗑️ Danh sách đã thêm")
    if st.session_state.events:
        for idx, ev in enumerate(st.session_state.events):
            col_t, col_b = st.columns([4, 1])
            col_t.write(f"🎨 **{ev['title']}** ({ev['start']} đến {ev['end']})")
            if col_b.button("Xóa", key=f"del_{idx}"):
                st.session_state.events.pop(idx)
                save_data(st.session_state.events)
                st.rerun()
    else:
        st.caption("Chưa có công việc nào.")

with tab_lich:
    st.subheader("Lịch Trình Chi Tiết")
    
    calendar_options = {
        "editable": True,
        "selectable": True,
        "headerToolbar": {
            "left": "prev,next today",
            "center": "title",
            "right": "dayGridMonth,timeGridDay",
        },
        "initialView": "dayGridMonth",
        "height": "auto", # Ép lịch tự động tính chiều cao theo ô thay vì sinh thanh cuộn
    }
    
    calendar(events=st.session_state.events, options=calendar_options, key="calendar_final")

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
