import cv2
import math
import numpy as np
from sys import argv
from lib import sauvola, linelocalization, astar
from time import time as timer


def draw_line(im, path):
    for p in path:
        im[p[0], p[1]] = 0


def draw_map(im, map):
    for m in map:
        im[m[0], m[1]] = 255


def print_path(path):
    print '\t# path: ' + str(path[::-1])


######################
# ------ MAIN ------ #
######################


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

    length = im.shape[1] - 1
    step = 2
    if (length) % step != 0:
        im_end = math.floor(length / step) * step
    else:
        im_end = length

    path = []
    immap = np.zeros((imbw.shape), dtype=np.int32)
    for key, index in enumerate(indexes):
        start = [index, 0]
        goal = [index, im_end]
        a = astar.Astar()
        begin_search = timer()
        print '\t# ' + str(key + 1) + '. ',
        print 'start: ' + str(start) + " - goal: " + str(goal),
        path, map = a.pathfind(imbw, start, goal, step)
        draw_line(imbw, path)
        draw_map(immap, map)
        print ' => path found in ' + str(timer() - begin_search) + ' s'

    imbw_filename = str.replace(filename, '.', '_bw.')
    imbw_filename = str.replace(imbw_filename, 'data', 'data/bw')
    print 'Saving image "' + imbw_filename + '"..\n'
    cv2.imwrite(imbw_filename, imbw)
    immap_filename = str.replace(imbw_filename, '_bw', '_map')
    cv2.imwrite(immap_filename, immap)

print ' - Elapsed time: ' + str((timer() - begin)) + ' s\n'
