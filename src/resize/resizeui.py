import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class SquareCropperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Square Cropper")
        self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])
        if not self.image_path:
            exit()

        self.original_image = Image.open(self.image_path)
        self.tk_image = ImageTk.PhotoImage(self.original_image)

        self.canvas = tk.Canvas(root, width=self.tk_image.width(), height=self.tk_image.height())
        self.canvas.pack()

        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

        # Default square: largest centered square
        side = min(self.tk_image.width(), self.tk_image.height())
        self.start_x = (self.tk_image.width() - side) // 2
        self.start_y = (self.tk_image.height() - side) // 2
        self.end_x = self.start_x + side
        self.end_y = self.start_y + side

        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.end_x, self.end_y, outline='red', width=2)
        self.dragging = False

        self.canvas.bind("<Button-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.do_drag)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drag)

        save_button = tk.Button(root, text="Save Selection", command=self.save_selection)
        save_button.pack(pady=10)

    def start_drag(self, event):
        if abs(event.x - self.end_x) < 10 and abs(event.y - self.end_y) < 10:
            self.dragging = True

    def do_drag(self, event):
        if self.dragging:
            new_size = min(event.x - self.start_x, event.y - self.start_y)
            new_size = max(10, new_size)  # prevent too small
            self.end_x = self.start_x + new_size
            self.end_y = self.start_y + new_size
            self.canvas.coords(self.rect, self.start_x, self.start_y, self.end_x, self.end_y)

    def stop_drag(self, event):
        self.dragging = False

    def save_selection(self):
        crop_box = (self.start_x, self.start_y, self.end_x, self.end_y)
        cropped = self.original_image.crop(crop_box)

        # Ask for output resolution
        res_win = tk.Toplevel(self.root)
        res_win.title("Output Resolution")

        tk.Label(res_win, text="Output resolution (e.g., 512):").pack()
        res_entry = tk.Entry(res_win)
        res_entry.pack()
        res_entry.insert(0, "512")

        def do_save():
            resolution = int(res_entry.get())
            resized = cropped.resize((resolution, resolution), Image.LANCZOS)
            save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[("PNG files", "*.png")])
            if save_path:
                resized.save(save_path)
            res_win.destroy()

        tk.Button(res_win, text="Save", command=do_save).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = SquareCropperApp(root)
    root.mainloop()

