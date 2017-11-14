#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division             # Division in Python 2.7
import matplotlib
matplotlib.use('Agg')                       # So that we can render files without GUI
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
import math

from matplotlib import colors

GRADIENT_LEN = 1024

RGBcolors = {
    'b': (0,0,0),
    'i': (0,0,1), #indigo
    'g': (0,1,0),
    'c': (0,1,1),
    'r': (1,0,0),
    'm': (1,0,1),
    'y': (1,1,0),
    'w': (1,1,1),
}

def get_color_diff(c1,c2):
    rgb1 = RGBcolors[c1]
    rgb2 = RGBcolors[c2]
    return [rgb2[0]-rgb1[0],rgb2[1]-rgb1[1],rgb2[2]-rgb1[2]]

def normalize_values(c1,c2,n):
    diff = get_color_diff(c1,c2)
    rgb = list(RGBcolors[c1])
    for i in range(3):
	if diff[i] != 0:
            if diff[i] == 1:
		rgb[i]=n
	    else:
		rgb[i]=1-n
    return tuple(rgb)
    
    

def get_RGBvalues (colors,v):
    interval = 1.0 / (len(colors)-1)
    print("\n INTERVAL: " + str(interval))
    mini = 0
    idc = 0
    while v > mini + interval:
        mini += interval
        idc += 1
    maxi = mini + interval
    if idc == len(colors)-1:
        idc -= 1
    print("idc " + str(idc) + ": " + colors[idc])
    print("v " + str(v))
    normalizer = (v - mini)/(maxi - mini)
    return normalize_values(colors[idc],colors[idc+1], normalizer)
    
HSVcolors = {
    #TODO include black and white colors in hsv
    #'b': (0,0,0),
    #'w': (0,0,100),
    'r': (0,100,100),
    'y': (60,100,100),
    'g': (120,100,100),
    'c': (180,100,100),
    'i': (240,100,100),
    'm': (300,100,100),
}


def plot_color_gradients(gradients, names):
    # For pretty latex fonts (commented out, because it does not work on some machines)
    #rc('text', usetex=True) 
    #rc('font', family='serif', serif=['Times'], size=10)
    rc('legend', fontsize=10)

    column_width_pt = 400         # Show in latex using \the\linewidth
    pt_per_inch = 72
    size = column_width_pt / pt_per_inch

    fig, axes = plt.subplots(nrows=len(gradients), sharex=True, figsize=(size, 0.75 * size))
    fig.subplots_adjust(top=1.00, bottom=0.05, left=0.25, right=0.95)


    for ax, gradient, name in zip(axes, gradients, names):
        # Create image with two lines and draw gradient on it
        img = np.zeros((2, GRADIENT_LEN, 3))
        for i, v in enumerate(np.linspace(0, 1, GRADIENT_LEN)):
            img[:, i] = gradient(v)

        im = ax.imshow(img, aspect='auto')
        im.set_extent([0, 1, 0, 1])
        ax.yaxis.set_visible(False)

        pos = list(ax.get_position().bounds)
        x_text = pos[0] - 0.25
        y_text = pos[1] + pos[3]/2.
        fig.text(x_text, y_text, name, va='center', ha='left', fontsize=10)

    fig.savefig('my-gradients.pdf')

def hsv2rgb(h, s, v):
    if v==0:
        return 0,0,0
    else:
        c = v * s
	x = c * (1-abs((h/60)%2 -1))
	m = v - c
        
	choice = math.floor(h/60)
        options = {
            0: (c,x,0),
            1: (x,c,0),
            2: (0,c,x),
            3: (0,x,c),
            4: (x,0,c),
            5: (c,0,x),
        }
	r,g,b = options[choice]
	return ((r+m), (g+m), (b+m))

def gradient_rgb_bw(v):
    colors = ['b','w']
    r,g,b = get_RGBvalues(colors,v)
    return (r,g,b)

def gradient_rgb_gbr(v):
    colors = ['g','i','r']
    return get_RGBvalues(colors,v)

def gradient_rgb_gbr_full(v):
    colors = ['g','c','i','m','r']
    return get_RGBvalues(colors,v)


def gradient_rgb_wb_custom(v):
    colors = ['w','m','i','c','g','y','r','b']
    return get_RGBvalues(colors,v)

def gradient_hsv_bw(v):
    return hsv2rgb(0, 0, v)

def gradient_hsv_gbr(v):
    h = (v * 240 + 120) % 360
    return hsv2rgb(h,1,1)

def gradient_hsv_unknown(v):
    h = 120 * (1-v)
    return hsv2rgb(h, 0.5, 1)

def gradient_hsv_custom(v):
    h = (360 * v)%360
    return hsv2rgb(h,1-v,1)

if __name__ == '__main__':
    def toname(g):
        return g.__name__.replace('gradient_', '').replace('_', '-').upper()
    
    gradients = (gradient_rgb_bw, gradient_rgb_gbr, gradient_rgb_gbr_full, gradient_rgb_wb_custom,
                 gradient_hsv_bw, gradient_hsv_gbr, gradient_hsv_unknown, gradient_hsv_custom)

    plot_color_gradients(gradients, [toname(g) for g in gradients])
