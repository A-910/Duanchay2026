from fastapi import FastAPI, Request
import numpy as np
import cv2
import os
from datetime import datetime

from app.detector import detect_fire
from app.firebase_service import update_status

app = FastAPI()

@app.post("/detect")
async def detect(request: Request):

    device_id = request.query_params.get("device_id", "unknown")

    try:
        body = await request.body()

        if not body:
            return {"status": "no_image"}

        nparr = np.frombuffer(body, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            return {"status": "decode_failed"}

        detected, img = detect_fire(img, device_id)

        # Update Firebase
        update_status(device_id, detected)

        # Save snapshot if fire
        if detected == 1:

            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            save_dir = f"snapshots/{device_id}"
            os.makedirs(save_dir, exist_ok=True)

            filename = f"{save_dir}/{timestamp}.jpg"
            cv2.imwrite(filename, img)

            print(f"[ FIRE DETECTED] {device_id}")

        return {
            "device_id": device_id,
            "fire": detected,
            "status": "ok"
        }

    except Exception as e:
        print(f"[ERROR] {e}")
        return {"status": "error"}
