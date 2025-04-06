import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from pillow_heif import register_heif_opener
import os

MAX_WIDTH = 1000
MAX_HEIGHT = 800
HANDLE_SIZE = 12
SUPPORTED_EXTS = ('.jpg', '.jpeg', '.png', '.webp', '.heic', '.tif', '.tiff')

class SquareCropperApp:
    def __init__(self, root):
        register_heif_opener() 
        self.root = root
        self.root.title("Square Cropper")

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

        self.current_index = 0
        self.output_resolution = None
        self.init_ui()
        self.load_next_image()


    def init_ui(self):
        self.canvas = tk.Canvas(self.root)
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        
        controls = tk.Frame(self.root)
        controls.pack(pady=10)

        tk.Button(controls, text="Save & Next", command=self.save_and_next).pack(side=tk.LEFT, padx=5)
        tk.Button(controls, text="Skip", command=self.skip).pack(side=tk.LEFT, padx=5)
        tk.Button(controls, text="Quit", command=self.root.quit).pack(side=tk.LEFT, padx=5)
        tk.Button(controls, text="Reset Square", command=self.set_square).pack(side=tk.LEFT, padx=5)


    def scale_image_to_fit(self, img):
        width, height = img.size
        scale = min(MAX_WIDTH / width, MAX_HEIGHT / height, 1.0)
        new_size = (int(width * scale), int(height * scale))
        return img.resize(new_size, Image.LANCZOS), scale

    def load_next_image(self):
        if self.current_index >= len(self.image_files):
            messagebox.showinfo("Done", "Finished processing all images.")
            self.root.quit()
            return

        filename = self.image_files[self.current_index]
        full_path = os.path.join(self.folder_path, filename)

        try:
            self.original_image = Image.open(full_path)
        except Exception as e:
            messagebox.showerror("Error", f"Could not open image {filename}:\n{e}")
            self.current_index += 1
            self.load_next_image()
            return

        self.display_image, self.scale = self.scale_image_to_fit(self.original_image)
        self.tk_image = ImageTk.PhotoImage(self.display_image)

        self.canvas.config(width=self.tk_image.width(), height=self.tk_image.height())
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

        self.set_square()
        self.dragging = False
        self.resizing = False

        if self.output_resolution is None:
            self.ask_resolution()


    def set_square(self):
        self.rect = None 
        # Default square: largest centered square
        side = min(self.tk_image.width(), self.tk_image.height())
        self.start_x = (self.tk_image.width() - side) // 2
        self.start_y = (self.tk_image.height() - side) // 2
        self.end_x = self.start_x + side
        self.end_y = self.start_y + side

        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.end_x, self.end_y, outline='red', width=2)

    def ask_resolution(self):
        popup = tk.Toplevel(self.root)
        popup.title("Set Output Resolution")

        tk.Label(popup, text="Output square resolution (e.g., 512):").pack(pady=5)
        entry = tk.Entry(popup)
        entry.pack()
        entry.insert(0, "512")

        def confirm():
            try:
                self.output_resolution = int(entry.get())
                popup.destroy()
            except ValueError:
                messagebox.showerror("Invalid", "Please enter a valid number.")

        tk.Button(popup, text="OK", command=confirm).pack(pady=10)
        popup.grab_set()

    def on_click(self, event):
        # Check if we're near the bottom-right corner
        if abs(event.x - self.end_x) < HANDLE_SIZE and abs(event.y - self.end_y) < HANDLE_SIZE:
            self.resizing = True
        elif self.start_x <= event.x <= self.end_x and self.start_y <= event.y <= self.end_y:
            self.dragging = True
            self.drag_offset_x = event.x - self.start_x
            self.drag_offset_y = event.y - self.start_y


    def on_drag(self, event):
        if self.resizing:
            new_size = max(10, min(event.x - self.start_x, event.y - self.start_y))
            self.end_x = self.start_x + new_size
            self.end_y = self.start_y + new_size
        elif self.dragging:
            square_size = self.end_x - self.start_x
            new_start_x = event.x - self.drag_offset_x
            new_start_y = event.y - self.drag_offset_y

            # Clamp to canvas bounds
            new_start_x = max(0, min(new_start_x, self.tk_image.width() - square_size))
            new_start_y = max(0, min(new_start_y, self.tk_image.height() - square_size))

            self.start_x = new_start_x
            self.start_y = new_start_y
            self.end_x = self.start_x + square_size
            self.end_y = self.start_y + square_size

        self.canvas.coords(self.rect, self.start_x, self.start_y, self.end_x, self.end_y)

    def on_release(self, event):
        self.dragging = False
        self.resizing = False

    def save_and_next(self):
        filename = os.path.splitext(self.image_files[self.current_index])[0]
        save_dir = os.path.join(self.folder_path, "cropped")
        os.makedirs(save_dir, exist_ok=True)

        crop_box_display = (self.start_x, self.start_y, self.end_x, self.end_y)
        crop_box_original = tuple(int(coord / self.scale) for coord in crop_box_display)
        cropped = self.original_image.crop(crop_box_original)
        resized = cropped.resize((self.output_resolution, self.output_resolution), Image.LANCZOS)

        save_path = os.path.join(save_dir, f"{filename}_cropped.png")
        try:
            resized.save(save_path)
        except Exception as e:
            messagebox.showerror("Save Error", f"Could not save image:\n{e}")
        
        self.current_index += 1
        self.load_next_image()

    def skip(self):
        self.current_index += 1
        self.load_next_image()

if __name__ == "__main__":
    root = tk.Tk()
    app = SquareCropperApp(root)
    root.mainloop()

