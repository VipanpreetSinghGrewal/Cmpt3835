from pathlib import Path
from ultralytics import YOLO

BASE_DIR = Path("/workspaces/Cmpt3835")
DATA_YAML = BASE_DIR / "data.yaml"

if not DATA_YAML.exists():
    raise FileNotFoundError(f"data.yaml not found: {DATA_YAML}")

model = YOLO("yolov8s.pt")

model.train(
    data=str(DATA_YAML),
    epochs=5,
    imgsz=640,
    batch=8,
    project=str(BASE_DIR),
    name="egg_detector"
)

print("Training complete.")
print("Model created at:", BASE_DIR / "egg_detector" / "weights" / "best.pt")