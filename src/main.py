import os
import cv2
import numpy as np
import pandas as pd
from ultralytics import YOLO
import easyocr


MODEL_WEIGHTS = 'bestv2.pt'
OUTPUT_DIR = 'detected_license_plates'
EXCEL_FILE = 'license_plates.xlsx'
MIN_CONFIDENCE = 0.80  
REQUIRED_LENGTH = 6    
HIGH_CONFIDENCE = 0.90 

reader = easyocr.Reader(['en'], 
                       gpu=True,
                       model_storage_directory='./model_weights',
                       download_enabled=True)


detected_plates = []
license_plate_data = []

def is_new_detection(x1, y1, x2, y2, threshold=50):
    for (px1, py1, px2, py2) in detected_plates:
        if (abs(x1 - px1) < threshold and 
           abs(y1 - py1) < threshold and 
           abs(x2 - px2) < threshold and
           abs(y2 - py2) < threshold):
            return False
    return True

def is_valid_plate(text, confidence):
    return (len(text) == REQUIRED_LENGTH and 
            confidence >= MIN_CONFIDENCE and
            text.isalnum()) 

def preprocess_plate(plate_img):
    gray = cv2.cvtColor(plate_img, cv2.COLOR_BGR2GRAY)
    
    alpha = 1.5  
    beta = 0     
    enhanced = cv2.convertScaleAbs(gray, alpha=alpha, beta=beta)
    
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    final = clahe.apply(enhanced)
    
    _, thresh = cv2.threshold(final, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    return thresh

def extract_plate_text(plate_img):
    processed = preprocess_plate(plate_img)

    text_results = reader.readtext(processed,
                                 decoder='beamsearch',
                                 beamWidth=15,
                                 batch_size=1,
                                 allowlist='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
                                 width_ths=0.5,
                                 height_ths=0.5)
    
    text_results.sort(key=lambda x: x[0][0][0]) 
    
    plate_text = "".join([res[1] for res in text_results]).strip()
    plate_text = plate_text.upper()

    
    return plate_text, text_results

def detect_and_process(frame, model):
    results = model(frame)[0]
    
    for box in results.boxes:
        confidence = float(box.conf[0])
        if confidence >= MIN_CONFIDENCE:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            
            if not is_new_detection(x1, y1, x2, y2):
                continue
                
            plate_img = frame[y1:y2, x1:x2]
            plate_text, raw_text = extract_plate_text(plate_img)
            
            if is_valid_plate(plate_text, confidence):
                print(f"Matrícula detectada: {plate_text} (Confiança: {confidence:.2f})")
                
                # Garante diretório de saída
                if not os.path.exists(OUTPUT_DIR):
                    os.makedirs(OUTPUT_DIR)
                
                # Armazena apenas se for de alta confiança ou nova
                if confidence >= HIGH_CONFIDENCE or plate_text not in [entry['text'] for entry in license_plate_data]:
                    # Nome do arquivo com matrícula e confiança
                    plate_path = f"{OUTPUT_DIR}/{plate_text}_{confidence:.2f}.jpg"
                    cv2.imwrite(plate_path, plate_img)
                    
                    license_plate_data.append({
                        'image_path': plate_path,
                        'text': plate_text,
                        'confidence': confidence,
                        'detection_coords': f"{x1},{y1},{x2},{y2}",
                        'high_confidence': confidence >= HIGH_CONFIDENCE
                    })
                    
                    detected_plates.append((x1, y1, x2, y2))
                    
                    color = (0, 255, 0) if confidence >= HIGH_CONFIDENCE else (0, 0, 255)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(frame, 
                               f"{plate_text} ({confidence:.2f})", 
                               (x1, y1-10), 
                               cv2.FONT_HERSHEY_SIMPLEX, 
                               0.7, color, 2)

def main():
    cap = cv2.VideoCapture(1)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    model = YOLO(MODEL_WEIGHTS)
    
    try:
        while True:
            success, frame = cap.read()
            if not success:
                break
                
            detect_and_process(frame, model)
            
            if license_plate_data and len(license_plate_data) % 5 == 0:
                df = pd.DataFrame(license_plate_data)
                
                df = df.sort_values('confidence', ascending=False)
                df.to_excel(EXCEL_FILE, index=False)
            
            cv2.imshow("Sistema de Matrículas Portuguesas", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    finally:
        if license_plate_data:
            df = pd.DataFrame(license_plate_data)
            df = df.sort_values('confidence', ascending=False)
            df.to_excel(EXCEL_FILE, index=False)
        
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()