# 👀 Human Counter CMS

Human Counter CMS là một dịch vụ nhẹ sử dụng AI, tận dụng mô hình phát hiện đối tượng YOLO và OpenCV để đếm số lượng người trong luồng video hoặc từ camera IP. Dịch vụ cung cấp API WebSocket để cập nhật dữ liệu theo thời gian thực và hỗ trợ lấy ảnh chụp từ phía client.

## 🛠️ Tính năng

- Đếm người theo thời gian thực từ camera IP hoặc video
- Phát hiện bằng AI sử dụng YOLO và OpenCV
- Máy chủ WebSocket cung cấp dữ liệu đếm trực tiếp
- Endpoint để chụp và trả về khung hình hiện tại
- Chạy được trên cả Linux và Windows

## 📐 Kiến trúc hệ thống

```text
┌────────────────┐   khung hình   ┌───────────────┐   đếm/ảnh chụp    ┌──────────────────┐
│ Camera IP hoặc │ ─────────────▶│ Dịch vụ phát  │ ─────────────────▶│ Máy chủ WebSocket │
│ File video     │               │ hiện (YOLO +  │                   │ (FastAPI + WS)    │
│                │               │ OpenCV)       │                   └──────────────────┘
└────────────────┘               └───────────────┘
```

## 📋 Yêu cầu hệ thống

- Python 3.11+
- pip 21+  
- CUDA 12+ (tùy chọn, cần nếu muốn tăng tốc bằng GPU)
- Hệ điều hành: Linux hoặc Windows

## 🚀 Cài đặt

1. **Clone repository**
   ```bash
   git clone https://github.com/Dong071102/human-couter-cms-AI-service.git
   cd human-couter-cms-AI-service
   ```

2. **Cài đặt thư viện phụ thuộc**
   ```bash
   pip install -r requirements.txt
   ```

3. **Chạy dịch vụ**
   ```bash
   python main.py
   ```

## ⚙️ Cấu hình

- **Nguồn camera**: chỉnh sửa `main.py` hoặc sử dụng biến môi trường để trỏ tới URL của camera IP hoặc đường dẫn video.
- **Thiết lập mô hình**: chỉnh sửa `src/detector.py` để thay đổi trọng số YOLO hoặc điều chỉnh ngưỡng phát hiện.
- **Cổng WebSocket**: mặc định là `8000`, có thể thay đổi trong `main.py`.

## 📡 Cách sử dụng

1. **Kết nối tới WebSocket**
   ```js
   const socket = new WebSocket('ws://localhost:8000/ws/count');
   socket.onmessage = (event) => {
     const data = JSON.parse(event.data);
     console.log('Số người hiện tại:', data.count);
   };
   ```

2. **Yêu cầu lấy ảnh chụp**
   ```http
   GET http://localhost:8000/snapshot
   ```
   - Trả về khung hình mới nhất dưới dạng ảnh JPEG.

## 🤝 Đóng góp

Chào mừng mọi đóng góp! Hãy mở issue hoặc pull request nếu bạn có ý tưởng cải tiến, sửa lỗi hoặc thêm tính năng mới.

## 📄 Giấy phép

Dự án này được phát hành theo giấy phép MIT. Xem chi tiết trong tập tin [LICENSE](LICENSE).
