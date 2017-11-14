from skimage import data, io, morphology
from skimage.color import rgb2hsv, hsv2rgb, rgb2gray
from pylab import *
from skimage.morphology import square
import skimage as si
import numpy as np
from numpy import array
import matplotlib.pyplot as plt
import cv2

#opencv find contour

def process(img):
    imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #imgray = cv2.bilateralFilter(imgray,1,1,1)
    eroded = cv2.erode(imgray, np.ones((11, 11)) )
    dilated = cv2.dilate(eroded, np.ones((11, 11)) )
    

    edged = cv2.Canny(dilated,30,200)
    (cnts, hierarchy) = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for i in range(len(cnts)):
        if hierarchy[0][i][3]==-1:
            cv2.drawContours(img,[cnts[i]],-1,(0,255,0),3)
    return img

def show(args):
    #Show multiple images in a row
    fig = plt.figure(figsize=(20,len(args)*5))
    for i,img in enumerate(args):       
        ax = plt.subplot(len(args), 1, i+1)
	ax.set_axis_off()
        io.imshow(img)
	
    fig.savefig('my-planes.pdf')

#def process(img):
    #eroded = morphology.erosion(img, square(5))
    #dilated = morphology.dilation(eroded, square(5))
    #opened = morphology.opening(dilated, square(2))
    #count = 3
    #eroded = opened
    #for i in range(count):
    #    eroded = morphology.erosion(eroded, square(5))
    #dilated = eroded
    #for i in range(count):
    #    dilated = morphology.dilation(dilated, square(5))
    #img = rgb2gray(1 - dilated)
    #imgray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    #ret, thresh = cv2.threshold(imgray, 127, 255, 0)
    #img2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #return img2,contours

def get_number(n):
    return str(n//10) + str(n%10)

if __name__ == '__main__':    
    images = []
    for i in range(18):
        img = cv2.imread('/home/paulina/Desktop/Studia/KCK/Planes/samolot' + get_number(i) + '.jpg')
	images.append(process(img))
    show(images)
