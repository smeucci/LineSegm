import cv2
import numpy as np
from sys import argv
from lib import sauvola, linelocalization, pathfinder
from time import time as timer


filename = 'data/test3.jpg'

print 'Reading image "' + filename + '"..'
im = cv2.imread(filename, 0)

print '- Thresholding image..'
imbw = sauvola.binarize(im, [20, 20], 128, 0.3)

imbw = cv2.medianBlur(imbw, 1)

imbw_filename = str.replace(filename, '.', '_bw.')
imbw_filename = str.replace(imbw_filename, 'data', 'data/bw')
print 'Saving image "' + imbw_filename + '"..\n'
cv2.imwrite(imbw_filename, imbw)
