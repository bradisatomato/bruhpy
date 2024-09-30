from pathlib import Path
import sys
import struct
import tkinter as tk
from PIL import Image, ImageTk
import numpy as np

TEMP_RESULT_PATH = "temp.png"

def vec_to_u32_ne(bytes):
    return struct.unpack('<I', bytes)[0]

def png_to_bruh(path):
    img = Image.open(path)
    img = img.convert("RGBA")
    width, height = img.size
    pixels = np.array(img)

    hex_colors = []
    for y in range(height):
        for x in range(width):
            r, g, b, _ = pixels[y, x]
            hex_color = f"{r:02x}{g:02x}{b:02x}"
            hex_colors.append(hex_color)

    path_to_bruh = path.with_suffix(".bruh")
    
    with open(path_to_bruh, "wb") as f:
        f.write(struct.pack('<II', width, height))
        f.write(''.join(hex_colors).encode('utf-8'))

    print("Successfully converted PNG to BRUH")

def bruh_to_png(path):
    with open(path, "rb") as f:
        width, height = struct.unpack('<II', f.read(8))
        hex_string = f.read().decode('utf-8').replace('\n', '')
    
    pixels = [tuple(int(hex_string[i:i+2], 16) for i in range(j, j + 6, 2)) for j in range(0, len(hex_string), 6)]
    image = Image.new("RGBA", (width, height))
    
    for i, color in enumerate(pixels):
        image.putpixel((i % width, i // width), (*color, 255))
    
    image.save(TEMP_RESULT_PATH, "PNG")
    return width, height

class ImagePreviewApp:
    def __init__(self, master, img_path):
        self.master = master
        self.master.title("Image Preview")
        self.image = Image.open(img_path)
        self.image = self.image.resize((self.image.width, self.image.height))
        self.img_tk = ImageTk.PhotoImage(self.image)

        self.label = tk.Label(master, image=self.img_tk)
        self.label.image = self.img_tk
        self.label.pack()

def main():
    root = tk.Tk()
    
    args = sys.argv
    if args[1] == "compile":
        if len(args) < 3:
            raise ValueError("Secondary argument ('path') not provided. Example: `python script.py compile ~/image.png`")
        
        path = Path(args[2])
        png_to_bruh(path)

    else:
        file_path = Path(args[1])
        width, height = bruh_to_png(file_path)
        print(f"{width} {height}")
        app = ImagePreviewApp(root, TEMP_RESULT_PATH)
        root.geometry(f"{width}x{height}")
        root.mainloop()
