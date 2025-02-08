import os

# Path to the captions file
captions_file = "/Users/danacase/code/data/MousseCroppedSquare/captions.txt"  # Change this if needed
output_folder = "/Users/danacase/code/data/MousseCroppedSquare"  # Where text files will be saved

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# Read captions file and create individual text files
with open(captions_file, "r") as f:
    for line in f:
        parts = line.strip().split(": ", 1)  # Split filename and caption
        if len(parts) == 2:
            filename, caption = parts
            text_filename = os.path.join(output_folder, f"{filename}.txt")

            # Write the caption to an individual text file
            with open(text_filename, "w") as txt_file:
                txt_file.write(caption.strip())

            print(f"Saved: {text_filename}")

print("✅ All captions saved as individual text files!")
