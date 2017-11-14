from skimage import data, io, morphology
from skimage.color import rgb2hsv, hsv2rgb, rgb2gray
from pylab import *
from skimage.morphology import square
import skimage as si
import numpy as np
from numpy import array
import matplotlib.pyplot as pl

#opencv find contour

def show(*args):
    #Show multiple images in a row
    pl.figure(figsize=(20,12))
    for i,img in enumerate(args):
        pl.subplot(1, len(args), i+1)
        io.imshow(img)
#plt.show() 

if __name__ == '__main__':
    figure(figsize=(15,4))
    io.imshow(io.imread('/media/student/B/FLS/Studia/KCK/samoloty/samolot00.jpg'))
	eroded = morphology.erosion(arr, square(3))
	morphology.dilation(eroded, square(3))
coins = data.coins()
binary = coins > 150
show(coins, binary)
eroded = Image(morphology.erosion(binary, square(3)))
show(binary, eroded)
dilated = Image(morphology.dilation(binary, square(3)))
show(binary, dilated)
dilated = Image(morphology.dilation(binary, square(5)))
eroded = Image(morphology.erosion(dilated, square(5)))
show(binary, dilated, eroded)
result = eroded
opened = morphology.opening(result, square(2))
show(result, opened)
horse = rgb2gray(255 - data.horse()) > 0.5

count = 3
eroded = horse
for i in range(count):
    eroded = morphology.erosion(eroded, square(5))

dilated = eroded
for i in range(count):
    dilated = morphology.dilation(dilated, square(5))

show(horse, eroded, dilated)


horse = rgb2gray(255 - data.horse()) > 0.5

count = 3
dilated = horse
for i in range(count):
    dilated = morphology.dilation(dilated, square(5))

eroded = dilated
for i in range(count):
    eroded = morphology.erosion(eroded, square(5))

show(horse, dilated, eroded)





