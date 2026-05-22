import streamlit as st
from streamlit_calendar import calendar
import json
import os

# 1. Cấu hình trang
st.set_page_config(page_title="Lịch Công Việc", page_icon="📅", layout="wide")

# 2. BỘ CSS FIX LỖI GIAO DIỆN TOÀN DIỆN (CẢ PC VÀ MOBILE)
st.markdown("""
    <style>
    /* Khoảng cách viền trang tổng thể */
    .block-container {
        padding: 1rem !important;
    }
    
    /* FIX LỖI PC: Đảm bảo lịch luôn hiển thị, không bị che mất, thu gọn vừa vặn */
    .fc {
        max-width: 95% !important;
        margin: 0 auto 20px auto !important;
        background-color: #1e1e1e !important; /* Ép lịch luôn ở giao diện tối sang trọng */
        color: #ffffff !important;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #333333;
    }
    
    /* Sửa thuộc tính scroller để biến mất thanh cuộn dọc nhưng KHÔNG nuốt mất lịch */
    .fc-scroller {
        overflow: visible !important;
        height: auto !important;
    }
    .fc-scroller-harness {
        overflow: visible !important;
        height: auto !important;
    }

    /* Định dạng màu chữ ngày tháng và đường kẻ */
    .fc a { color: #ffffff !important; text-decoration: none !important; }
    .fc-theme-standard td, .fc-theme-standard th { border: 1px solid #444444 !important; }
    .fc-col-header-cell-cushion { padding: 8px 0 !important; }

    /* --- FIX LỖI MOBILE (Dưới 768px): Sắp xếp các nút điều hướng cực đẹp --- */
    @media (max-width: 768px) {
        .fc {
            padding: 8px !important;
            font-size: 11px !important;
        }
        /* Tổ chức lại thanh công cụ của lịch */
        .fc .fc-toolbar {
            display: grid !important;
            grid-template-columns: 1fr !important; /* Xếp thành các hàng dọc độc lập */
            gap: 10px !important;
            justify-items: center !important;
            text-align: center !important;
        }
        /* Căn chỉnh lại cụm nút điều hướng (Trái, Giữa, Phải) */
        .fc-header-toolbar .fc-toolbar-chunk {
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
            gap: 4px !important;
            width: 100% !important;
        }
        /* Thu nhỏ tiêu đề Tháng / Năm để không bị đẩy dòng */
        .fc .fc-toolbar-title {
            font-size: 1.2rem !important;
            font-weight: bold !important;
            color: #00F29D !important; /* Làm nổi bật tiêu đề tháng */
        }
        /* Tối ưu hóa kích cỡ các nút bấm vừa vặn ngón tay trên điện thoại */
        .fc .fc-button {
            padding: 6px 10px !important;
            font-size: 11px !important;
            line-height: 1 !important;
            margin: 0 2px !important;
            background-color: #333333 !important;
            border-color: #444444 !important;
            color: #ffffff !important;
        }
        .fc .fc-button-active {
            background-color: #00F29D !important; /* Màu xanh khi đang được chọn */
            color: #000000 !important;
        }
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

# --- CHUYỂN ĐỔI TAB GIAO DIỆN CHỐNG TRÀN ---
tab_them, tab_lich = st.tabs(["➕ Thêm & Quản lý", "🗓️ Xem Lịch Trình"])

with tab_them:
    st.subheader("Thêm Công Việc Mới")
    with st.form("event_form", clear_on_submit=True):
        title = st.text_input("Tên công việc:", placeholder="Ví dụ: Đi chụp hình, Họp nhóm...")
        
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            start_date = st.date_input("Từ ngày:")
        with col_d2:
            end_date = st.date_input("Đến ngày:")
            
        color = st.color_picker("Chọn màu hiển thị:", "#FF4B4B")
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
        "height": "auto", 
    }
    
    # Render component lịch
    calendar(events=st.session_state.events, options=calendar_options, key="calendar_perfect")

# --- THÔNG TIN BẢN QUYỀN CỐ ĐỊNH GÓC DƯỚI TRÁI ---
st.markdown(
    """
    <style>
    .copyright-footer {
        position: fixed;
        bottom: 5px;
        left: 5px;
        background-color: rgba(0, 0, 0, 0.8);
        color: #ffffff;
        padding: 4px 10px;
        border-radius: 4px;
        font-size: 10px;
        z-index: 9999;
        pointer-events: none;
    }
    </style>
    <div class="copyright-footer">© 2026 Powered by Thinh</div>
    """,
    unsafe_allow_html=True
)
