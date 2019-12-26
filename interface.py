import numpy as np
from tkinter import *
from tkinter.ttk import Combobox
import tkinter.ttk as ttk
from tkinter.colorchooser import *
from colour import Color
import time
from lightcontrol import *

class Fullscreen_Window:
    def __init__(self):
        self.tk = Tk()
        self.tk.attributes('-zoomed', True)  # This just maximizes it so we can see the window. It's nothing to do with fullscreen.

        ## Light Control Module
        self.lc = LightControl()

        self.setting_frame = LabelFrame(self.tk, text='Settings')
        self.setting_frame.pack(side=LEFT)

        ## Settings
        ## Number of Candles slider
        self.N = NUM_CANDLES_0
        self.num_candles = Scale(self.setting_frame, from_=1, to=300, orient=HORIZONTAL, label='Num Candles', length=300, command=self.update_N)
        self.num_candles.set(NUM_CANDLES_0)
        self.num_candles.pack()

        ## Flickering variable
        self.var_flickering = IntVar(value=FLICKERING_0)
        self.flickering_button = Checkbutton(self.setting_frame, text = "Flickering", variable = self.var_flickering, command=self.update_flickering)
        self.flickering_button.pack()

        ## Mode variable
        self.mode_frame = LabelFrame(self.setting_frame, text='Mode')
        self.mode_frame.pack()
        self.var_mode=IntVar()
        self.var_mode.set(2)
        self.r0=Radiobutton(self.mode_frame , text="Single Color" , variable=self.var_mode , value=MODE_DICT['Single Color'] , command=self.update_mode).grid(column=0,row=1, sticky='W')
        self.r1=Radiobutton(self.mode_frame , text="Two Colors"   , variable=self.var_mode , value=MODE_DICT['Two Colors'] , command=self.update_mode).grid(column=0,row=2, sticky='W')
        self.r2=Radiobutton(self.mode_frame , text="Rainbow"      , variable=self.var_mode , value=MODE_DICT['Rainbow'] , command=self.update_mode).grid(column=0,row=3, sticky='W')

        ## Rainbow settings
        self.rb_frame = LabelFrame(self.setting_frame, text='Rainbow Settings')
        self.rb_frame.pack()
        self.rainbow_velocity = Scale(self.rb_frame, from_=5, to=120, orient=HORIZONTAL, label='Time Period', length=300, command=self.update_rb_velocity)
        self.rainbow_velocity.set(RAINBOW_VELOCITY_0)
        self.rainbow_velocity.pack()
        self.rainbow_offset = Scale(self.rb_frame, from_=0, to=20, orient=HORIZONTAL, label='Candle-to-Candle Offset', length=300, command=self.update_rb_offset)
        self.rainbow_offset.set(RAINBOW_OFFSET_0)
        self.rainbow_offset.pack(side=LEFT)


        ## Candle Preview
        self.canvas = Canvas(self.tk, width=self.tk.winfo_screenwidth()-200, height=40, bg='white')
        self.canvas.pack(side=LEFT, padx=10, pady=10)


        self.state = False
        self.tk.bind("<F11>", self.toggle_fullscreen)
        self.tk.bind("<Escape>", self.end_fullscreen)
        self.tk.attributes("-fullscreen", self.state)

        self.tk.after(0,self.candle_preview)

    def toggle_fullscreen(self, event=None):
        self.state = not self.state  # Just toggling the boolean
        self.tk.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.tk.attributes("-fullscreen", False)
        return "break"

    def candle_preview(self):
        cs = self.lc.generate_light_pattern()
        total_width = self.canvas.winfo_width()
        total_heigth = self.canvas.winfo_height()
        wbox = total_width / self.N
        for i, c in enumerate(cs):
            self.canvas.create_rectangle(i*wbox,0,(i+1)*wbox-1,total_heigth, fill=c.hex)
        self.tk.after(UPDATE_SPEED,self.candle_preview)

    def update_N(self, val):
        val=int(val)
        self.N=val
        self.lc.N=val
    def update_flickering(self):
        self.lc.flickering = bool(self.var_flickering.get())
    def update_rb_velocity(self,val):
        val=int(val)
        self.lc.rainbow_time_periodicity=val
    def update_rb_offset(self,val):
        val=int(val)
        self.lc.rainbow_color_shift_per_candle=val/100
    def update_mode(self):
        val=self.var_mode.get()
        self.lc.mode=val


if __name__ == '__main__':
    w = Fullscreen_Window()
    w.tk.mainloop()
