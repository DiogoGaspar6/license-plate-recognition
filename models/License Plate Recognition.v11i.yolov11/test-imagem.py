import os
import cv2
import numpy as np
import pandas as pd
from ultralytics import YOLO
import easyocr

# Configurações globais
MODEL_WEIGHTS = 'runs/detect/matriculas-modelo5/weights/best.pt'
OUTPUT_DIR = 'detected_license_plates'
EXCEL_FILE = 'license_plates.xlsx'
MIN_CONFIDENCE = 0.80  # Confiança mínima para considerar válido
REQUIRED_LENGTH = 6    # Comprimento exato para matrículas portuguesas

# Inicialização do OCR
reader = easyocr.Reader(['en'], 
                       gpu=True,
                       model_storage_directory='./model_weights',
                       download_enabled=True)

# Estruturas de dados
detected_plates = []
license_plate_data = []

def is_valid_plate(text, confidence):
    """Verifica se a matrícula cumpre os critérios"""
    return (len(text) == REQUIRED_LENGTH and 
            confidence >= MIN_CONFIDENCE and
            text.isalnum())  # Só caracteres alfanuméricos

def preprocess_plate(plate_img):
    """Melhora a qualidade da imagem para OCR"""
    gray = cv2.cvtColor(plate_img, cv2.COLOR_BGR2GRAY)
    
    # Aumento de contraste
    alpha = 1.5  # Contraste (1.0-3.0)
    beta = 0     # Brilho
    enhanced = cv2.convertScaleAbs(gray, alpha=alpha, beta=beta)
    
    # Equalização de histograma
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    final = clahe.apply(enhanced)
    
    return final

def extract_plate_text(plate_img):
    """Extrai texto da placa com pós-processamento rigoroso"""
    processed = preprocess_plate(plate_img)
    
    # Configuração específica para matrículas portuguesas
    text_results = reader.readtext(processed,
                                 decoder='beamsearch',
                                 beamWidth=15,  # Aumentado para maior precisão
                                 batch_size=1,
                                 allowlist='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
                                 width_ths=0.5,  # Tolerância para espaçamento
                                 height_ths=0.5)
    
    # Combina todos os textos detectados
    plate_text = "".join([res[1] for res in text_results]).strip()
    
    # Pós-processamento adicional
    plate_text = plate_text.upper()
    
    # Corrige confusões comuns
    common_errors = {'I': '1', 'O': '0', 'Z': '2', 'B': '8'}
    corrected_text = []
    for char in plate_text:
        corrected_text.append(common_errors.get(char, char))
    plate_text = "".join(corrected_text)
    
    return plate_text, text_results

def detect_and_process(frame, model):
    """Detecta e processa matrículas no frame com critérios rigorosos"""
    results = model(frame)[0]
    
    for box in results.boxes:
        confidence = float(box.conf[0])
        if confidence >= MIN_CONFIDENCE:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            
            plate_img = frame[y1:y2, x1:x2]
            plate_text, raw_text = extract_plate_text(plate_img)
            
            if is_valid_plate(plate_text, confidence):
                print(f"Matrícula válida detectada: {plate_text} (Confiança: {confidence:.2f})")
                
                # Garante diretório de saída
                if not os.path.exists(OUTPUT_DIR):
                    os.makedirs(OUTPUT_DIR)
                
                # Nome do arquivo com matrícula e confiança
                plate_path = f"{OUTPUT_DIR}/{plate_text}_{confidence:.2f}.jpg"
                cv2.imwrite(plate_path, plate_img)
                
                # Armazena apenas se for nova
                if plate_text not in [entry['text'] for entry in license_plate_data]:
                    license_plate_data.append({
                        'image_path': plate_path,
                        'text': plate_text,
                        'confidence': confidence,
                        'detection_coords': f"{x1},{y1},{x2},{y2}"
                    })
                    
                    # Desenha no frame
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, 
                               f"{plate_text} ({confidence:.2f})", 
                               (x1, y1-10), 
                               cv2.FONT_HERSHEY_SIMPLEX, 
                               0.7, (0, 255, 0), 2)

def main():
    # Configuração da câmera
    cap = cv2.VideoCapture(1)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    # Carrega o modelo
    model = YOLO(MODEL_WEIGHTS)
    
    try:
        while True:
            success, frame = cap.read()
            if not success:
                break
                
            detect_and_process(frame, model)
            
            # Atualiza o Excel se houver novas detecções
            if license_plate_data:
                df = pd.DataFrame(license_plate_data)
                df.to_excel(EXCEL_FILE, index=False)
            
            cv2.imshow("Sistema de Matrículas Portuguesas", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()