from PIL import Image
import os
import argparse

folder_path = "/Users/danacase/code/data/MousseCropped/"

if __name__ == "__main__":
    argparse = argparse.ArgumentParser(description="Check image file formats")
    argparse.add_argument("--image_folder", type=str, required=True)
    args = argparse.parse_args()

    for file in os.listdir(args.image_folder):
        file_path = os.path.join(folder_path, file)
        try:
            with Image.open(file_path) as img:
                print(f"{file}: {img.format}")
        except Exception as e:
            print(f"Error with {file}: {e}")
