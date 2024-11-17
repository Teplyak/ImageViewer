from tkinter import *
from tkinter import ttk, messagebox, filedialog
import tkinter as tk
from PIL import Image, ImageTk, ImageOps
import os

window = Tk()
window.title("Image Viewer")
window.geometry("640x480")
thumbnail_size = (1024, 768)

file_types = [('JPG', '.jpg'), ('BMP', '.bmp')]
img = None
canvas = None
filename = None
window_title = "Image Viewer"
scale_factor = 1.0
coef = 2

def create_canvas():
    global img, canvas
    img_title = os.path.basename(img_path)
    title_text = f"{window_title} - {img_title} ({scale_factor}x) - В процессе"
    window.title(title_text)
    if canvas:
        canvas.destroy()
    
    if img is not None:
        canvas = tk.Canvas(
            window, 
            width=img.width(), 
            height=img.height(),
            xscrollcommand=scrollbar_x.set,
            yscrollcommand=scrollbar_y.set,
            scrollregion=(0, 0, img.width(), img.height())
        )
        canvas.create_image(0, 0, anchor='nw', image=img)
        canvas.pack(fill=BOTH, expand=True)

        scrollbar_x.config(command=canvas.xview)
        scrollbar_y.config(command=canvas.yview)
        window.title(title_text.replace(' - В процессе', ''))

def open_image():
    global img, img_path, scale_factor, original_img 
    scale_factor = 1.0
    img_path = filedialog.askopenfilename(title='Выберите изображение', filetypes=file_types)
    if not img_path == '':
        try:
            original_img = Image.open(img_path)
            original_img.thumbnail(thumbnail_size)
            print(f'Исходный размер изображения - {original_img.size}')
            img = ImageTk.PhotoImage(original_img)
            create_canvas()
        except:
            messagebox.showinfo("Ошибка", "Файл неверного формата или повреждён.")

def scale_func(func):
    global img, scale_factor, original_img
    previous_scale = scale_factor
    if original_img is not None:
        if func == "Увеличить":
            scale_factor *= coef
            if scale_factor > 8:
                scale_factor = 10.0
        elif func == 'Уменьшить':
            scale_factor /= coef
        elif func == 'Исходный размер':
            scale_factor = 1.0

        if scale_factor != previous_scale:
            scaled_img = ImageOps.scale(original_img, scale_factor)
            print(f'Текущий размер изображения - {scaled_img.size}')
            img = ImageTk.PhotoImage(scaled_img)
            
            print(f'Текущий масштаб - {scale_factor}x')
            create_canvas()

def display_help():
    messagebox.showinfo("Справка", "Меню \"Лупа\" представляет собой окно с тремя командами - \"Увеличить\", \"Уменьшить\" и \"Исходный размер\". В зависимости от того, какая команда была вызвана, произойдёт увеличение или уменьшение изображения в 2 раза относительно текущего размера, или возврат масштаба изображения к стандартному значению. Максимальный коэффициент приближения равен 10.")

def main():
    global scrollbar_x, scrollbar_y
    main_menu = Menu()
    file_menu = Menu(tearoff=0)
    file_menu.add_command(label="Увеличить", command=lambda:scale_func('Увеличить'))
    file_menu.add_command(label="Уменьшить", command=lambda:scale_func('Уменьшить'))
    file_menu.add_separator()
    file_menu.add_command(label="Исходный размер", command=lambda:scale_func('Исходный размер'))
    
    main_menu.add_cascade(label="Загрузить изображение", command=open_image)
    main_menu.add_cascade(label="Лупа", menu=file_menu)
    main_menu.add_cascade(label="Справка", command=display_help)

    window.config(menu=main_menu)

    scrollbar_x = ttk.Scrollbar(orient="horizontal")
    scrollbar_x.pack(side=BOTTOM, fill=X)
    scrollbar_y = ttk.Scrollbar(orient="vertical")
    scrollbar_y.pack(side=RIGHT, fill=Y)

    window.mainloop()

main()