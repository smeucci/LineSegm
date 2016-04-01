import cv2
import numpy as np
import peakutils


a = cv2.imread('data/bw/test_th.jpg', 0)
a = abs(255-a)
a = a / 255
a = cv2.reduce(a, 1, cv2.REDUCE_SUM, dtype=cv2.CV_32F)
a = a.ravel()
max = max(a)
mean = np.mean(a)
std = np.std(a)
t = mean/max
# t = t + std/max
i = peakutils.indexes(a, thres=t, min_dist=100)
print i.shape
print i
aa = a[i]
print aa
m = np.mean(aa)
s = np.std(aa)
tr = m+s
loc = (aa > tr)
print loc
idx = 0
arr = []
for d, l in enumerate(loc):
    if bool(l) is True:
        arr.append(d)

i = np.delete(i, arr, axis=0)
print i
print aa[np.where(aa < tr)]
