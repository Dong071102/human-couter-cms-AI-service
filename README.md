# Human Counter CMS

**Human Counter CMS** là một dịch vụ sử dụng mô hình YOLO và OpenCV để đếm số lượng người trong thời gian thực từ camera IP hoặc video file. Hệ thống được triển khai thông qua WebSocket server và có thể chụp ảnh bằng yêu cầu từ client.

# Writing README content to a markdown file for download
readme_content = """# Human Counter CMS

Human Counter CMS is a lightweight AI-powered service that leverages the YOLO object detection model and OpenCV to count people in video streams or IP camera feeds. The service exposes a WebSocket API for real-time updates and supports snapshot requests from clients.

## 🛠️ Features

- Real-time human counting from IP cameras or video files
- AI-driven detection using YOLO and OpenCV
- WebSocket server for live count updates
- Snapshot endpoint to capture and retrieve current frames
- Cross-platform: runs on both Linux and Windows

## 📐 Architecture

```text
┌────────────────┐   frames   ┌───────────────┐   counts/snapshots   ┌──────────────────┐
│ IP Camera or   │ ─────────▶│ Detection     │ ───────────────────▶│ WebSocket Server  │
│ Video File     │           │ Service (YOLO│                     │ (FastAPI + WS)    │
│                │           │ + OpenCV)     │                     └──────────────────┘
└────────────────┘           └───────────────┘
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
