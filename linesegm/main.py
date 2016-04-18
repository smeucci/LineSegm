import cv2
import numpy as np
from sys import argv
from lib import sauvola, linelocalization, pathfinder
from time import time as timer


def draw_line(im, path):
    for p in path:
        im[p[0], p[1]] = 0


def draw_map(im, map):
    for m in map:
        im[m[0], m[1]] = 255


def print_path(path):
    print '\t# path: ' + str(path[::-1])


def save(filename, imbw, immap):
    imbw_filename = str.replace(filename, '.', '_bw.')
    imbw_filename = str.replace(imbw_filename, 'data', 'data/bw')
    print 'Saving image "' + imbw_filename + '"..\n'
    cv2.imwrite(imbw_filename, imbw)
    immap_filename = str.replace(imbw_filename, '_bw', '_map')
    cv2.imwrite(immap_filename, immap)


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
    lines = linelocalization.localize(imbw)
    print ' => ' + str(len(lines)) + ' lines detected.'

    print '- Path planning with ',

    immap = np.zeros((imbw.shape), dtype=np.int32)
    # for i in range(0, 1):
    for line in lines:
        # line = lines[i]
        path, map = pathfinder.search(imbw, 'A', line)
        draw_line(imbw, path)
        draw_map(immap, map)
        # print_path(path)

    save(filename, imbw, immap)

print ' - Elapsed time: ' + str((timer() - begin)) + ' s\n'
