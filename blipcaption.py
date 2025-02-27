from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import os
import glob
import argparse

if __name__ == "__main__":
    argparse = argparse.ArgumentParser(description="Generate captions for images")
    argparse.add_argument("--image_folder", type=str, required=True)
    argparse.add_argument("--output_file", type=str, required=True)
    args = argparse.parse_args()

    # Load BLIP-2 model
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

    # Process Each Image
    with open(args.output_file, "w") as f:
        for image_path in glob.glob(os.path.join(args.image_folder, "*.jpg")):
            image = Image.open(image_path).convert("RGB")
            inputs = processor(images=image, return_tensors="pt")

            # Generate Caption
            output = model.generate(**inputs)
            caption = processor.decode(output[0], skip_special_tokens=True)

            # Save Caption
            f.write(f"{os.path.basename(image_path)}: {caption}\n")
            print(f"Generated Caption: {caption}")
