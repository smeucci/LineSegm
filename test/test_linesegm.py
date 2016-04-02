import nose.tools as nt
from linesegm import Sauvola
from linesegm import LineLocalization
import cv2
import numpy as np


def test_sauvola():
    filename = 'data/test.jpg'
    img = cv2.imread(filename, 0)

    sauvola = Sauvola()
    th = sauvola.binarize(img, [20, 20], 128, 0.3)

    minval, maxval, minloc, maxloc = cv2.minMaxLoc(th)

    hist = cv2.calcHist([th], [0], None, [256], [0, 256])

    nt.assert_equal(th.dtype, 'uint8')
    nt.assert_equal(th.size, img.size)
    nt.assert_equal(minval, 0)
    nt.assert_equal(maxval, 255)
    nt.assert_equal(cv2.countNonZero(hist), 2)


def test_linelocalization():
    filename = 'data/test.jpg'
    img = cv2.imread(filename, 0)

    sauvola = Sauvola()
    th = sauvola.binarize(img, [20, 20], 128, 0.3)

    lineloc = LineLocalization()
    indexes = lineloc.localize(th)

    expected = [959, 1069, 1183, 1297, 1410, 1533, 1654, 1758, 1862,
                1972, 2076, 2197, 2311, 2411, 2521, 2630, 2739, 2847,
                2957, 3072, 3181, 3292, 3406]

    nt.assert_equal(type(indexes), type(expected))
    nt.assert_equal(max(indexes), max(expected))
    nt.assert_equal(min(indexes), min(expected))
    nt.assert_equal(len(indexes), len(expected))
    nt.assert_equal(np.mean(indexes), np.mean(expected))
    nt.assert_equal(np.std(indexes), np.std(expected))
