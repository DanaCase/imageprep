import os
import argparse


if __name__ == "__main__":
    argparse = argparse.ArgumentParser(description="Rename files in a folder")
    argparse.add_argument("--folder_path", type=str, required=True)
    args = argparse.parse_args()
    folder_path = args.folder_path

# Loop through all files in the folder
    for filename in os.listdir(folder_path):
        # Check if the file ends with ".json.txt"
        if filename.endswith(".jpg.txt"):
            # Create the new filename by replacing ".json.txt" with ".txt"
            new_filename = filename.replace(".jpg.txt", ".txt")

            # Construct full file paths
            old_path = os.path.join(folder_path, filename)
            new_path = os.path.join(folder_path, new_filename)

            # Rename the file
            os.rename(old_path, new_path)
            print(f"Renamed: {filename} ➝ {new_filename}")

    print("✅ Renaming complete!")
