import cv2
from ultralytics import YOLO
import pytesseract
import os

# Load the YOLO model
model = YOLO('best.pt')

# Read the image
image_path = 'detected_license_plates/license_plate_3.jpg'
frame = cv2.imread(image_path)

# Function to detect and process license plates
def detect_license_plate(frame, model):
    results = model(frame)[0]
    for box in results.boxes:
        cls = int(box.cls[0])
        conf = float(box.conf[0])
        if cls == 0 and conf > 0.5:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            license_plate = frame[y1:y2, x1:x2]
            text = pytesseract.image_to_string(license_plate, config='--psm 8').strip()
            print(f"Detected license plate: {text}")
            cv2.imshow('License Plate', license_plate)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

# Detect license plates in the image
detect_license_plate(frame, model)