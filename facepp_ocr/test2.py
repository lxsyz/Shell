#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from PIL import Image
import os
import cv2 as cv

threshold_value = 190

def binarize(img, target_file):
    # gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)  # 把输入图像灰度化
    # 直接阈值化是对输入的单通道矩阵逐像素进行阈值分割。
    ret, binary = cv.threshold(img, threshold_value, 255, cv.THRESH_BINARY)
    print("threshold value %s" % ret)
    res = Image.fromarray(binary)
    res.save(target_file)

img = cv.imread("017.jpg", 0)
target_file = "binarize_017_" +str(threshold_value) + ".jpg"
binarize(img, target_file)

# Image.MAX_IMAGE_PIXELS = None
#
# for filename in os.listdir("dem_result/dem"):
#     print filename
#     img = Image.open("dem_result/dem/" + filename)
#     w, h = img.size
#     target = img.resize((w // 4, h // 4), Image.ANTIALIAS)
#     target.save("dem_result/resize/" + filename)
#
#
#
# target = img.resize((1311, 1754), Image.ANTIALIAS)
#
# target.save("170.jpg")



# for filename in os.listdir("dem_result/dem"):
#     print filename
#     new_name = filename[-7::]
#     # print new_name
#     if filename.endswith(".jpg"):
#         os.rename("dem_result/dem/" + filename, "dem_result/dem/" + new_name)