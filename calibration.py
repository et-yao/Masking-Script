import cv2
import imutils
import numpy as np
import sys
#There are some weird shenanigans where I'm just trying to pass in an argument here
def nothing(x):
    pass
#First argument is just the file name of whatever you're trying to calibrate.
image = cv2.imread(sys.argv[1])
sliderWindow = 'Sliders'
cv2.namedWindow(sliderWindow)
imageHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
#cv2.imshow("test", imageHSV)
wnd = "Calibration"
cv2.createTrackbar('H_low',sliderWindow,0,179,nothing)
cv2.createTrackbar('S_low',sliderWindow,0,255,nothing)
cv2.createTrackbar('V_low',sliderWindow,0,255,nothing)
cv2.createTrackbar('H_high',sliderWindow,0,179,nothing)
cv2.createTrackbar('S_high',sliderWindow,0,255,nothing)
cv2.createTrackbar('V_high',sliderWindow,0,255,nothing)

cv2.setTrackbarPos('H_low', sliderWindow, 0)
cv2.setTrackbarPos('H_high', sliderWindow, 20)
cv2.setTrackbarPos('S_low', sliderWindow, 100)
cv2.setTrackbarPos('S_high', sliderWindow, 255)
cv2.setTrackbarPos('V_low', sliderWindow, 100)
cv2.setTrackbarPos('V_high', sliderWindow, 255)
r = 1000.0 / image.shape[1]
dim = (1000, int(image.shape[0] * r))
while(1):
    hueLow = cv2.getTrackbarPos('H_low', sliderWindow)
    hueHigh = cv2.getTrackbarPos('H_high', sliderWindow)
    satLow = cv2.getTrackbarPos('S_low', sliderWindow)
    satHigh = cv2.getTrackbarPos('S_high', sliderWindow)
    valLow = cv2.getTrackbarPos('V_low', sliderWindow)
    valHigh = cv2.getTrackbarPos('V_high', sliderWindow)
    imgCopy = imageHSV
    

    #lower = np.array([0,100,100])
    #upper = np.array([20,255,255])
    HSVLOW = np.array([hueLow, satLow, valLow], dtype = "uint8")
    HSVHIGH = np.array([hueHigh, satHigh, valHigh], dtype = "uint8")
    
    mask = cv2.inRange(imageHSV, HSVLOW, HSVHIGH)
    res = cv2.bitwise_and(image,image, mask = mask)
    resized = cv2.resize(res, dim, interpolation = cv2.INTER_AREA)
    cv2.imshow(wnd, resized)
    
    #invert it to help with noise reduction
    maskInverted = 255 - mask
    resizedMask = cv2.resize(maskInverted,dim, interpolation = cv2.INTER_AREA)
    cv2.imshow("mask Inverted", resizedMask)
    k = cv2.waitKey(5) & 0xFF
    if k == ord('s'):
        file = open(r"arrays.txt", 'w')
        file.write(str(hueLow) + "\n")
        file.write(str(satLow) + "\n")
        file.write(str(valLow) + "\n")
        file.write(str(hueHigh) + "\n")
        file.write(str(satHigh) + "\n")
        file.write(str(valHigh) + "\n")
        file.close()
        break
    if k == ord('q'):
        break
 
cv2.destroyAllWindows()