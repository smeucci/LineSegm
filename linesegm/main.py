import cv2
import numpy as np
from sys import argv
from lib import sauvola, linelocalization, astar
from time import time as timer


begin = timer()

filenames = argv
filenames.pop(0)

print '\n############################'
print '##    Line Segmentation   ##'
print '############################\n'

for filename in filenames:
    print 'Reading image "' + filename + '"..'
    im = cv2.imread(filename, 0)

    print '- Thresholding image..'
    imbw = sauvola.binarize(im, [20, 20], 128, 0.3)

    print '- Localizing lines..',
    indexes = linelocalization.localize(imbw)

    print ' => ' + str(len(indexes)) + ' lines detected.'

    print '- Path planning with A*..'
    path = []
    for i in range(0, 1):
        start = [indexes[i], 0]
        goal = [indexes[i], 1400]  # im.shape[1]-1]
        a = astar.Astar()
        path, map = a.pathfind(imbw, start, goal)
        print '\t# path: ' + str(path[::-1])

    for p in path:
        imbw[p[0], p[1]] = 0

    immap = np.zeros((imbw.shape), dtype=np.int32)
    for m in map:
        immap[m[0], m[1]] = 255

    imbw_filename = str.replace(filename, '.', '_bw.')
    imbw_filename = str.replace(imbw_filename, 'data', 'data/bw')
    print 'Saving image "' + imbw_filename + '"..\n'
    cv2.imwrite(imbw_filename, imbw)
    immap_filename = str.replace(imbw_filename, '_bw', '_map')
    cv2.imwrite(immap_filename, immap)

print ' - Elapsed time: ' + str((timer() - begin)) + ' s\n'
