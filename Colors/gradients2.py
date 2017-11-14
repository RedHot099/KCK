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
        img = np.zeros((2, 1024, 3))
        for i, v in enumerate(np.linspace(0, 1, 1024)):
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
    return (v, v, v)

def gradient_rgb_gbr(v):
    if v <= 0.5:
	r,g,b = (0, 1-2*v, 2*v)
    else:
	r,g,b = (2*v+0.01, 0, 2*(1-v))
    return (r, g, b)


def gradient_rgb_gbr_full(v):
    if v == 1:
	return (1,0,0)
    choice = math.floor(v*4)
    options = {
            0: (0,1,4 * v),
            1: (0,4 * (0.5-v),1),
            2: (-4 * (0.5-v),0,1),
            3: (1,0,4 * (1-v)),
    }
    return options[choice]


def gradient_rgb_wb_custom(v):
    r=b=g=0
    if v == 1:
	return (r,g,b)
    choice = math.floor(v*7)
    options = {
            0: (1,-v * 7+1,1),
            1: (-v * 7+2,g,1),
            2: (r,v * 7-2,1),
            3: (r,1,-v * 7+4),
	    4: (v * 7-4,1,b),
	    5: (1,-v * 7+6,b),
	    6: (-v * 7+7,g,b),
    }
    return options[choice]

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
    s = 1 - v
    b = 1
    return hsv2rgb(h,s,b)


if __name__ == '__main__':
    def toname(g):
        return g.__name__.replace('gradient_', '').replace('_', '-').upper()

    gradients = (gradient_rgb_bw, gradient_rgb_gbr, gradient_rgb_gbr_full, gradient_rgb_wb_custom,
                 gradient_hsv_bw, gradient_hsv_gbr, gradient_hsv_unknown, gradient_hsv_custom)

    plot_color_gradients(gradients, [toname(g) for g in gradients])
