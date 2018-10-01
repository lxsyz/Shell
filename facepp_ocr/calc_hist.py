#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import cv2
from matplotlib import pyplot as plt
import numpy as np

img = cv2.imread("017.jpg", 0)

mask = np.zeros(img.shape[:2], np.uint8)
mask[62:331, 171:489] = 255
masked_img = cv2.bitwise_and(img, img, mask=mask)
# cv2.imshow("Original", image)


print img.shape
# img[img >= 220] = 255
# img[(img > 215) & (img < 230)] = 0
# img[(img < 130) & (img > 90)] = 0
plt.hist(img.ravel(),128,[0,256])
plt.show()
# img[img < 90] = 255

cv2.imwrite("11_histogram.jpg", img)
cv2.imshow("deal", img)

#图像直方图
hist_mask = cv2.calcHist([img], [0], None, [256], [0, 256])
# hist = cv2.calcHist([img], [0], None, [256], [0,256])
#
plt.figure()#新建一个图像
plt.title("Grayscale Histogram")#图像的标题
plt.xlabel("Bins")#X轴标签
plt.ylabel("# of Pixels")#Y轴标签
plt.plot(hist_mask)#画图
plt.xlim([0, 256])#设置x坐标轴范围
plt.show()#显示图像

hist, bins = np.histogram(img.flatten(), 256, [0, 256])  # img.flatten()将数组变为一维数组

cdf = hist.cumsum()  # 计算直方图
cdf_normalized = cdf * hist.max() / cdf.max()

cdf_m = np.ma.masked_equal(cdf, 0)
cdf_m = (cdf_m - cdf_m.min()) * 255 / (cdf_m.max() - cdf_m.min())
cdf = np.ma.filled(cdf_m, 0).astype('uint8')
img2 = cdf[img]

cv2.imwrite("11_histogram2.jpg", img2)
cv2.imshow('res', img2)
cv2.waitKey(0)

# for i,col in enumerate(color):
#     histr = cv2.calcHist([img],[i],mask,[256],[0,256])
#     plt.plot(histr,color = col)
#     plt.xlim([0,256])
# plt.show()