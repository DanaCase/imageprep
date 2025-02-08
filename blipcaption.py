from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import os
import glob

# Load BLIP-2 model
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

# Input & Output Paths
image_folder = "/Users/danacase/code/data/MousseCroppedSquare"  # Change this
output_file = "/Users/danacase/code/data/MousseCropped/captions.txt"

# Process Each Image
with open(output_file, "w") as f:
    for image_path in glob.glob(os.path.join(image_folder, "*.jpg")):
        image = Image.open(image_path).convert("RGB")
        inputs = processor(images=image, return_tensors="pt")

        # Generate Caption
        output = model.generate(**inputs)
        caption = processor.decode(output[0], skip_special_tokens=True)

        # Save Caption
        f.write(f"{os.path.basename(image_path)}: {caption}\n")
        print(f"Generated Caption: {caption}")
