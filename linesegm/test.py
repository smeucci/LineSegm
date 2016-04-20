
import cv2

filename = "data/1.jpg"

im = cv2.imread(filename, 0)
print im
dst = cv2.distanceTransform(im, cv2.DIST_L2, 3)
print dst
