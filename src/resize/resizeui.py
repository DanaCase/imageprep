import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from pillow_heif import register_heif_opener

MAX_WIDTH = 1000
MAX_HEIGHT = 800
HANDLE_SIZE = 12

class SquareCropperApp:
    def __init__(self, root):
        register_heif_opener() 
        self.root = root
        self.root.title("Square Cropper")
        self.image_path = filedialog.askopenfilename()
        if not self.image_path:
            exit()

        self.original_image = Image.open(self.image_path)
        self.display_image, self.scale = self.scale_image_to_fit(self.original_image)

        self.tk_image = ImageTk.PhotoImage(self.display_image)

        self.canvas = tk.Canvas(root, width=self.tk_image.width(), height=self.tk_image.height())
        self.canvas.pack()

        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

        self.set_square()

        self.dragging = False
        self.resizing = False

        self.drag_offset_x = 0
        self.drag_offset_y = 0

        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

        save_button = tk.Button(root, text="Save Selection", command=self.save_selection)
        save_button.pack(pady=10)

        reset_button = tk.Button(root, text="Reset Square", command=self.set_square)

    def scale_image_to_fit(self, img):
        width, height = img.size
        scale = min(MAX_WIDTH / width, MAX_HEIGHT / height, 1.0)
        new_size = (int(width * scale), int(height * scale))
        return img.resize(new_size, Image.LANCZOS), scale

    def set_square(self):
        # Default square: largest centered square
        side = min(self.tk_image.width(), self.tk_image.height())
        self.start_x = (self.tk_image.width() - side) // 2
        self.start_y = (self.tk_image.height() - side) // 2
        self.end_x = self.start_x + side
        self.end_y = self.start_y + side

        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.end_x, self.end_y, outline='red', width=2)

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

    def save_selection(self):
        # Convert display coords back to original image coords
        crop_box_display = (self.start_x, self.start_y, self.end_x, self.end_y)
        crop_box_original = tuple(int(coord / self.scale) for coord in crop_box_display)

        cropped = self.original_image.crop(crop_box_original)

        res_win = tk.Toplevel(self.root)
        res_win.title("Output Resolution")

        tk.Label(res_win, text="Output resolution (e.g., 512):").pack()
        res_entry = tk.Entry(res_win)
        res_entry.pack()
        res_entry.insert(0, "512")

        def do_save():
            try:
                resolution = int(res_entry.get())
                resized = cropped.resize((resolution, resolution), Image.LANCZOS)
                save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
                if save_path:
                    resized.save(save_path)
                res_win.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Could not save image:\n{e}")        

        tk.Button(res_win, text="Save", command=do_save).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = SquareCropperApp(root)
    root.mainloop()

