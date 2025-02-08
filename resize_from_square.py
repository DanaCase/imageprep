import os
from PIL import Image

# Set input and output folders
input_folder = "/Users/danacase/code/data/MousseCroppedSquare"  # Change this
output_folder = "/Users/danacase/code/data/MousseCroppedSquare512"  # Change this

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

