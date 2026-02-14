from fastapi import FastAPI, Request
from ultralytics import YOLO
import numpy as np
import cv2
import os
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, db, storage


FIRE_THRESHOLD = 0.6
# Firebase init
cred = credentials.Certificate("./serviceAccountKey.json") 
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://robloxshop-c65a7.firebaseio.com/',
    'storageBucket': 'robloxshop-c65a7.firebasestorage.app'  
})

bucket = storage.bucket()
model = YOLO("best.pt")
app = FastAPI()


@app.post("/detect")
async def detect(request: Request):

    device_id = request.query_params.get("device_id", "unknown")

    body = await request.body()
    nparr = np.frombuffer(body, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        return {"error": "Invalid image data"}

    results = model.predict(img, imgsz=416, conf=FIRE_THRESHOLD, verbose=False)

    detected = 0

    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])

            if model.names[cls] == "fire" and conf >= FIRE_THRESHOLD:
                detected = 1
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

    # Update Firebase
    ref = db.reference(f"fire_detection/{device_id}")
    ref.set({
        "result": detected,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    # Nếu có cháy lưu ảnh
    if detected == 1:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        local_dir = f"snapshots/{device_id}"
        os.makedirs(local_dir, exist_ok=True)

        filename = f"{local_dir}/{timestamp}.jpg"
        cv2.imwrite(filename, img)

        blob = bucket.blob(f"fire_snapshots/{device_id}/{timestamp}.jpg")
        blob.upload_from_filename(filename)

        print(f" Fire detected from {device_id}")

    return {
        "device_id": device_id,
        "fire": detected
    }