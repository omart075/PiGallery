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
    global idx

    if index is None:
        print("random")
        idx = random.randint(0, len(IMAGE_NAMES)-1)
    else:
        window.after_cancel(id)
        idx = index

    print(idx)

    image = Image.open(f'{IMAGES_DIR}/{IMAGE_NAMES[idx]}')
    width, height = image.size

    resized_image = image.copy().resize((int(width/3), int(height/3)))
    image = ImageTk.PhotoImage(resized_image)

    label.configure(image=image)
    label.image = image

    if index is None:
        if id:
            window.after_cancel(id)
        id = window.after(5000, update_image)
        print(f"Thread: {id}")
    

def update_image_randomly(e):
    update_image()


def update_image_back(e):
    global idx

    if idx == 0:
        idx = len(IMAGE_NAMES)-1
    else:
        idx -= 1

    update_image(idx)
    
def update_image_forward(e):
    global idx

    if idx == len(IMAGE_NAMES)-1:
        idx = 0
    else:
        idx += 1

    update_image(idx)
    

if __name__ == '__main__':
    id = None
    idx = 0
    window = create_window()

    image = Image.open(f'{IMAGES_DIR}/{IMAGE_NAMES[0]}')
    width, height = image.size

    resized_image = image.copy().resize((int(width/3), int(height/3)))
    image = ImageTk.PhotoImage(resized_image)
    label = tk.Label(window, bg='black', image=image)
    label.pack()

    update_image()

    window.bind("s", update_image_randomly)
    window.bind("a", update_image_back)
    window.bind("d", update_image_forward)
    
    window.mainloop()