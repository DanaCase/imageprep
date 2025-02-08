import cv2
import os
import glob
from ultralytics import YOLO
from pillow_heif import register_heif_opener
from PIL import Image
import numpy as np

# Register HEIC support in PIL
register_heif_opener()

# Load the YOLOv8 model (pretrained on COCO dataset, which includes dogs)
model = YOLO("yolov8n.pt")

# Define the input and output directories
input_folder = "/Users/danacase/code/data/Mousse Unmodified"  # Change this
output_folder = "/Users/danacase/code/data/MousseCroppedSquare"  # Change this

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)


def resize_and_pad(image, size=512, pad_color=(0, 0, 0)):
    """ Resize and pad an image to keep aspect ratio while fitting into (size x size). """
    h, w = image.shape[:2]
    scale = size / max(h, w)  # Scale based on the longest side
    new_w, new_h = int(w * scale), int(h * scale)

    # Resize image
    resized = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_LINEAR)

    # Create new square canvas (size x size) with padding color
    padded = np.full((size, size, 3), pad_color, dtype=np.uint8)

    # Compute center offsets
    x_offset = (size - new_w) // 2
    y_offset = (size - new_h) // 2

    # Paste resized image onto the center of the padded canvas
    padded[y_offset:y_offset + new_h, x_offset:x_offset + new_w] = resized

    return padded


def make_yolo_box_square(yolo_box, img_width, img_height):
    """
    Convert a YOLO bounding box to a square while keeping it centered.

    :param yolo_box: A single YOLO box object (assumed format [x_center, y_center, width, height])
    :param img_width: Width of the image
    :param img_height: Height of the image
    :return: (x1, y1, x2, y2) coordinates of the square box
    """
    # Convert YOLO tensor to float values
    x_center, y_center, width, height = yolo_box.xywh[0].tolist()  # Ensure values are floats

    # Find the max dimension to make the box square
    max_size = max(width, height)

    # Compute new square box coordinates
    new_width = new_height = max_size

    # Adjust x1, y1, x2, y2
    x1 = x_center - new_width / 2
    y1 = y_center - new_height / 2
    x2 = x_center + new_width / 2
    y2 = y_center + new_height / 2

    # Ensure the box stays within image boundaries
    x1 = max(0, x1)
    y1 = max(0, y1)
    x2 = min(img_width, x2)
    y2 = min(img_height, y2)

    # Explicitly convert to integers to avoid OpenCV slicing issues
    return int(x1), int(y1), int(x2), int(y2)



# Process each image
for image_path in glob.glob(os.path.join(input_folder, "*.*")):
    try:
        # Check if the file is HEIC
        if image_path.lower().endswith(".heic"):
            # Convert HEIC to a format OpenCV can read (JPEG)
            img_pil = Image.open(image_path).convert("RGB")
            image_path_jpg = image_path.replace(".heic", ".jpg")
            img_pil.save(image_path_jpg, "JPEG")
            image_path = image_path_jpg  # Use the converted file

        # Read image
        img = cv2.imread(image_path)

        # Run YOLO detection
        results = model.predict(source=image_path, save=False)

        for r in results:
            for box in r.boxes:
                cls = int(box.cls.item())  # Get class index
                if cls == 16:  # Class 16 = "dog" in COCO dataset
                   # x1, y1, x2, y2 = map(int, box.xyxy[0])  # Get bounding box
                  
                    print(img.shape)
                    h, w, _ = img.shape
                    x1, y1, x2, y2 = make_yolo_box_square(box, w, h)
                    
                    print(x1, y1, x2, y2)
                    # Crop image
                    cropped = img[y1:y2, x1:x2]

                    print("got to here")
                    # final_image = resize_and_pad(cropped, size=512, pad_color=(0, 0, 0))  # Black padding

                    # Save as JPEG instead of HEIC
                    filename = os.path.basename(image_path).lower().replace(".heic", ".jpg")
                    output_path = os.path.join(output_folder, f"cropped_{filename}")
                    # cv2.imwrite(output_path, final_image)
                    cv2.imwrite(output_path, cropped)
                    print(f"Saved cropped dog: {output_path}")

    except Exception as e:
        print(f"Error processing {image_path}: {e}")

print("Processing complete!")

