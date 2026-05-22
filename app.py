<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lịch Công Việc</title>
    
    <!-- Tải thư viện FullCalendar từ CDN -->
    <script src="https://cdn.jsdelivr.net/npm/fullcalendar@6.1.11/index.global.min.js"></script>
    
    <style>
        /* --- CẤU HÌNH GIAO DIỆN TỔNG THỂ (DARK MODE) --- */
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }

        body {
            background-color: #0f1115;
            color: #ffffff;
            padding: 1rem;
            padding-bottom: 30px;
        }

        h1 {
            text-align: center;
            margin-bottom: 1.5rem;
            font-size: 1.8rem;
        }

        /* --- CẤU HÌNH TABS (GIỐNG STREAMLIT) --- */
        .tabs-container {
            max-width: 1200px;
            margin: 0 auto;
        }

        .tab-headers {
            display: flex;
            border-bottom: 1px solid #333;
            margin-bottom: 1.5rem;
            gap: 10px;
        }

        .tab-button {
            background: none;
            border: none;
            color: #888;
            padding: 10px 20px;
            font-size: 1rem;
            cursor: pointer;
            border-bottom: 2px solid transparent;
            transition: all 0.3s ease;
        }

        .tab-button.active {
            color: #00F29D;
            border-bottom: 2px solid #00F29D;
            font-weight: bold;
        }

        .tab-content {
            display: none;
        }

        .tab-content.active {
            display: block;
        }

        /* --- FORM & QUẢN LÝ CÔNG VIỆC --- */
        .form-section {
            background-color: #1a1d24;
            padding: 1.5rem;
            border-radius: 12px;
            border: 1px solid #333;
            margin-bottom: 2rem;
        }

        .form-group {
            margin-bottom: 1rem;
        }

        .form-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
        }

        label {
            display: block;
            margin-bottom: 5px;
            font-size: 0.9rem;
            color: #aaa;
        }

        input[type="text"], input[type="date"] {
            width: 100%;
            padding: 10px;
            background-color: #262930;
            border: 1px solid #444;
            border-radius: 6px;
            color: #fff;
            font-size: 1rem;
        }

        input[type="color"] {
            width: 60px;
            height: 35px;
            background: none;
            border: none;
            cursor: pointer;
        }

        .btn-submit {
            background-color: #ff4b4b;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 6px;
            font-weight: bold;
            cursor: pointer;
            width: 100%;
            margin-top: 10px;
        }

        /* Danh sách đã thêm */
        .event-list {
            margin-top: 1.5rem;
        }

        .event-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background-color: #1a1d24;
            padding: 12px 15px;
            border-radius: 8px;
            border: 1px solid #333;
            margin-bottom: 8px;
        }

        .btn-delete {
            background-color: transparent;
            color: #ff4b4b;
            border: 1px solid #ff4b4b;
            padding: 5px 12px;
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.2s;
        }

        .btn-delete:hover {
            background-color: #ff4b4b;
            color: white;
        }

        .no-event {
            color: #888;
            font-style: italic;
        }

        /* --- BỘ CSS SANG TRỌNG CHO FULLCALENDAR --- */
        .fc {
            max-width: 100% !important;
            margin: 0 auto !important;
            background-color: #1e1e1e !important;
            color: #ffffff !important;
            padding: 15px;
            border-radius: 12px;
            border: 1px solid #333333;
        }

        /* Ẩn thanh cuộn xấu xí */
        .fc-scroller {
            -ms-overflow-style: none;
            scrollbar-width: none;
        }
        .fc-scroller::-webkit-scrollbar {
            display: none;
        }

        .fc a { color: #ffffff !important; text-decoration: none !important; }
        .fc-theme-standard td, .fc-theme-standard th { border: 1px solid #444444 !important; }
        
        /* Chỉnh màu nút của FullCalendar gốc */
        .fc .fc-button-primary {
            background-color: #333333 !important;
            border-color: #444444 !important;
            color: #ffffff !important;
        }
        .fc .fc-button-primary:not(:disabled).fc-button-active, 
        .fc .fc-button-primary:not(:disabled):active {
            background-color: #00F29D !important;
            color: #000000 !important;
            border-color: #00F29D !important;
        }

        /* --- FIX LỖI MOBILE (DƯỚI 768PX) --- */
        @media (max-width: 768px) {
            .form-row {
                grid-template-columns: 1fr;
                gap: 10px;
            }
            .fc {
                padding: 8px !important;
                font-size: 11px !important;
            }
            .fc .fc-toolbar {
                display: grid !important;
                grid-template-columns: 1fr !important;
                gap: 10px !important;
                justify-items: center !important;
                text-align: center !important;
            }
            .fc-header-toolbar .fc-toolbar-chunk {
                display: flex !important;
                justify-content: center !important;
                align-items: center !important;
                gap: 4px !important;
                width: 100% !important;
            }
            .fc .fc-toolbar-title {
                font-size: 1.2rem !important;
                font-weight: bold !important;
                color: #00F29D !important;
            }
            .fc .fc-button {
                padding: 6px 10px !important;
                font-size: 11px !important;
            }
        }

        /* --- COPYRIGHT FOOTER CỐ ĐỊNH --- */
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
</head>
<body>

    <h1>📅 Lịch Trình Cá Nhân</h1>

    <div class="tabs-container">
        <!-- Thanh điều hướng Tab -->
        <div class="tab-headers">
            <button class="tab-button active" onclick="switchTab('tab-them')">➕ Thêm & Quản lý</button>
            <button class="tab-button" onclick="switchTab('tab-lich')">🗓️ Xem Lịch Trình</button>
        </div>

        <!-- TAB 1: THÊM & QUẢN LÝ -->
        <div id="tab-them" class="tab-content active">
            <div class="form-section">
                <h3 style="margin-bottom:15px;">Thêm Công Việc Mới</h3>
                <form id="eventForm">
                    <div class="form-group">
                        <label>Tên công việc:</label>
                        <input type="text" id="title" placeholder="Ví dụ: Đi chụp hình, Họp nhóm..." required>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label>Từ ngày:</label>
                            <input type="date" id="startDate" required>
                        </div>
                        <div class="form-group">
                            <label>Đến ngày:</label>
                            <input type="date" id="endDate" required>
                        </div>
                    </div>
                    <div class="form-group">
                        <label>Chọn màu hiển thị:</label>
                        <input type="color" id="colorPicker" value="#FF4B4B">
                    </div>
                    <button type="submit" class="btn-submit">Thêm vào lịch</button>
                </form>
            </div>

            <h3>🗑️ Danh sách đã thêm</h3>
            <div id="eventList" class="event-list"></div>
        </div>

        <!-- TAB 2: XEM LỊCH TRÌNH -->
        <div id="tab-lich" class="tab-content">
            <h3 style="margin-bottom:15px;">Lịch Trình Chi Tiết</h3>
            <div id="calendar"></div>
        </div>
    </div>

    <!-- Bản quyền cố định góc dưới trái -->
    <div class="copyright-footer">© 2026 Powered by Thinh</div>

    <script>
        // --- QUẢN LÝ DỮ LIỆU LOCALSTORAGE ---
        let events = JSON.parse(localStorage.getItem('calendar_events')) || [];
        let calendar;

        // Tự động điền ngày hôm nay vào ô input date cho tiện lợi
        const todayStr = new Date().toISOString().split('T')[0];
        document.getElementById('startDate').value = todayStr;
        document.getElementById('endDate').value = todayStr;

        // --- XỬ LÝ CHUYỂN TAB ---
        function switchTab(tabId) {
            document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
            document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
            
            document.getElementById(tabId).classList.add('active');
            event.currentTarget.classList.add('active');

            // Cần cập nhật lại kích thước lịch nếu chuyển sang tab lịch
            if (tabId === 'tab-lich' && calendar) {
                setTimeout(() => {
                    calendar.updateSize();
                }, 50);
            }
        }

        // --- HÀM RENDER DANH SÁCH CÔNG VIỆC ĐÃ THÊM ---
        function renderEventList() {
            const listContainer = document.getElementById('eventList');
            listContainer.innerHTML = '';

            if (events.length === 0) {
                listContainer.innerHTML = '<p class="no-event">Chưa có công việc nào.</p>';
                return;
            }

            events.forEach((ev, idx) => {
                const item = document.createElement('div');
                item.className = 'event-item';
                
                // Chuẩn hóa chuỗi ngày hiển thị (vì FullCalendar tăng ngày kết thúc lên 1, cần giảm lại khi hiển thị text)
                let displayEnd = ev.end;
                if(ev.end !== ev.start) {
                    let d = new Date(ev.end);
                    d.setDate(d.getDate() - 1);
                    displayEnd = d.toISOString().split('T')[0];
                }

                item.innerHTML = `
                    <div>
                        <span style="display:inline-block; width:12px; height:12px; background:${ev.backgroundColor}; border-radius:50%; margin-right:5px;"></span>
                        <strong>${ev.title}</strong> (${ev.start} đến ${displayEnd})
                    </div>
                    <button class="btn-delete" onclick="deleteEvent(${idx})">Xóa</button>
                `;
                listContainer.appendChild(item);
            });
        }

        // --- HÀM XÓA CÔNG VIỆC ---
        function deleteEvent(index) {
            events.splice(index, 1);
            localStorage.setItem('calendar_events', JSON.stringify(events));
            renderEventList();
            if (calendar) {
                calendar.removeAllEvents();
                calendar.addEventSource(events);
            }
        }

        // --- SỰ KIỆN SUBMIT FORM ---
        document.getElementById('eventForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const title = document.getElementById('title').value;
            const start = document.getElementById('startDate').value;
            let end = document.getElementById('endDate').value;
            const color = document.getElementById('colorPicker').value;

            // Mẹo kỹ thuật của FullCalendar: Ngày kết thúc của sự kiện All-Day mang tính loại trừ,
            // nên cần cộng thêm 1 ngày để dải màu hiển thị trọn vẹn trên lịch.
            let endDateObj = new Date(end);
            endDateObj.setDate(endDateObj.getDate() + 1);
            const fullCalendarEnd = endDateObj.toISOString().split('T')[0];

            const newEvent = {
                title: title,
                start: start,
                end: fullCalendarEnd,
                backgroundColor: color,
                borderColor: color,
                textColor: '#FFFFFF',
                allDay: true
            };

            events.push(newEvent);
            localStorage.setItem('calendar_events', JSON.stringify(events));
            
            // Reset form
            document.getElementById('title').value = '';
            document.getElementById('startDate').value = todayStr;
            document.getElementById('endDate').value = todayStr;

            renderEventList();
            
            if (calendar) {
                calendar.removeAllEvents();
                calendar.addEventSource(events);
            }

            alert("Đã thêm công việc thành công!");
        });

        // --- KHỞI TẠO FULLCALENDAR LÀM MƯỢT ---
        document.addEventListener('DOMContentLoaded', function() {
            renderEventList();

            const calendarEl = document.getElementById('calendar');
            calendar = new FullCalendar.Calendar(calendarEl, {
                initialView: 'dayGridMonth',
                height: 'auto',
                editable: true,
                selectable: true,
                headerToolbar: {
                    left: 'prev,next today',
                    center: 'title',
                    right: 'dayGridMonth,timeGridDay'
                },
                events: events,
                locale: 'vi' // Chuyển ngôn ngữ nút bấm tự động nếu thư viện hỗ trợ
            });
            calendar.render();
        });
    </script>
</body>
</html>
