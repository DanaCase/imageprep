from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import os
import glob
import argparse
import itertools

if __name__ == "__main__":
    argparse = argparse.ArgumentParser(description="Generate captions for images")
    argparse.add_argument("--image_folder", type=str, required=True)
    argparse.add_argument("--output_file", type=str, help="Output filepath for captions")
    args = argparse.parse_args()

    if args.output_file is None:
        args.output_file = os.path.join(args.image_folder, "captions.txt")

    # Load BLIP-2 model
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

    image_paths = sorted(itertools.chain(
        glob.glob(os.path.join(args.image_folder, "*.jpg")),
        glob.glob(os.path.join(args.image_folder, "*.jpeg"))
        )
    )

    # Process Each Image
    with open(args.output_file, "w") as f:
        for image_path in image_paths:
            image = Image.open(image_path).convert("RGB")
            inputs = processor(images=image, return_tensors="pt")

            # Generate Caption
            output = model.generate(**inputs)
            caption = processor.decode(output[0], skip_special_tokens=True)

            # Save Caption
            f.write(f"{os.path.basename(image_path)}: {caption}\n")
            print(f"Generated Caption: {caption}")
