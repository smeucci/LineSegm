import cv2
import numpy as np


def binarize(im, window, dr, k):
    # get the image dimensions
    rows, cols = im.shape
    # pad the image based on the window size
    impad = padding(im, window)
    # compute the mean and the squared mean
    mean, sqmean = integralMean(impad, rows, cols, window)
    # compute the variance and the standard deviation
    n = window[0] * window[1]
    variance = (sqmean - (mean**2) / n) / n
    # std = (sqmean - mean ** 2) ** 0.5
    std = variance ** 0.5
    # compute the threshold
    threshold = mean * (1 + k * (std / dr - 1))
    check_border = (mean >= 100)
    threshold = threshold * check_border
    # apply the threshold to the image
    output = np.array(255 * (im >= threshold), 'uint8')

    return output


def padding(im, window):
    pad = int(np.floor(window[0] / 2))
    im = cv2.copyMakeBorder(im, pad, pad, pad, pad, cv2.BORDER_CONSTANT)

    return im


def integralMean(im, rows, cols, window):
    # get the window size
    m, n = window
    # compute the integral images of im and im.^2
    sum, sqsum = cv2.integral2(im)
    # calculate the window area for each pixel
    isum = sum[m:rows + m, n:cols + n] + \
        sum[0:rows, 0:cols] - \
        sum[m:rows + m, 0:cols] - \
        sum[0:rows, n:cols + n]

    isqsum = sqsum[m:rows + m, n:cols + n] + \
        sqsum[0:rows, 0:cols] - \
        sqsum[m:rows + m, 0:cols] - \
        sqsum[0:rows, n:cols + n]
    # calculate the average values for each pixel
    mean = isum / (m * n)
    sqmean = isqsum / (m * n)

    return mean, sqmean


def ind2sub(ind, shape):
    row = ind / shape[1]
    col = ind % shape[1]

    return row, col
