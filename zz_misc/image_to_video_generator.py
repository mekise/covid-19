import cv2
import numpy as np
import glob
import sys, os

img_array = []
for filename in sorted(glob.glob('./fig/*.png')):
	img = cv2.imread(filename)
	height, width, layers = img.shape
	size = (width,height)
	img_array.append(img)

out = cv2.VideoWriter('covid_animation.avi',cv2.VideoWriter_fourcc(*'DIVX'), 4, size)
 
for i in range(len(img_array)):
    out.write(img_array[i])
out.release()