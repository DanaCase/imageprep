from PIL import Image
import os

folder_path = "/Users/danacase/code/data/MousseCropped/"

for file in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file)
    try:
        with Image.open(file_path) as img:
            print(f"{file}: {img.format}")
    except Exception as e:
        print(f"Error with {file}: {e}")
