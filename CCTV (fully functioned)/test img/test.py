import cv2
from ultralytics import YOLO
import os

# ===== CONFIG =====
MODEL_PATH = "best.pt"     # đường dẫn model
CONF_THRESHOLD = 0.5       # threshold confidence
IMAGE_PATH = "fire2.jpg"    # ảnh local để test
CAM_INDEX = 0              # webcam mặc định
VIDEO_PATH = r"C:\Users\trieu\Downloads\CCTV-Docker-20260212T164735Z-1-001\CCTV-Docker\CCTV(fully functioned)\test img\video chay.mp4"

# ===== LOAD MODEL =====
model = YOLO(MODEL_PATH)
print("Classes:", model.names)

# =========================
# ====== TEST IMAGE ======
# =========================
def test_image():

    if not os.path.exists(IMAGE_PATH):
        print("❌ Không tìm thấy ảnh:", IMAGE_PATH)
        return

    img = cv2.imread(IMAGE_PATH)

    results = model.predict(
        img,
        conf=0.01,
        verbose=False
    )

    for r in results:
        if r.boxes is not None:
            for box in r.boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                class_name = model.names[cls_id]

                if class_name.lower() == "fire" and conf >= CONF_THRESHOLD:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])

                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    label = f"fire {conf:.2f}"
                    cv2.putText(
                        img,
                        label,
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (0, 0, 255),
                        2
                    )

    cv2.imshow("Fire Detection - Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# =========================
# ====== TEST CAMERA =====
# =========================
def test_camera():

    cap = cv2.VideoCapture(CAM_INDEX)

    if not cap.isOpened():
        print("❌ Không mở được camera")
        return

    print("🔥 Camera started - Nhấn Q để thoát")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model.predict(
            frame,
            conf=0.01,
            verbose=False
        )

        for r in results:
            if r.boxes is not None:
                for box in r.boxes:
                    cls_id = int(box.cls[0])
                    conf = float(box.conf[0])
                    class_name = model.names[cls_id]

                    if class_name.lower() == "fire" and conf >= CONF_THRESHOLD:
                        x1, y1, x2, y2 = map(int, box.xyxy[0])

                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                        label = f"fire {conf:.2f}"
                        cv2.putText(
                            frame,
                            label,
                            (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.6,
                            (0, 0, 255),
                            2
                        )

        cv2.imshow("Fire Detection - Camera", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

def test_video():

    VIDEO_PATH = "video chay.mp4"

    if not os.path.exists(VIDEO_PATH):
        print("❌ Không tìm thấy video:", VIDEO_PATH)
        return

    cap = cv2.VideoCapture(VIDEO_PATH)

    if not cap.isOpened():
        print("❌ Không mở được video")
        return

    print("🎥 Video started - Nhấn Q để thoát")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model.predict(
            frame,
            conf=0.01,
            verbose=False
        )

        for r in results:
            if r.boxes is not None:
                for box in r.boxes:
                    cls_id = int(box.cls[0])
                    conf = float(box.conf[0])
                    class_name = model.names[cls_id]

                    if class_name.lower() == "fire" and conf >= CONF_THRESHOLD:
                        x1, y1, x2, y2 = map(int, box.xyxy[0])

                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                        label = f"fire {conf:.2f}"
                        cv2.putText(
                            frame,
                            label,
                            (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.6,
                            (0, 0, 255),
                            2
                        )

        cv2.imshow("Fire Detection - Video", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


# =========================
# ========= MENU ==========
# =========================
if __name__ == "__main__":
    print("\nChọn chế độ:")
    print("1 - Test Webcam")
    print("2 - Test Ảnh Local")

    choice = input("Nhập lựa chọn (1/2): ")

    if choice == "1":
        test_video()
    elif choice == "2":
        test_image()
    else:
        print("❌ Lựa chọn không hợp lệ")
