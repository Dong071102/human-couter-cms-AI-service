# Human Counter CMS

**Human Counter CMS** là một dịch vụ sử dụng mô hình YOLO và OpenCV để đếm số lượng người trong thời gian thực từ camera IP hoặc video file. Hệ thống được triển khai thông qua WebSocket server và có thể chụp ảnh bằng yêu cầu từ client.

---

## 📦 Yêu cầu hệ thống

- Python 3.11
- pip ≥ 21
- CUDA 12 (nếu dùng GPU)
- Hệ điều hành: Linux / Windows

---

## 🚀 Cài đặt

1. **Clone project:**

```bash
git clone https://github.com/yourusername/human-couter-services.git
cd human-couter-services
```
2. **Install packages and dependency**

```bash
pip install .
```
3. **Run project**

```bash
python main.py
```