import os
import glob
import cv2
import numpy as np
from ultralytics import YOLO
from pillow_heif import register_heif_opener
from PIL import Image
from rembg import remove
import argparse

typemap = {
        "dog": 16, 
        "cat": 17
        }

if __name__ == "__main__":
    argparse = argparse.ArgumentParser(description="Crop and remove background from dog images")
    argparse.add_argument("--input_folder", type=str, required=True)
    argparse.add_argument("--output_folder", type=str, required=True)
    argparse.add_argument("--image_category", type=str, default="dog")
    args = argparse.parse_args()
    input_folder = args.input_folder
    output_folder = args.output_folder
    
    os.makedirs(output_folder, exist_ok=True)
    
    # Register HEIC support
    register_heif_opener()

    model = YOLO("yolov8n.pt")  # YOLOv8 Small Model
    
    for image_path in glob.glob(os.path.join(input_folder, "*.*")):
        try:
            if image_path.lower().endswith(".heic"):
                img_pil = Image.open(image_path).convert("RGB")
                image_path_jpg = image_path.replace(".heic", ".jpg")
                img_pil.save(image_path_jpg, "JPEG")
                image_path = image_path_jpg
            
            img = cv2.imread(image_path)
            
            results = model.predict(source=image_path, save=False)
            
            for r in results:
                for box in r.boxes:
                    cls = int(box.cls.item())
                    if cls == 16:
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        cropped = img[y1:y2, x1:x2]
                        cropped_pil = Image.fromarray(cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB))
                        cropped_no_bg = remove(cropped_pil)
                        filename = os.path.basename(image_path).lower().replace(".heic", ".png").replace(".jpg", ".png")
                        output_path = os.path.join(output_folder, f"cropped_no_bg_{filename}")
                        cropped_no_bg.save(output_path, "PNG")
                        print(f"Saved cropped dog with no background: {output_path}")
        except Exception as e:
            print(f"Error processing {image_path}: {e}")
    print("Processing complete!")

