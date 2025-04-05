import os
import argparse

if __name__ == "__main__":
    argparse = argparse.ArgumentParser(
            description="convert captions to per image files")
    argparse.add_argument("--captions_file", type=str, required=True)
    argparse.add_argument("--output_folder", type=str, required=True)
    args = argparse.parse_args()
    captions_file = args.captions_file
    output_folder = args.output_folder

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
