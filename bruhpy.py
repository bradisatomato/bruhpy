import backend
from tkinter import *
from tkinter import filedialog
root = Tk()

def pngtobruhc():
    png = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
    backend.png_to_bruh(backend.Path(png))

def openbruhc():
    bruh = filedialog.askopenfilename(filetypes=[("BRUH files", "*.bruh")])
    width, height = backend.bruh_to_png(backend.Path(bruh))
    img = backend.ImagePreviewApp(root, backend.TEMP_RESULT_PATH)
    root.geometry(f"{width}x{height}")


root.title("bruhpy")
root.iconbitmap("./face-hh.ico")

pngtobruh = Button(root, text="PNG -> BRUH", command=pngtobruhc)
pngtobruh.pack()

openbruh = Button(root, text="Open BRUH", command=openbruhc)
openbruh.pack()

root.mainloop()