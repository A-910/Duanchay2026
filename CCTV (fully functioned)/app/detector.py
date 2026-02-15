from ultralytics import YOLO
import cv2
from datetime import datetime
from app.firebase_service import bucket
from app.config import MODEL_PATH, FIRE_THRESHOLD

model = YOLO(MODEL_PATH)
CONF_THRESHOLD = 0.5
def detect_fire(img, device_id):

    results = model.predict(
        img,
        imgsz=416,
        conf=0.01,   # để thấp, mình tự lọc bằng FIRE_THRESHOLD
        verbose=False
    )

    fire_detected = 0  # mặc định không cháy

    for r in results:
        if r.boxes is not None:
            for box in r.boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                class_name = model.names[cls_id]

                if class_name.lower() == "Cháy" and conf >= CONF_THRESHOLD:
                    fire_detected = 1  # ✅ QUAN TRỌNG

                    x1, y1, x2, y2 = map(int, box.xyxy[0])

                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    label = f"Cháy {conf:.2f}"
                    cv2.putText(
                        img,
                        label,
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (0, 0, 255),
                        2
                    )

    # Encode ảnh sau khi vẽ
    _, buffer = cv2.imencode(".jpg", img)
    image_bytes = buffer.tobytes()

    # Luôn lưu latest.jpg
    latest_blob = bucket.blob(f"{device_id}/latest.jpg")
    latest_blob.upload_from_string(image_bytes, content_type="image/jpeg")

    # 🔥 Nếu có cháy thì lưu ảnh timestamp
    if fire_detected == 1:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        fire_blob = bucket.blob(f"{device_id}/fire_{timestamp}.jpg")
        fire_blob.upload_from_string(image_bytes, content_type="image/jpeg")

    return fire_detected, img
