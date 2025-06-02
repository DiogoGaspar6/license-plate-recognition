from ultralytics import YOLO

model = YOLO('runs/detect/matriculas-modelo3/weights/best.pt')


results = model('imagem/imagem.jpg')

# Mostra o resultado com bounding boxes
results[0].show()
