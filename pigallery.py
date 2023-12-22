import config
import os
import random
import tkinter as tk
from typing import List
from PIL import Image, ImageTk

IMAGES_DIR: str = config.CONFIG['images_path']
IMAGE_NAMES: List[str] = os.listdir(IMAGES_DIR)

def create_window():
    window = tk.Tk()
    window.attributes('-fullscreen', True)
    window.configure(background='black')
    tk.Button(window, text='Quit', command=window.destroy).pack(side='right')

    return window


def update_image(index=None):
    '''
    Update the image displayed. By default, image is changed randomly every n seconds.
    If there is manual intervention, image does not change randomly until signal resets timer.
    '''
    global id

    if not index:
        idx = random.randint(0, len(IMAGE_NAMES)-1)
    else:
        window.after_cancel(id)
        idx = index

    image = Image.open(f'{IMAGES_DIR}/{IMAGE_NAMES[idx]}')
    width, height = image.size

    resized_image = image.copy().resize((int(width/3), int(height/3)))
    image = ImageTk.PhotoImage(resized_image)

    label.configure(image=image)
    label.image = image

    if not index:
        if id:
            window.after_cancel(id)
        id = window.after(5000, update_image)
    

def update_image_randomly(e):
    update_image()


def update_image_manually(e):
    update_image(1)
    

if __name__ == '__main__':
    id = None
    window = create_window()

    image = Image.open(f'{IMAGES_DIR}/{IMAGE_NAMES[0]}')
    width, height = image.size

    resized_image = image.copy().resize((int(width/3), int(height/3)))
    image = ImageTk.PhotoImage(resized_image)
    label = tk.Label(window, bg='black', image=image)
    label.pack()

    update_image()

    window.bind("1", update_image_randomly)
    window.bind("<Return>", update_image_manually)
    
    window.mainloop()