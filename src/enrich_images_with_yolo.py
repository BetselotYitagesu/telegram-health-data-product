import os
import re
import pandas as pd
from ultralytics import YOLO

# Load model
model = YOLO("yolov8n.pt")  # or yolov8s.pt for slightly better results

# Output file
OUTPUT_CSV = "data/processed/image_detections.csv"


def extract_message_id(filename):
    match = re.search(r"_(\d+)\.jpg$", filename)
    return int(match.group(1)) if match else None


def run_detection_on_folder(folder_path):
    records = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg"):
            image_path = os.path.join(folder_path, filename)
            print(f"🔍 Processing {image_path}")

            message_id = extract_message_id(filename)
            if not message_id:
                print(f"⚠️ Skipping {filename} (no message ID)")
                continue

            results = model(image_path, verbose=False)[0]

            for r in results.boxes.data.tolist():
                x1, y1, x2, y2, score, class_id = r
                class_name = results.names[int(class_id)]
                records.append({
                    "message_id": message_id,
                    "class_name": class_name,
                    "confidence": round(score, 3),
                    "image_file": filename
                })

    return pd.DataFrame(records)


if __name__ == "__main__":
    all_records = []

    root_dir = "data/raw/images"
    for date_folder in os.listdir(root_dir):
        folder_path = os.path.join(root_dir, date_folder)
        if os.path.isdir(folder_path):
            df = run_detection_on_folder(folder_path)
            all_records.append(df)

    if all_records:
        final_df = pd.concat(all_records)
        os.makedirs("data/processed", exist_ok=True)
        final_df.to_csv(OUTPUT_CSV, index=False)
        print(f"✅ Detections saved to {OUTPUT_CSV}")
    else:
        print("❌ No image detections found.")
