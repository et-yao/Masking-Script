import cv2
import imutils
import numpy as np
import sys

#The first argument should be the file name UP TO the series: ex 1-nnnnnn_s3
#Second argument is the number of the last file.


for i in range(2, int(sys.argv[2])):
    
    
    image = cv2.imread(sys.argv[1] + "_%003d_crop.tif" %i)
    
    imageHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    #Read in the arrays
    file = open(r"arrays.txt", 'r')
    HSVLOW = np.array([int(file.readline()), int(file.readline()), int(file.readline())], dtype = "uint8")
    HSVHIGH = np.array([int(file.readline()), int(file.readline()), int(file.readline())], dtype = "uint8")
    mask = cv2.inRange(imageHSV, HSVLOW, HSVHIGH)
    res = cv2.bitwise_and(image,image, mask = mask)
    
    gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    filtered = gray
    filtered = cv2.bilateralFilter(gray, 5, 20, 20)
    gray = filtered
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)[1]

    r = 1000.0 / image.shape[1]
    dim = (1000, int(image.shape[0] * r))
 

    cnts, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    output = image.copy()
    bigContours = [] 
    for j in range(len(cnts)):
        area = cv2.contourArea(cnts[j])
        if area > 1000:
            cv2.drawContours(output, [cnts[j]], -1, (240, 0, 159), 3)
            bigContours.append(cnts[j])
    maskContours = np.zeros(image.shape[:2],np.uint8)
    for c in bigContours:
        cv2.drawContours(maskContours, [c], 0, (255, 255, 255), -1)
        
    dst = cv2.bitwise_and(image, image, mask=maskContours)
    
    #From here I repeated the procedure again to hopefully clean up the contours
    #Empirical tests result in something like 3000+ contours the first time through
    #and generally less than 30 the second time.
    gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
    thresh2 = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)[1]
    cnts, hierarchy2 = cv2.findContours(thresh2.copy(), cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    output = dst.copy()
    bigContours = [] 
    relevantHierarchy = [] #big contour hierarchy stuff
    for j in range(len(cnts)):
        area = cv2.contourArea(cnts[j])
        if area > 1000:
            cv2.drawContours(output, [cnts[j]], -1, (240, 0, 159), 3)
            bigContours.append((cnts[j], j))
            relevantHierarchy.append(hierarchy2[0][j])
    maskContours = np.zeros(image.shape[:2],np.uint8)
    
    
    for tuple in bigContours:
        if hierarchy2[0][tuple[1]][3] == -1:
            cv2.drawContours(maskContours, [tuple[0]], 0, (255, 255, 255), -1)
        else:
            cv2.drawContours(maskContours, [tuple[0]], 0, (0, 0, 0), -1)
        
        
        
    dst = cv2.bitwise_and(image, image, mask=thresh2)
    
    
   
    b, g, r = cv2.split(dst)
    rgba = [b,g,r, maskContours]
    dst = cv2.merge(rgba,4)
    #resized = cv2.resize(dst, dim, interpolation = cv2.INTER_AREA)
    #cv2.imshow("gray", resized)
    #k = cv2.waitKey(5) & 0xFF
    #if k == ord('q'):
    #   break
    str = "_%003d_crop_and_mask.tif" %i;
    cv2.imwrite(sys.argv[1] + str, dst)
