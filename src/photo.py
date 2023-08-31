#!/usr/bin/python3

import glob
import tkinter as tk
from PIL import Image, ImageTk

class Frame(tk.Frame):

    interval_time = 5 * 60;
    
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.show_photo()
        
    def show_photo(self):
        self.photos = self.get_images()
        self.photo_index = 0
        self.photo = ImageTk.PhotoImage(self.photos[self.photo_index])
        self.photo_label = tk.Label(self, image = self.photo)
        self.photo_label.bind("<Button-1>", self.next_photo)
        self.photo_label.after(1000 * self.interval_time, self.next_photo)
        self.photo_label.pack()
        
        
    def get_images(self):
        image_files = glob.glob("../photos/*")
        images = []
        for image_file in image_files:
            image = Image.open(image_file)
            image = image.resize((400, 240))
            images.append(image)
        return images

    def next_photo(self, event = None):
        self.photo_index = (self.photo_index + 1) % len(self.photos)
        self.photo = ImageTk.PhotoImage(self.photos[self.photo_index])
        self.photo_label.configure(image = self.photo)
        self.photo_label.after(1000 * self.interval_time, self.next_photo)
