import os
import requests

# Set your Pinterest API credentials
ACCESS_TOKEN = "your_pinterest_access_token"  # Replace with your actual access token
BOARD_ID = "your_board_id"  # Replace with your Pinterest board ID

# API URL to fetch board pins
PINS_API_URL = f"https://api.pinterest.com/v5/boards/{BOARD_ID}/pins"

# Set headers for authorization
HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

# Folder to save images
OUTPUT_FOLDER = "pinterest_images"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def download_images():
    response = requests.get(PINS_API_URL, headers=HEADERS)
    
    if response.status_code == 200:
        pins = response.json().get("items", [])
        
        for pin in pins:
            image_url = pin.get("media", {}).get("image", {}).get("original", {}).get("url")
            if image_url:
                try:
                    # Get the image file name from URL
                    image_name = image_url.split("/")[-1].split("?")[0]
                    image_path = os.path.join(OUTPUT_FOLDER, image_name)
                    
                    # Download the image
                    img_data = requests.get(image_url).content
                    with open(image_path, "wb") as f:
                        f.write(img_data)
                    
                    print(f"✅ Downloaded: {image_name}")
                except Exception as e:
                    print(f"❌ Error downloading {image_url}: {e}")
    
    else:
        print(f"❌ Failed to fetch pins: {response.json()}")

# Run the script
download_images()

print("🎯 Image downloading complete!")
