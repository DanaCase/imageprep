import os

# Set the folder path where the files are located
folder_path = "/Users/danacase/code/data/MousseCroppedSquare"  # Change this to your actual folder path

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
