import numpy as np
from tkinter import *
from tkinter import filedialog
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


        ### Settings
        self.setting_frame = LabelFrame(self.tk, text='General Settings')
        self.setting_frame.grid(row = 0, column = 0, sticky = W, padx=5, pady=5)

        ### Number of Candles slider
        self.N = NUM_CANDLES_0
        self.num_candles = Scale(self.setting_frame, from_=1, to=300, orient=HORIZONTAL, label='Num Candles', length=300, command=self.update_N)
        self.num_candles.set(NUM_CANDLES_0)
        self.num_candles.pack()

        ### Flickering variable
        self.var_flickering = IntVar(value=FLICKERING_0)
        self.flickering_button = Checkbutton(self.setting_frame, text = "Flickering", variable = self.var_flickering, command=self.update_flickering)
        self.flickering_button.pack()

        ### Mode variable
        self.mode_frame = LabelFrame(self.setting_frame, text='Mode')
        self.mode_frame.pack()
        self.var_mode=IntVar()
        self.var_mode.set(2)
        self.r0=Radiobutton(self.mode_frame , text="Single Color" , variable=self.var_mode , value=MODE_DICT['Single Color'] , command=self.update_mode).grid(column=0,row=1, sticky='W')
        self.r1=Radiobutton(self.mode_frame , text="Two Colors"   , variable=self.var_mode , value=MODE_DICT['Two Colors'] , command=self.update_mode).grid(column=0,row=2, sticky='W')
        self.r2=Radiobutton(self.mode_frame , text="Rainbow"      , variable=self.var_mode , value=MODE_DICT['Rainbow'] , command=self.update_mode).grid(column=0,row=3, sticky='W')

        ### Rainbow settings
        self.rb_frame = LabelFrame(self.tk, text='Rainbow Settings')
        self.rb_frame.grid(row=1,column=0, padx=5,pady=5, sticky='W')
        self.rainbow_velocity = Scale(self.rb_frame, from_=5, to=120, orient=HORIZONTAL, label='Time Period', length=300, command=self.update_rb_velocity)
        self.rainbow_velocity.set(RAINBOW_VELOCITY_0)
        self.rainbow_velocity.pack()
        self.rainbow_offset = Scale(self.rb_frame, from_=0, to=20, orient=HORIZONTAL, label='Candle-to-Candle Offset', length=300, command=self.update_rb_offset)
        self.rainbow_offset.set(RAINBOW_OFFSET_0)
        self.rainbow_offset.pack(side=LEFT)

        ### Color Selector
        self.cs_frame = LabelFrame(self.tk, text='Color Selector')
        self.cs_frame.grid(row=0,column=1, padx=5,pady=5, sticky='W', rowspan=2)
        self.slider_h = Scale(self.cs_frame, from_=0, to=1, orient=HORIZONTAL, label='HSL H', length=300, command=self.update_color_selector, resolution=.01)
        self.slider_s = Scale(self.cs_frame, from_=0, to=1, orient=HORIZONTAL, label='HSL S', length=300, command=self.update_color_selector, resolution=.01)
        self.slider_l = Scale(self.cs_frame, from_=0, to=1, orient=HORIZONTAL, label='HSL L', length=300, command=self.update_color_selector, resolution=.01)
        self.slider_h.grid(row=0,column=1, padx=5,pady=5)
        self.slider_s.grid(row=1,column=1, padx=5,pady=5)
        self.slider_l.grid(row=2,column=1, padx=5,pady=5)
        self.slider_h.set(0)
        self.slider_s.set(1)
        self.slider_l.set(.5)
        self.color_preview_canvas=Canvas(self.cs_frame, width=100, height=100, bg='white')
        self.color_preview_canvas.grid(row=3,column=1, padx=10, pady=10)
        self.color_hex = Label(self.cs_frame)
        self.color_hex.grid(row=4,column=1)
        self.update_color_selector()

        self.c1_canvas = Canvas(self.cs_frame, width=100, height=100, bg='white')
        self.c2_canvas = Canvas(self.cs_frame, width=100, height=100, bg='white')
        self.c1_canvas.grid(row=5,column=0, padx=10, pady=10)
        self.c2_canvas.grid(row=5,column=2, padx=10, pady=10)
        self.set_c1_button = Button(self.cs_frame, text='Set', command=self.update_C1)
        self.set_c1_button.grid(row=6,column=0)
        self.set_c2_button = Button(self.cs_frame, text='Set', command=self.update_C2)
        self.set_c2_button.grid(row=6,column=2)

        self.save_colors = Button(self.cs_frame, text='Save Colors', command=self.save_color_profile)
        self.save_colors.grid(row=7,column=0)
        self.load_colors = Button(self.cs_frame, text='Load Colors', command=self.load_color_profile)
        self.load_colors.grid(row=7,column=2)
        

        ### Candle Preview
        self.canvas = Canvas(self.tk, width=self.tk.winfo_screenwidth()-20, height=40, bg='white')
        self.canvas.grid(row=2,column=0, padx=10, pady=10, columnspan=2)


        self.state = False
        self.tk.bind("<F11>", self.toggle_fullscreen)
        self.tk.bind("<Escape>", self.end_fullscreen)
        self.tk.attributes("-fullscreen", self.state)

        self.tk.after(0,self.candle_preview)
        self.update_color_selector()
        self.update_C1()
        self.update_C2()

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
    def update_color_selector(self, val=0):
        h = self.slider_h.get()
        s = self.slider_s.get()
        l = self.slider_l.get()
        c = Color(hsl=(h,s,l))
        self.color_selector_c=c
        self.redraw_color_selectors()
    def update_C1(self):
        h = self.slider_h.get()
        s = self.slider_s.get()
        l = self.slider_l.get()
        c = Color(hsl=(h,s,l))
        self.set_C1(c)
    def set_C1(self,c):
        self.c1=c
        self.lc.c1 = c
        width = self.c1_canvas.winfo_width()
        height = self.c1_canvas.winfo_height()
        self.c1_canvas.create_rectangle(0,0,width, height, fill=self.c1.hex)
    def update_C2(self):
        h = self.slider_h.get()
        s = self.slider_s.get()
        l = self.slider_l.get()
        c = Color(hsl=(h,s,l))
        self.set_C2(c)
    def set_C2(self,c):
        self.c2=c
        self.lc.c2 =c
        width = self.c2_canvas.winfo_width()
        height = self.c2_canvas.winfo_height()
        self.c2_canvas.create_rectangle(0,0,width, height, fill=self.c2.hex)
    def redraw_color_selectors(self):
        width = self.color_preview_canvas.winfo_width()
        height = self.color_preview_canvas.winfo_height()
        self.color_preview_canvas.create_rectangle(0,0,width, height, fill=self.color_selector_c.hex)
        self.color_hex['text']=self.color_selector_c

    def save_color_profile(self):
        s=f'{self.c1},{self.c2}'
        with filedialog.asksaveasfile(defaultextension='.colorprofile') as f:
            f.write(s)
        
    def load_color_profile(self):
        with filedialog.askopenfile(defaultextension='.colorprofile') as f:
            s=f.read()
        if s!=None:
            s=s.split(',')
            c1=Color(s[0])
            c2=Color(s[1])
            self.set_C1(c1)
            self.set_C2(c2)




if __name__ == '__main__':
    w = Fullscreen_Window()
    w.tk.mainloop()
