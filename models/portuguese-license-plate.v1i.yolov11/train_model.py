from ultralytics import YOLO

model = YOLO("yolo11n.pt")

model.train(
    data="data.yaml",
    epochs=50,
    imgsz=640,
    batch=8,
    name="matriculas-modelo-novo"
)
