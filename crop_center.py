#Code for the first part is adapted from pyimagesearch
#Source: https://www.pyimagesearch.com/2016/04/11/finding-extreme-points-in-contours-with-opencv/

import cv2
import imutils
import numpy as np
import sys

def distance(p0, p1):
    return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)
mostLeft = sys.maxsize
mostRight = 0
mostBottom = 0
mostTop = sys.maxsize
for i in range(2, int(sys.argv[2])):
    
    
    image = cv2.imread(sys.argv[1] + "_%003d.tif" %i)
    imageHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    #prep the image
    file = open(r"arrays.txt", 'r')
    HSVLOW = np.array([int(file.readline()), int(file.readline()), int(file.readline())], dtype = "uint8")
    HSVHIGH = np.array([int(file.readline()), int(file.readline()), int(file.readline())], dtype = "uint8")
    mask = cv2.inRange(imageHSV, HSVLOW, HSVHIGH)
    res = cv2.bitwise_and(image,image, mask = mask)
    
    gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    #filtered = cv2.bilateralFilter(gray, 5, 20, 20)
    #gray = filtered
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    #thresholds
    thresh = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.erode(thresh, None, iterations=2)
    thresh = cv2.dilate(thresh, None, iterations=2)

    #find contours
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    c = max(cnts, key=cv2.contourArea)
    #assume the largest contour is the object

    #Use funky numpy 
    #also i realized it would be a lot funnier if funky rhymed with numpy
    # determine the most extreme points along the contour - thanks pyimagesearch
    extLeft = tuple(c[c[:, :, 0].argmin()][0])
    extRight = tuple(c[c[:, :, 0].argmax()][0])
    extTop = tuple(c[c[:, :, 1].argmin()][0])
    extBot = tuple(c[c[:, :, 1].argmax()][0])
    
    if extLeft[0] < mostLeft:
        mostLeft = extLeft[0]
    if extRight[0] > mostRight:
        mostRight = extRight[0]
    if extBot[1] > mostBottom:
        mostBottom = extBot[1]
    if extTop[1] < mostTop:
        mostTop = extTop[1]
    print(str(mostLeft) + " " + str(mostRight) + " " + str(mostBottom) + " " + str(mostTop))
    cv2.drawContours(image, [c], -1, (0, 255, 255), 2)
    cv2.circle(image, extLeft, 8, (0, 0, 255), -1)
    cv2.circle(image, extRight, 8, (0, 255, 0), -1)
    cv2.circle(image, extTop, 8, (255, 0, 0), -1)
    cv2.circle(image, extBot, 8, (255, 255, 0), -1)
    lineThickness = 2
    cv2.line(image, (mostLeft, 0), (mostLeft, image.shape[0]), (0,255,0), lineThickness)
    cv2.line(image, (mostRight, 0), (mostRight, image.shape[0]), (0,255,0), lineThickness)
    cv2.line(image, (0, mostTop), (image.shape[1], mostTop), (0,255,0), lineThickness)
    cv2.line(image, (0, mostBottom), (image.shape[1], mostBottom), (0,255,0), lineThickness)
 
    
    r = 1000.0 / image.shape[1]
    dim = (1000, int(image.shape[0] * r))
    resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
    # show the output image
    cv2.imshow("Image", resized)
    cv2.waitKey(0)
"""for i in range(2, int(sys.argv[2])):
    image = cv2.imread(sys.argv[1] + "_%003d.tif" %i)
    cropped = image[mostTop:mostBottom, mostLeft:mostRight].copy()
    cv2.imwrite(sys.argv[1] + "_%003d_crop.tif"%i, cropped)"""

