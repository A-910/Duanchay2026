import firebase_admin
from firebase_admin import credentials, db, storage
from datetime import datetime
from app.config import DATABASE_URL, STORAGE_BUCKET

# =========================
# Init Firebase (an toàn)
# =========================
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")

    firebase_admin.initialize_app(cred, {
        "databaseURL": DATABASE_URL,
        "storageBucket": STORAGE_BUCKET
    })

bucket = storage.bucket()


# =========================
# Update trạng thái theo cam
# =========================
def update_status(device_id, result):

    ref = db.reference(f"fire_detection/{device_id}")

    ref.set({
        "result": result,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })


# =========================
# Upload ảnh phân theo cam
# =========================
def upload_image(device_id, image_bytes, fire_detected):

    # luôn ghi đè latest.jpg
    latest_blob = bucket.blob(f"{device_id}/latest.jpg")
    latest_blob.upload_from_string(image_bytes, content_type="image/jpeg")

    # nếu cháy → lưu thêm ảnh timestamp
    if fire_detected == 1:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        fire_blob = bucket.blob(f"{device_id}/fire_{timestamp}.jpg")
        fire_blob.upload_from_string(image_bytes, content_type="image/jpeg")

print("Bucket name:", storage.bucket().name)

