from flask import Flask, request, jsonify
from ultralytics import YOLO
import numpy as np
import cv2

app = Flask(__name__)

# Load model (có thể thay bằng model fire custom)
model = YOLO("yolov8n.pt")

def detect_fire(image):
    results = model(image)

    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])

            # Nếu detect smoke hoặc fire class custom
            if conf > 0.5:
                return "FIRE"

    return "NORMAL"

@app.route('/predict', methods=['POST'])
def predict():
    file = request.data
    npimg = np.frombuffer(file, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    status = detect_fire(img)

    return jsonify({"status": status})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
