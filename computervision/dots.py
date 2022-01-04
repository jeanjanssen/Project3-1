import cv2
import math
import numpy as np


picsdot1= "/Users/stijnoverwater/Documents/GitHub/Project3-1/computervision/dots and boxes.jpeg"
picsdot2= "/Users/stijnoverwater/Documents/GitHub/Project3-1/computervision/dots2.png"

img = cv2.imread(picsdot1)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow("gray",gray)
thresh2 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY, 199, 5)
cv2.imshow("thres",thresh2)
cnts = cv2.findContours(thresh2, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[-2]



min_dot_size = 1
max_dot_size = 20
dots = []

for cnt in cnts:
    dots.append(cnt)
    if min_dot_size < cv2.contourArea(cnt) < max_dot_size:

        M = cv2.moments(cnt)

             # calculate x,y coordinate of center
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        cv2.circle(img, (cX, cY), 15, (255,0, 0), -1)

# printing output
number_dots= len(dots)
row = math.sqrt(number_dots)
print("\nRow size: {}".format(row))
print("\nDots number: {}".format(number_dots))
cv2.imshow("Image", img)

gray2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
thresh3 = cv2.adaptiveThreshold(gray2, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY, 199, 5)
cnts2 = cv2.findContours(thresh2, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[-2]
min_dot_size2 = 10
max_dot_size2 = 50
dots2 = []
for cnt in cnts2:
    if min_dot_size < cv2.contourArea(cnt) < max_dot_size:

     dots2.append(cnt)

number_dots2= len(dots2)
row2 = math.sqrt(number_dots2)
print("\nRow size: {}".format(row2))
print("\nDots number: {}".format(number_dots2))



"""
blur = cv2.GaussianBlur(gray,(3,3),3)
thresh2 = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY, 199, 9)
cimg = cv2.cvtColor(blur,cv2.COLOR_GRAY2BGR)
circles = cv2.HoughCircles(blur,cv2.HOUGH_GRADIENT,1,1,
                            param1=120,param2=10,minRadius=2,maxRadius=30)

circlecount=0
circles = np.uint16(np.around(circles))
for i in circles[0,:]:
    # draw the outer circle
    cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
    # draw the center of the circle
    cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)
    circlecount = circlecount +1

print(circlecount)
cv2.imshow('detected circles',cimg)
"""
cv2.waitKey(0)
cv2.destroyAllWindows()