import os
import glob
import cv2
import numpy as np
from ultralytics import YOLO
from pillow_heif import register_heif_opener
from PIL import Image
from rembg import remove

# Register HEIC support
register_heif_opener()

# Load YOLO model
model = YOLO("yolov8n.pt")  # YOLOv8 Small Model

# Define input/output folders
# Define the input and output directories
input_folder = "/Users/danacase/code/data/Mousse Unmodified"  # Change this
output_folder = "/Users/danacase/code/data/MousseCroppedNoBG" # Change this
os.makedirs(output_folder, exist_ok=True)

# Process each image
for image_path in glob.glob(os.path.join(input_folder, "*.*")):
    try:
        # Convert HEIC to JPG if needed
        if image_path.lower().endswith(".heic"):
            img_pil = Image.open(image_path).convert("RGB")
            image_path_jpg = image_path.replace(".heic", ".jpg")
            img_pil.save(image_path_jpg, "JPEG")
            image_path = image_path_jpg  # Use the converted file

        # Load image using OpenCV
        img = cv2.imread(image_path)

        # Run YOLO detection
        results = model.predict(source=image_path, save=False)

        for r in results:
            for box in r.boxes:
                cls = int(box.cls.item())  # Get class index
                if cls == 16:  # Class 16 = "dog" in COCO dataset
                    x1, y1, x2, y2 = map(int, box.xyxy[0])  # Get bounding box

                    # Crop the detected dog
                    cropped = img[y1:y2, x1:x2]

                    # Convert to PIL format for background removal
                    cropped_pil = Image.fromarray(cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB))

                    # Remove background
                    cropped_no_bg = remove(cropped_pil)  # Transparent BG

                    # Save as PNG (to preserve transparency)
                    filename = os.path.basename(image_path).lower().replace(".heic", ".png").replace(".jpg", ".png")
                    output_path = os.path.join(output_folder, f"cropped_no_bg_{filename}")
                    cropped_no_bg.save(output_path, "PNG")

                    print(f"Saved cropped dog with no background: {output_path}")

    except Exception as e:
        print(f"Error processing {image_path}: {e}")

print("Processing complete!")
