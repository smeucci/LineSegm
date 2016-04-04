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

    imbw[indexes, 0:imbw.shape[1]] = 1
    print ' => ' + str(len(indexes)) + ' lines detected.'

    print '- Path planning with A*..'
    for i in range(0, 1):
        start = [indexes[i], 0]
        goal = [indexes[i], 3]
        a = astar.Astar()
        path = a.pathfind(imbw, start, goal)
        print '\t# path: ' + str(path[::-1])

    imbw_filename = str.replace(filename, '.', '_bw.')
    imbw_filename = str.replace(imbw_filename, 'data', 'data/bw')
    print 'Saving image "' + imbw_filename + '"..\n'
    cv2.imwrite(imbw_filename, imbw)


print ' - Elapsed time: ' + str((timer() - begin)) + ' s\n'
