from flask import Flask, request, jsonify
import cv2
import numpy as np

app = Flask(__name__)

def detect_fire(image):
    # Convert to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Range màu lửa (đỏ cam vàng)
    lower = np.array([0, 50, 50])
    upper = np.array([35, 255, 255])

    mask = cv2.inRange(hsv, lower, upper)
    fire_ratio = np.sum(mask > 0) / mask.size

    if fire_ratio > 0.05:
        return "FIRE"
    return "NORMAL"

@app.route('/predict', methods=['POST'])
def predict():
    file = request.data
    npimg = np.frombuffer(file, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    result = detect_fire(img)

    return jsonify({
        "status": result
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
