import os
import json
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

import torch
from transformers import Blip2Processor, Blip2ForConditionalGeneration

# Load BLIP2 once at the start
device = "mps" if torch.mps.is_available() else "cpu"
processor = Blip2Processor.from_pretrained("Salesforce/blip2-opt-2.7b")
model = Blip2ForConditionalGeneration.from_pretrained(
    "Salesforce/blip2-opt-2.7b",
    torch_dtype=torch.float32
).to(device)
model.eval()

SUPPORTED_EXTS = ('.jpg', '.jpeg', '.png', '.webp', '.heic', '.tif', '.tiff')
MAX_WIDTH = 1000
MAX_HEIGHT = 800

class CaptioningApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Captioner")

        self.folder_path = filedialog.askdirectory(title="Choose Folder of Images")
        if not self.folder_path:
            exit()

        self.image_files = sorted([
            f for f in os.listdir(self.folder_path)
            if f.lower().endswith(SUPPORTED_EXTS)
        ])

        if not self.image_files:
            messagebox.showinfo("No Images", "No supported images found in folder.")
            exit()

        self.caption_data = {}
        self.caption_path = os.path.join(self.folder_path, "captions.json")
        if os.path.exists(self.caption_path):
            with open(self.caption_path, "r") as f:
                self.caption_data = json.load(f)

        self.current_index = 0
        self.init_ui()
        self.load_next_image()

    def init_ui(self):
        self.canvas = tk.Canvas(self.root)
        self.canvas.pack()

        self.caption_var = tk.StringVar()
        self.entry = tk.Entry(self.root, textvariable=self.caption_var, width=80, font=("Helvetica", 12))
        self.entry.pack(pady=10)

        controls = tk.Frame(self.root)
        controls.pack(pady=10)

        tk.Button(controls, text="Save & Next", command=self.save_and_next).pack(side=tk.LEFT, padx=5)
        tk.Button(controls, text="Skip", command=self.skip).pack(side=tk.LEFT, padx=5)
        tk.Button(controls, text="Quit", command=self.root.quit).pack(side=tk.LEFT, padx=5)

    def scale_image_to_fit(self, img):
        width, height = img.size
        scale = min(MAX_WIDTH / width, MAX_HEIGHT / height, 1.0)
        new_size = (int(width * scale), int(height * scale))
        return img.resize(new_size, Image.LANCZOS)

    def load_next_image(self):
        if self.current_index >= len(self.image_files):
            messagebox.showinfo("Done", "All images captioned.")
            self.save_json()
            self.root.quit()
            return

        filename = self.image_files[self.current_index]
        full_path = os.path.join(self.folder_path, filename)

        try:
            image = Image.open(full_path).convert("RGB")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open image {filename}:\n{e}")
            self.current_index += 1
            self.load_next_image()
            return

        self.original_image = image
        display_image = self.scale_image_to_fit(image)
        self.tk_image = ImageTk.PhotoImage(display_image)

        self.canvas.config(width=self.tk_image.width(), height=self.tk_image.height())
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

        if filename in self.caption_data:
            self.caption_var.set(self.caption_data[filename])
        else:
            caption = self.generate_caption(image)
            self.caption_var.set(caption)

    def generate_caption(self, image):
        try:
            inputs = processor(images=image, return_tensors="pt").to(device)
            generated_ids = model.generate(**inputs, max_new_tokens=50)
            caption = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
            return caption
        except Exception as e:
            print(f"BLIP2 error: {e}")
            return ""

    def save_and_next(self):
        filename = self.image_files[self.current_index]
        self.caption_data[filename] = self.caption_var.get().strip()
        self.save_json()
        self.current_index += 1
        self.load_next_image()

    def skip(self):
        self.current_index += 1
        self.load_next_image()

    def save_json(self):
        with open(self.caption_path, "w") as f:
            json.dump(self.caption_data, f, indent=2)

if __name__ == "__main__":
    root = tk.Tk()
    app = CaptioningApp(root)
    root.mainloop()

