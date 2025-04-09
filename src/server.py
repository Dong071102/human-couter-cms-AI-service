import asyncio
import json
import os
import cv2
import base64
from datetime import datetime
from websockets.server import serve
import websockets
from ultralytics import YOLO
import numpy as np
import cvzone
from src.DB.database import get_all_camera_ip, insert_snapshot_person

BASE_VIDEO_DIR = 'src/person_couter_image'
model = YOLO("src/models/best.onnx", task='detect')
names = model.names

cameras_info = get_all_camera_ip()
cameras_details = {
    row[3]: {
        "camera_id": row[0],
        "camera_URL": row[1],
        "classroom_id": row[2]
    }
    for row in cameras_info
} if cameras_info else {}

def create_evidence_image_url(schedule_id, camera_id):
    today = datetime.now()
    date_folder = today.strftime("%Y/%m/%d")
    full_folder_path = os.path.join(BASE_VIDEO_DIR, date_folder)
    os.makedirs(full_folder_path, exist_ok=True)
    video_filename = f"{schedule_id}__{camera_id}.jpg"
    return os.path.join(full_folder_path, video_filename)

async def handle_client(websocket, path):
    socket_id = path.split("/human_couter/")[-1]
    camera_info = cameras_details.get(socket_id)

    if not camera_info:
        print(f"Không tìm thấy lớp học {socket_id}")
        await websocket.close()
        return

    camera_id = camera_info["camera_id"]
    camera_URL = camera_info["camera_URL"]
    classroom_id = camera_info["classroom_id"]
    print("📹 Đang stream từ:", camera_URL)

    cap = cv2.VideoCapture('tv3_sau.mp4')  # hoặc camera_URL nếu live
    if not cap.isOpened():
        await websocket.send(json.dumps({
            "type": "error",
            "message": f"Không kết nối được camera: {camera_URL}",
            "timestamp": datetime.now().isoformat()
        }))
        return

    snapshot_requested = False
    schedule_id = None

    try:
        while True:
            for _ in range(3): cap.read()  # bỏ frame để giảm trễ
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.resize(frame, (640, 360))  # giảm kích thước cho nhẹ
            results = model.track(frame, persist=True, classes=0)

            num_people = 0
            if results[0].boxes and results[0].boxes.id is not None:
                track_ids = results[0].boxes.id.int().cpu().tolist()
                num_people = len(set(track_ids))

                cvzone.putTextRect(frame, f'Number of people: {num_people}',
                                   (20, 40), scale=1.5, thickness=2, colorR=(255, 0, 0))

                boxes = results[0].boxes.xyxy.int().cpu().tolist()
                class_ids = results[0].boxes.cls.int().cpu().tolist()
                track_ids = results[0].boxes.id.int().cpu().tolist()

                for box, class_id, track_id in zip(boxes, class_ids, track_ids):
                    x1, y1, x2, y2 = box
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cvzone.putTextRect(frame, f'{track_id}', (x1, y1), scale=1, thickness=1)

            # Nhận yêu cầu từ client
            try:
                msg = await asyncio.wait_for(websocket.recv(), timeout=0.01)
                data = json.loads(msg)
                if data["type"] == "snapshot_request":
                    snapshot_requested = True
                    schedule_id = data.get("schedule_id", None)
            except asyncio.TimeoutError:
                pass
            except Exception as e:
                print("❌ Lỗi nhận message từ client:", e)

            # Lưu snapshot nếu có yêu cầu
            if snapshot_requested:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                snapshot_path = create_evidence_image_url(schedule_id, camera_id)
                cv2.imwrite(snapshot_path, frame)

                insert_snapshot_person(
                    schedule_id=schedule_id,
                    camera_id=camera_id,
                    people_couter=num_people,
                    captured_at=timestamp,
                    image_path=snapshot_path
                )

                _, buffer = cv2.imencode('.jpg', frame)
                img_base64 = base64.b64encode(buffer).decode('utf-8')

                await websocket.send(json.dumps({
                    "type": "snapshot_response",
                    "message": "Snapshot captured successfully",
                    "filename": snapshot_path,
                    "num_people": num_people,
                    "image_base64": img_base64,
                    "timestamp": datetime.now().isoformat()
                }))
                snapshot_requested = False
                schedule_id = None

            # Gửi video frame về client
            _, buffer = cv2.imencode('.jpg', frame)
            jpg_as_text = base64.b64encode(buffer).decode('utf-8')
            await websocket.send(json.dumps({
                "type": "video_frame",
                "frame": jpg_as_text
            }))

            await asyncio.sleep(1/25)

    except websockets.ConnectionClosed:
        print("🔌 Kết nối WebSocket đã đóng")
    except Exception as e:
        print("❌ Lỗi khi stream:", e)
    finally:
        cap.release()
        print("🛑 Đã ngắt stream cho:", socket_id)

async def main():
    HOST = "localhost"
    PORT = 13000
    server = await serve(handle_client, HOST, PORT)
    print(f"🚀 WebSocket server đang chạy tại ws://{HOST}:{PORT}")
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
