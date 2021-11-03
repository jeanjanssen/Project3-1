import cv2 # use pip install open cv
import numpy as np

"""
**** uncomment cv2.imshow to see resulting image !!!!

cropped image coordinates with paper edge img[125:675, 200:975] (format [x:x+h][y:y+w])
cropped image coordinates without paper edge img[130:660, 220:960]
"""

img = cv2.imread('webcam2.jpeg')  # image for now will be be made into a video stream

print(img.shape)  # Print image shape

kernelsize =3

blurr = cv2.medianBlur(img, kernelsize)

#cv2.imshow("orignal", img)
#cv2.imshow("blurr", blurr)


""" crop gameboard out of picture"""
cropped_image = img[130:660, 220:960]   # cropped image
cropped_blurr =blurr[130:660, 220:960] # blurred cropped image
cv2.imshow("cropped", cropped_image)

 # convert cropped image to gray scale
cropped_gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
cv2.imshow("cropped gray", cropped_gray)

cropped_gray_blurry = cv2.cvtColor(cropped_blurr, cv2.COLOR_BGR2GRAY) # blurred cropped grayscaled

"""Different treshold for line FLD than Canny, then overlay lines for better image(if that exactly works???)"""

(T, thresh) = cv2.threshold(cropped_gray_blurry, 135, 255, cv2.THRESH_BINARY) #canny edge detection

(T, thresh_2) = cv2.threshold(cropped_gray, 142, 255, cv2.THRESH_BINARY) # fast line detection (maybe use a different one?)
cv2.imshow("Threshold Binary + canny", thresh)
cv2.imshow("Threshold Binary FLD", thresh_2)
edges = cv2.Canny(thresh,100,200,apertureSize=7)
cv2.imshow("Edges",edges)

fld = cv2.ximgproc.createFastLineDetector()
"""
fld = cv2.createLineSegmentDetector(refine=cv2.LSD_REFINE_STD, )
custom linesegmentdetector to overlay on canny?

"""
#Detect lines in the image
lines1 = fld.detect(thresh_2)

#Draw detected lines in the image
drawn_img = fld.drawSegments(edges,lines1)  # draw lines in canny edge image
drawn_img1 = fld.drawSegments(cropped_gray,lines1) # draw lines seperate image
#Show image
cv2.imshow("FLD", drawn_img1)
cv2.imshow("FLD+CANNY", drawn_img)
mask0 = np.ones((3,3), np.uint8)
drawn_img_dilate=cv2.dilate(drawn_img, kernel=mask0,iterations=1) # dilate to see if we can make a more coherent picture





""" second round of canny edge for coherence might not be needed will have to see in practice """
#cv2.imshow("dilation", drawn_img_dilate)
canny_rnd2=cv2.Canny(drawn_img_dilate,100,200,apertureSize=7)
dilation_grayscale =cv2.cvtColor(drawn_img_dilate, cv2.COLOR_BGR2GRAY)
#cv2.imshow("dilation_grayscale",dilation_grayscale)
(T_,dilation_threshold) =cv2.threshold(dilation_grayscale, 10, 255, cv2.THRESH_BINARY)
#cv2.imshow("dilation threshold", dilation_threshold)

opening = cv2.morphologyEx(canny_rnd2, cv2.MORPH_OPEN, kernel=mask0)
#cv2.imshow("opening",opening)
"""

 threshold[125<->175]  
 
 image 1 
 best for now 146
 showcase reflection [130,150,160]
 
 image 2 best 131
 """
 
 

(T_1, thresh_1) = cv2.threshold(cropped_gray, 125, 255, cv2.THRESH_BINARY)
(T_2, thresh_2) = cv2.threshold(cropped_gray, 145, 255, cv2.THRESH_BINARY)
(T_3, thresh_3) = cv2.threshold(cropped_gray, 165, 255, cv2.THRESH_BINARY)
#cv2.imshow("Threshold Binary", thresh)

cv2.imshow('threshold_1',thresh_1)
cv2.imshow('threshold_2',thresh_2)
cv2.imshow('threshold_3',thresh_3)





minLineLength =30
maxLineGap = 10
lines = cv2.HoughLinesP(canny_rnd2,2,np.pi/180,threshold=80,minLineLength=minLineLength,maxLineGap=maxLineGap)

for x1,y1,x2,y2 in lines[0]:
    cv2.line(cropped_gray,(x1,y1),(x2,y2),(0,0,25),2)
cv2.imshow('houghlines5.jpg',cropped_gray)


"""


 houghline transform might not even be needed but rico said it would work. i just havent been able to make it work :/.
 
"""

#cv2.imshow('houghlines3.jpg', cropped_image)



corners = cv2.goodFeaturesToTrack(dilation_threshold,maxCorners=1000,qualityLevel=0.05,minDistance=60)
corners = np.int0(corners)

for corner in corners:
        x, y = corner.ravel()
        cv2.circle(cropped_image, (x, y), 3, 255, -1)
#cv2.imshow('Corner', cropped_image)



cv2.waitKey(0)
cv2.destroyAllWindows()