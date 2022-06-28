# -*- coding: utf-8 -*-
# @Time : 2022/6/27 16:46
import cv2
import numpy as np

file1 = "1 (1).png"
file2 = "1_LSB-generated.png"


image1 = cv2.imread(file1)
image2 = cv2.imread(file2)
difference = cv2.subtract(image1, image2)

result = not np.any(difference)

if result is True:
    print("True")
else:
    cv2.imwrite("result.jpg", difference)
    print("False")