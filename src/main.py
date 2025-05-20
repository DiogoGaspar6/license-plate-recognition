import os
import cv2
import numpy as np

def main():
    # Obter configurações da câmera a partir de variáveis de ambiente
    camera_device = int(os.getenv('CAMERA_DEVICE', 1)) # 0 para a câmera integrada, 1 para a câmera do iphone
    frame_width = int(os.getenv('FRAME_WIDTH', 1280))
    frame_height = int(os.getenv('FRAME_HEIGHT', 720))
    
    cap = cv2.VideoCapture(camera_device)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
    
    success, frame = cap.read()
    while success:
        success, frame = cap.read()
        cv2.imshow("frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    main()