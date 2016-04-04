import cv2
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
    for i in range(1, 2):
        start = [indexes[i], 0]
        # goal = [indexes[i], 1110]  # im.shape[1]-1]
        a = astar.Astar()
        step = im.shape[1] / 15
        for t in range(0, 15):
            tmp_start = [start[0], start[1] + t*step]
            tmp_goal = [start[0], start[1] + step + step*t]
            path += a.pathfind(imbw, tmp_start, tmp_goal)

        print '\t# path: ' + str(path[::-1])

    imbw_filename = str.replace(filename, '.', '_bw.')
    imbw_filename = str.replace(imbw_filename, 'data', 'data/bw')
    print 'Saving image "' + imbw_filename + '"..\n'
    for p in path:
        imbw[p[0], p[1]] = 0

    cv2.imwrite(imbw_filename, imbw)


print ' - Elapsed time: ' + str((timer() - begin)) + ' s\n'
