import nose.tools as nt
from linesegm import Sauvola
import cv2


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
    pass
