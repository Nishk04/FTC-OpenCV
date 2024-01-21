import cv2 as cv
import numpy as np
import sys

filename = "C:/Users/nishk/Data-Photos/RedProp3.png"

img = cv.imread(filename)
img = cv.resize(img, [0,0], fx=0.1, fy=0.1)
#print(img.shape) - to check if we are reading the image
cv.imshow("Original Image", img)
k = cv.waitKey(0)

# Converts image to HSV
img_HSV = cv.cvtColor(img, cv.COLOR_BGR2HSV)
cv.imshow("HSV output", img_HSV)
s = cv.waitKey(0) 

# HSV in the array - lists out what color range to look at
# Hue goes to 180 max | Saturation goes to 255 (how much color is there? lower -> grey) | Value goes to 255 (how dark is it? too high would mean black)
low = np.array([0,128, 60])
low2 = np.array([15, 255, 255])
high = np.array([175, 128, 60])
high2 = np.array([180,255, 255])

red_mask = cv.inRange(img_HSV, low, low2)    
red_mask2 = cv.inRange(img_HSV, high, high2)

# It multiplies anything red which would be higher than 0 so it filters anything not red into black-not needed
#red_pixels = red_mask * img[:,:,2]
#red_pixels2 = red_mask2 * img[:, :, 2]

# Combines the masks together into one image
final_mask = cv.bitwise_or(red_mask, red_mask2)
cv.imshow("Red Color Mask Output", final_mask)
k = cv.waitKey(0)

# Adds blur to image - inside the parentheses make sure numbers are odd and the higher the more blur
img_blur = cv.GaussianBlur(final_mask, (11,11), 0)
cv.imshow("Blur Output", img_blur)
s = cv.waitKey(0)  

rows = red_mask.shape[0]
img_circle = cv.HoughCircles(final_mask, cv.HOUGH_GRADIENT, 1, rows/16, 
                             param1=50, param2=21, minRadius=30 , maxRadius=80)

if img_circle is not None:
        img_circle = np.uint16(np.around(img_circle))
        for i in img_circle[0, :]:
            center = (i[0], i[1])
            # circle center
            cv.circle(img, center, 1, (0, 255, 0), 3)
            # circle outline
            radius = i[2]
            cv.circle(img, center, radius, (0, 255, 0), 3)

cv.imshow("final", img)
k = cv.waitKey(0)