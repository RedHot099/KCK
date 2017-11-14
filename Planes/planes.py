import numpy as np
import skimage.filters as filters
from skimage import data, io,feature
from skimage.morphology import disk
from skimage.filters.rank import median
from matplotlib import pyplot as plt
import skimage.morphology as morph

image = data.load('/media/student/B/FLS/Studia/KCK/samoloty/samolot00.jpg') # 00-20 /home/paulina/.local/lib/python2.7/site-packages/skimage/data/samolot00.jpg

#med = median(image, disk(5))
#image = filters.gaussian(image, sigma=1, multichannel=True, mode='reflect')

print(image)
#edges = filters.sobel(image)
#edges2 = feature.canny(im, sigma=3)
#dilation(image, square(3))
#morph.erosion(image, morph.square(3))
io.imshow(image)
plt.show() 
