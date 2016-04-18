
from lib import sauvola
import cv2

filename = "data/test.jpg"

im = cv2.imread(filename, 0)

print '- Thresholding image..'
imbw = sauvola.binarize(im, [20, 20], 128, 0.3)

imbw_filename = str.replace(filename, '.', '_bw.')
imbw_filename = str.replace(imbw_filename, 'data', 'data/bw')
print 'Saving image "' + imbw_filename + '"..\n'
cv2.imwrite(imbw_filename, imbw)
