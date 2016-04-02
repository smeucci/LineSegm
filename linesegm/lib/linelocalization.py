import cv2
import numpy as np
import peakutils


def localize(im):
    # invert bw image
    im = invert(im)
    # enhance the image with morphological operations
    im = enhance(im)
    # execute projection profile analysis to localize lines of text
    peaks = projection_analysis(im)
    # compute the valley bewteen each pair of consecutive peaks
    indexes = []
    for i in range(0, len(peaks)-1):
        dist = (peaks[i+1] - peaks[i]) / 2
        valley = peaks[i] + dist
        indexes.append(valley)

    return indexes


def invert(im):
    im = abs(255 - im)
    im = im / 255

    return im


def enhance(im):
    kernel = np.ones((5, 5), np.uint8)
    im = cv2.erode(im, kernel, iterations=1)
    kernel = np.ones((15, 15), np.uint8)
    im = cv2.dilate(im, kernel, iterations=1)

    return im


def projection_analysis(im):
    # compute the ink density histogram (sum each rows)
    hist = cv2.reduce(im, 1, cv2.REDUCE_SUM, dtype=cv2.CV_32F)
    hist = hist.ravel()
    # find peaks withing the ink density histogram
    max_hist = max(hist)
    mean_hist = np.mean(hist)
    thres_hist = mean_hist / max_hist
    peaks = peakutils.indexes(hist, thres=thres_hist, min_dist=50)
    # find peaks that are too high
    mean_peaks = np.mean(hist[peaks])
    std_peaks = np.std(hist[peaks])
    thres_peaks_high = mean_peaks + 1.5*std_peaks
    thres_peaks_low = mean_peaks - 3*std_peaks
    peaks = peaks[np.logical_and(hist[peaks] < thres_peaks_high,
                                 hist[peaks] > thres_peaks_low)]

    return peaks
