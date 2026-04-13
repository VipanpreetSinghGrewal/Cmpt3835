import tempfile
from pathlib import Path

import gradio as gr
import pandas as pd
from PIL import Image
from ultralytics import YOLO

BASE_DIR = Path("/workspaces/Cmpt3835")
MODEL_PATH = BASE_DIR / "egg_detector" / "weights" / "best.pt"
RUN_FOLDER = BASE_DIR / "egg_detector"

if not MODEL_PATH.exists():
    print(f"Model not found yet: {MODEL_PATH}")
    print("Run train_model.py first to create best.pt")
    model = None
else:
    model = YOLO(str(MODEL_PATH))


def predict_image(image):
    if model is None:
        return None, pd.DataFrame(
            [{"error": "Model not trained yet. Run train_model.py first."}]
        )

    if image is None:
        return None, pd.DataFrame(columns=["class_id", "species", "confidence"])

    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
        temp_path = tmp.name
        image.save(temp_path)

    results = model.predict(source=temp_path, conf=0.25)
    result = results[0]

    plotted = result.plot()
    plotted_image = Image.fromarray(plotted)

    rows = []
    if result.boxes is not None and len(result.boxes) > 0:
        class_ids = result.boxes.cls.cpu().numpy().tolist()
        confidences = result.boxes.conf.cpu().numpy().tolist()

        for cls_id, conf in zip(class_ids, confidences):
            cls_id = int(cls_id)
            rows.append(
                {
                    "class_id": cls_id,
                    "species": result.names[cls_id],
                    "confidence": round(float(conf), 4),
                }
            )

    df = pd.DataFrame(rows)
    return plotted_image, df


def get_run_images():
    image_paths = []
    wanted_files = [
        "results.png",
        "confusion_matrix.png",
        "PR_curve.png",
        "F1_curve.png",
        "P_curve.png",
        "R_curve.png",
    ]

    for name in wanted_files:
        path = RUN_FOLDER / name
        if path.exists():
            image_paths.append(str(path))

    return image_paths


with gr.Blocks() as demo:
    gr.Markdown("# RAM Egg Detection App")
    gr.Markdown(
        "Upload an egg image, run prediction, and view detected species and confidence scores."
    )

    with gr.Tab("Predict"):
        with gr.Row():
            input_image = gr.Image(type="pil", label="Upload Image")
            output_image = gr.Image(type="pil", label="Prediction Output")

        output_table = gr.Dataframe(label="Detection Summary")
        predict_button = gr.Button("Run Prediction")

        predict_button.click(
            fn=predict_image,
            inputs=input_image,
            outputs=[output_image, output_table],
        )

    with gr.Tab("Model Evaluation Plots"):
        gallery = gr.Gallery(
            value=get_run_images(),
            label="Saved Training/Evaluation Plots",
            columns=2,
        )

demo.launch(server_name="0.0.0.0", server_port=7860)