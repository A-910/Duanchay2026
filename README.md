+ ESPCAM:
    - Giữ /stream để xem trực tiếp. (bị CANCEL do việc không cùng mạng LAN) \
    -> Giải quyết vấn đề không cùng mạng = cách post thẳng lên server VM. (test thì lấy IP: <localhost:ip>)

+ NODE RED:
    - Add flow xem ảnh cháy từ snapshot fire_result/. (link storage của firebase bucket qua) <- (Việc cần làm)
    - UI stream các ảnh post qua mỗi 5s theo từng luồng. (cấu trúc lại chức năng không còn là stream) <- (Việc cần làm)    
    ! LƯU Ý KHÔNG LƯU VỀ LOCAL!!!
+ Cân nhắc: không sử dụng stream thẳng từ cam lên Server hay UI của Node Red được vì:
    - Khác mạng và việc sử dụng NAT sẽ dễ lỗi stream do firewal và tái kết nôi dẽ lỗi, ESP32 không đủ điều kiện dùng giao thức webRTC hay RTSP.
    - Giới hạn cấu trúc và cấu hình để stream liên tục.
    - [Dự kiến] Thêm postgreSQL làm thành ứng dụng thương mại. (trên Node Red maybe?)

+ LOGIC giải quyết bài toán:
    - CAM (post ảnh lên VM) -> Server (xử lý-DB & storage firebase) -> Node red (UI stream các ảnh đưọc post về).

+ Sơ đồ hoạt động:
                 ┌────────────────────┐
                 │     ESP32-CAM      │
                 │  - Chụp ảnh 1s/lần │
                 │  - POST /detect    │
                 └─────────┬──────────┘
                           │ JPEG
                           ▼
                 ┌────────────────────┐
                 │     Node-RED       │
                 │  HTTP In (/detect) │
                 │  - Nhận ảnh        │
                 │  - Gửi AI server   │
                 │  - Lưu file        │
                 │  - Lưu database    │
                 └─────────┬──────────┘
                           │ JSON status
                           ▼
                 ┌────────────────────┐
                 │   Python AI YOLO   │
                 │  - best.pt model   │
                 │  - Detect FIRE     │
                 └─────────┬──────────┘
                           │ status
                           ▼
                 ┌────────────────────┐
                 │    Dashboard UI    │
                 │  - Ảnh mới nhất    │
                 │  - Status          │
                 │  - Gauge           │
                 │  - Lịch sử         │
                 └────────────────────┘
