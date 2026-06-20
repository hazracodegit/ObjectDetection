from flask import Flask, render_template, request, jsonify
from ultralytics import YOLO
import cv2
import os
import uuid

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
RESULT_FOLDER = "static/results"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

model = YOLO("yolov8n.pt")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/detect", methods=["POST"])
def detect():

    file = request.files["image"]

    filename = f"{uuid.uuid4()}.jpg"
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    file.save(filepath)

    results = model(filepath)

    img = cv2.imread(filepath)

    detected_objects = []

    for r in results:

        for box in r.boxes:

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            conf = float(box.conf[0])

            cls = int(box.cls[0])

            label = model.names[cls]

            detected_objects.append({
                "name": label,
                "confidence": round(conf * 100, 2)
            })

            cv2.rectangle(
                img,
                (x1, y1),
                (x2, y2),
                (0,255,0),
                2
            )

            cv2.putText(
                img,
                f"{label} {conf:.2f}",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0,255,0),
                2
            )

    result_name = f"result_{filename}"

    result_path = os.path.join(
        RESULT_FOLDER,
        result_name
    )

    cv2.imwrite(result_path, img)

    return jsonify({
        "image": f"/static/results/{result_name}",
        "objects": detected_objects,
        "count": len(detected_objects)
    })

if __name__ == "__main__":
    app.run(debug=True)