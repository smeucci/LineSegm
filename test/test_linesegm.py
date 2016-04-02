import nose.tools as nt
from linesegm import sauvola, linelocalization
import cv2
import numpy as np


def test_sauvola():
    filename = 'data/test.jpg'
    im = cv2.imread(filename, 0)

    th = sauvola.binarize(im, [20, 20], 128, 0.3)

    minval, maxval, minloc, maxloc = cv2.minMaxLoc(th)

    hist = cv2.calcHist([th], [0], None, [256], [0, 256])

    nt.assert_equal(th.dtype, 'uint8')
    nt.assert_equal(th.size, im.size)
    nt.assert_equal(minval, 0)
    nt.assert_equal(maxval, 255)
    nt.assert_equal(cv2.countNonZero(hist), 2)


def test_linelocalization():
    filename = 'data/test.jpg'
    im = cv2.imread(filename, 0)

    imbw = sauvola.binarize(im, [20, 20], 128, 0.3)

    indexes = linelocalization.localize(imbw)

    expected = [957, 1070, 1185, 1300, 1414, 1526, 1641, 1758, 1870, 1973,
                2077, 2195, 2307, 2414, 2524, 2633, 2742, 2849, 2960, 3072,
                3183, 3293, 3406]

    nt.assert_equal(type(indexes), type(expected))
    nt.assert_equal(max(indexes), max(expected))
    nt.assert_equal(min(indexes), min(expected))
    nt.assert_equal(len(indexes), len(expected))
    nt.assert_equal(np.mean(indexes), np.mean(expected))
    nt.assert_equal(np.std(indexes), np.std(expected))
