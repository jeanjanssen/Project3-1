import cv2 # use pip install open cv
import numpy as np

"""
**** uncomment cv2.imshow to see resulting image !!!!

cropped image coordinates with paper edge img[125:675, 200:975] (format [x:x+h][y:y+w])
cropped image coordinates without paper edge img[130:660, 220:960]
cropped image coordinates without gr code img[250:660, 220:760] 
"""

img = cv2.imread('webcam2.jpeg')  # image for now will be be made into a video stream

print(img.shape)  # Print image shape

kernelsize =5

blurr = cv2.medianBlur(img, kernelsize)

#cv2.imshow("orignal", img)
#cv2.imshow("blurr", blurr)


""" crop gameboard out of picture"""
cropped_image = img[250:660, 220:760]   # cropped image
cropped_blurr =blurr[250:660, 220:760] # blurred cropped image
cv2.imshow("cropped", cropped_image)

 # convert cropped image to gray scale
cropped_gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
#cv2.imshow("cropped gray", cropped_gray)

cropped_gray_blurry = cv2.cvtColor(cropped_blurr, cv2.COLOR_BGR2GRAY) # blurred cropped grayscaled





"""Different treshold for line FLD than Canny, then overlay lines for better image(if that exactly works???)"""
thresh = cv2.adaptiveThreshold(cropped_gray_blurry ,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
            cv2.THRESH_BINARY,11,6)
cv2.imshow("thres", thresh)


"""
 
thresh_1 = cv2.adaptiveThreshold(cropped_gray_blurry ,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
            cv2.THRESH_BINARY,11,6)
thresh_2 = cv2.adaptiveThreshold(cropped_gray_blurry ,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
            cv2.THRESH_BINARY,11,7)
thresh_3 = cv2.adaptiveThreshold(cropped_gray_blurry ,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
            cv2.THRESH_BINARY,11,9)

#cv2.imshow("Threshold Binary", thresh)

cv2.imshow('threshold_1',thresh_1)
cv2.imshow('threshold_2',thresh_2)
cv2.imshow('threshold_3',thresh_3)
"""

edges = cv2.Canny(thresh, 50, 200)
cv2.imshow("edges", edges)
# Detect points that form a line
lines = cv2.HoughLinesP(edges, 1, np.pi/180, 80, minLineLength=10, maxLineGap=500)
# Draw lines on the image
for line in lines:
    x1, y1, x2, y2 = line[0]
    cv2.line(cropped_gray, (x1, y1), (x2, y2), (255, 0, 0), 3)

# param1 = upperbound on threshold of canny, param2 is lowerbound on threshold
circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, 1, img.shape[0]/6, param1=200, param2=25, minRadius=15, maxRadius=30)
# Draw detected circles
if circles is not None:
    circles = np.uint16(np.around(circles))
    for i in circles[0, :]:
        # Draw outer circle
        cv2.circle(cropped_gray, (i[0], i[1]), i[2], (0, 255, 0), 2)
        # Draw inner circle
        cv2.circle(cropped_gray, (i[0], i[1]), 2, (0, 0, 255), 3)


# result
cv2.imshow("Result Image", cropped_gray)



cv2.waitKey(0)
cv2.destroyAllWindows()