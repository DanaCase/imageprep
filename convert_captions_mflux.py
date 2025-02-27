import json
import argparse

def convert_captions_to_json(input_file):
    """
    Converts a text file with 'filename: caption' format into a structured JSON format
    and prints it to the console.

    :param input_file: Path to the input text file.
    """
    data = []

    with open(input_file, "r") as f:
        for line in f:
            # Split the line into image filename and caption
            if ": " in line:
                image, prompt = line.strip().split(": ", 1)
                data.append({"image": image, "prompt": prompt})

    # Print JSON output to the console
    print(json.dumps(data, indent=4))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert caption text file to JSON format and print to console.")
    parser.add_argument("input_file", type=str, help="Path to the input text file")
    args = parser.parse_args()

    convert_captions_to_json(args.input_file)

