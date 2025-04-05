import os
from PIL import Image
import argparse


if __name__ == "__main__":
    argparse = argparse.ArgumentParser(description="Resize images to 512x512")
    argparse.add_argument("--input_folder", type=str, required=True)
    argparse.add_argument("--output_folder", type=str, required=True)
    args = argparse.parse_args()
    input_folder = args.input_folder
    output_folder = args.output_folder

# Ensure output directory exists
    os.makedirs(output_folder, exist_ok=True)

# Loop through all images in the input folder
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.webp')):  # Supported formats
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            # Open the image
            with Image.open(input_path) as img:
                # Ensure it's RGB (some images might be grayscale or CMYK)
                img = img.convert("RGB")

                # Resize to 512x512
                img = img.resize((512, 512), Image.LANCZOS)

                # Save the resized image
                img.save(output_path, "JPEG", quality=95)  # Change format if needed

                print(f"Resized and saved: {output_path}")

    print("✅ Image resizing complete!")

