#!/usr/bin/python3

import tkinter as tk
import photo
import clock

class window(tk.Tk):
        
    def __init__(self):
        super().__init__()
        self.geometry("800x480")
        self.frames = [
            photo.Frame(self, width = 400, height = 240),
            clock.Frame(self, width = 400, height = 240)
        ]        
        
        self.bind("<Button-1>", self.before_switch)
        self.bind("<B1-Motion>", self.switch_function)
        
        self.frame_index = 0
        self.frames[self.frame_index].pack()

    def before_switch(self, event):
        self.last_x = event.x
        self.start_motion = True
        
    def switch_function(self, event):        
        if not self.start_motion:
            return
        self.start_motion = False
        self.frames[self.frame_index].pack_forget()
        if event.x > self.last_x:
            self.function_index = (self.function_index + 1) % len(self.functions)
        elif event.x < self.last_x:
            self.function_index = (self.function_index - 1 + len(self.functions)) % len(self.functions)
        self.frames[self.frame_index].pack()            
