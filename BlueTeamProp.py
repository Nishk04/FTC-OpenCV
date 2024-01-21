import cv2 as cv
import numpy as np
import sys

filename = "C:/Users/nishk/Data-Photos/BlueProp5.png"

img = cv.imread(filename)
img = cv.resize(img, [0,0], fx=0.1, fy=0.1)
# print(img.shape) - to check if we are reading the image
cv.imshow("Original Image", img)
k = cv.waitKey(0)

# Converts image to HSV
img_HSV = cv.cvtColor(img, cv.COLOR_BGR2HSV)
cv.imshow("HSV output", img_HSV)
s = cv.waitKey(0) 

# HSV in the array - lists out what color range to look at
# Hue goes to 180 max | Saturation goes to 255 (how much color is there? lower -> grey) | Value goes to 255 (how dark is it? too high would mean black)
low = np.array([190/2,128, 64])
high = np.array([250/2, 255, 255])
blue_mask = cv.inRange(img_HSV, low, high)    

# It multiplies anything red which would be higher than 0 so it filters anything not red into black-not needed
blue_pixels = blue_mask * img[:,:,2]

cv.imshow("Blue Color Mask Output", blue_mask)
k = cv.waitKey(0)

# Adds blur to image - inside the parentheses make sure numbers are odd and the higher the more blur
img_blur = cv.GaussianBlur(blue_mask, (11,11), 0)
cv.imshow("Blur Output", img_blur)
s = cv.waitKey(0)  

rows = blue_mask.shape[0]
img_circle = cv.HoughCircles(blue_mask, cv.HOUGH_GRADIENT, 1, rows/16, 
                             param1=50, param2=35, minRadius=20, maxRadius=0)

if img_circle is not None:
        img_circle = np.uint16(np.around(img_circle))
        for i in img_circle[0, :]:
            center = (i[0], i[1])
            # circle center
            cv.circle(img, center, 1, (0, 255, 0), 3)
            # circle outline
            radius = i[2]
            cv.circle(img, center, radius, (0, 255, 0), 3)
            print("inside")
cv.imshow("final", img)
k = cv.waitKey(0)