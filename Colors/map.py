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

def plot_color_map(params,data):

    column_width_pt = params[0]        # Show in latex using \the\linewidth
    pt_per_inch = 72
    size = column_width_pt / pt_per_inch

    fig, ax = plt.subplots(nrows=1, sharex=True, figsize=(size, 0.75 * size))
    img = np.zeros((params[0], params[1], 3))
    for i in range(1,params[0]):
	for j in range(params[1]):
		img[i,j]=gradient_hsv_gyr(data[i-1][j], data[i][j])

    im = ax.imshow(img, aspect='auto')
    im.set_extent([0,499, 498, 0])
    ax.tick_params(axis='both',direction='in', top=True,right=True)

    fig.savefig('my-map.pdf')

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

def gradient_hsv_gyr(left,v):
    h = 120 * (1 - v)
    if (left - v) < -0.01:
	return hsv2rgb(h,0.55,1)
    if (left - v) > 0.01:
	return hsv2rgb(h,1,0.65)
    return hsv2rgb(h,1,1)

def make_data():
    f = open('big.dem.txt')
    lines = f.readlines()
    data = []
    for line in lines:
    	line = line.split()
    	line = [float(i) for i in line] #changing the game values to floats
	data.append(line)
    return [int(p) for p in data[0]], data[1:]

def find_min_max(data):
    mins = []
    maxs = []
    for array in data:
	mins.append(min(array))
	maxs.append(max(array))
    return min(mins),max(maxs)

def normalize_data(data):
    mini, maxi = find_min_max(data)
    for j,line in enumerate(data):
	for i,number in enumerate(line):
		line[i] = (number - mini)/(maxi-mini)
    return data

if __name__ == '__main__':
    params, data = make_data()
    data = normalize_data(data)
    plot_color_map(params,data)

