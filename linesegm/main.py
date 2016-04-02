import cv2
from sys import argv
from lib import Sauvola
from lib import LineLocalization
from time import time as timer

start = timer()

filenames = argv
filenames.pop(0)

for filename in filenames:
    print 'Reading image ' + filename + '..'
    im = cv2.imread(filename, 0)

    print 'Thresholding image ' + filename + '..'
    sauvola = Sauvola()
    th = sauvola.binarize(im, [20, 20], 128, 0.3)

    print 'Localizing lines..'
    lineloc = LineLocalization()
    indexes = lineloc.localize(th)
    print indexes
    th[indexes, 0:th.shape[1]] = 1
    print 'Number of lines detected: ' + str(len(indexes))

    th_filename = str.replace(filename, '.', '_th.')
    th_filename = str.replace(th_filename, 'data', 'data/bw')
    print 'Saving image ' + th_filename + '..\n'
    cv2.imwrite(th_filename, th)


print ' - Elapsed time: ' + str((timer() - start)) + ' s\n'
