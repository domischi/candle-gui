import numpy as np
from tkinter import *
from tkinter.ttk import Combobox
import tkinter.ttk as ttk
from tkinter.colorchooser import *
from colour import Color
import time
from itertools import cycle, islice

RAINBOW_OFFSET_0 = 5
RAINBOW_VELOCITY_0 = 10
FLICKERING_0 = False
UPDATE_SPEED = 200
NUM_CANDLES_0 = 15
MODE_DICT = {'Single Color': 0, 'Two Colors' : 1, 'Rainbow': 2}

class LightControl:
    def __init__(self, N=NUM_CANDLES_0):
        self.N = N

        self.mode = MODE_DICT['Rainbow'] ## Rainbow
        self.c1 = Color('white') ## For single color use
        self.c2 = Color('white') ## For dual color use
        self.rainbow_time_periodicity = RAINBOW_VELOCITY_0  ## How fast the system loops through the rainbow (in seconds)
        self.rainbow_color_shift_per_candle = RAINBOW_OFFSET_0/100. ## How much the rainbow color changes from one candle to the next, in degrees of a HSL scheme (360 is the full spectrum)

        self.flickering = FLICKERING_0

    def get_rainbow_pattern(self):
        t=time.time()
        c0_angle = (t % self.rainbow_time_periodicity)/self.rainbow_time_periodicity
        angles = [ (c0_angle+i*self.rainbow_color_shift_per_candle) % 1 for i in range(self.N)]
        return [Color(hsl=(a,.8,.5)) for a in angles]

    def get_flickering_pattern(self):
        intensities =  [ .5, .8 , 1.]
        probabilites = [.01, .89, .1]
        return np.random.choice(intensities, p=probabilites, size = self.N)
    def generate_light_pattern(self):
        if self.flickering:
            intensity = self.get_flickering_pattern();
        else:
            intensity = [1.]*self.N
        if self.mode == MODE_DICT['Rainbow']:
            color = self.get_rainbow_pattern()
        elif self.mode == MODE_DICT['Single Color']:
            color = [self.c1] * self.N
        elif self.mode == MODE_DICT['Two Colors']:
            color = list(islice(cycle([self.c1, self.c2]), self.N))
        color = [c.rgb for c in color]
        out = [Color(rgb=[r*i for r in c]) for c, i in zip(color, intensity)]
        return out
    def pprint(self):
        out=self.generate_light_pattern()
        for o in out:
            print(o)
