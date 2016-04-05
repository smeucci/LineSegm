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
    for i in range(0, 1):
        ys = 200
        yg = 2600
        step = 5
        start = [indexes[i], ys]
        goal = [indexes[i], yg]  # im.shape[1]-1]
        a = astar.Astar()
        path, map = a.pathfind(imbw, start, goal)
        print '\t# path: ' + str(path[::-1])
        print map[indexes[i]-step:indexes[i]+step, ys:yg+2]

    imbw_filename = str.replace(filename, '.', '_bw.')
    imbw_filename = str.replace(imbw_filename, 'data', 'data/bw')
    print 'Saving image "' + imbw_filename + '"..\n'
    for p in path:
        imbw[p[0], p[1]] = 0

    cv2.imwrite(imbw_filename, imbw)
    cv2.imwrite('data/bw/test_map.jpg', map)

print ' - Elapsed time: ' + str((timer() - begin)) + ' s\n'
