import cv2
from ultralytics import YOLO

model = YOLO('runs/detect/matriculas-modelo-novo/weights/best.pt')

# Abre o vídeo
cap = cv2.VideoCapture('imagem/video.mp4')

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Detecção de matrículas
    results = model(frame)[0]
    for box in results.boxes:
        cls = int(box.cls[0])
        conf = float(box.conf[0])
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        
        # Desenhar a caixa
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, f"Placa: {conf:.2f}", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    # Mostra o frame
    cv2.imshow('Detecção de Matrículas', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()