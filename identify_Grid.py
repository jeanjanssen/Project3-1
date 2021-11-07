


"""Different treshold for line FLD than Canny, then overlay lines for better image(if that exactly works???)"""
thresh = cv2.adaptiveThreshold(cropped_gray_blurry ,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
            cv2.THRESH_BINARY,11,6)
cv2.imshow("thres", thresh)

inverted_threshold = cv2.bitwise_not(thresh)
cv2.imshow("invert thres",inverted_threshold)


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
lines = cv2.HoughLinesP(inverted_threshold, 1, np.pi/180, 80, minLineLength=10, maxLineGap=50)
# Draw lines on the image
for line in lines:
    x1, y1, x2, y2 = line[0]
    cv2.line(inverted_threshold, (x1, y1), (x2, y2), (255, 0, 0), 3)

# param1 = upperbound on threshold of canny, param2 is lowerbound on threshold
circles = cv2.HoughCircles(inverted_threshold, cv2.HOUGH_GRADIENT, 1, img.shape[0]/6, param1=200, param2=25, minRadius=15, maxRadius=30)
# Draw detected circles
if circles is not None:
    circles = np.uint16(np.around(circles))
    for i in circles[0, :]:
        # Draw outer circle
        cv2.circle(inverted_threshold, (i[0], i[1]), i[2], (255, 0, 0), 2)
        # Draw inner circle
        cv2.circle(inverted_threshold, (i[0], i[1]), 2, (255, 0, 0), 3)


# result

cv2.imshow("Result Image", inverted_threshold)
#cv2.imwrite("edges.png",edges)
cv2.imwrite("invertedthreshold.png", inverted_threshold)

cv2.waitKey(0)
cv2.destroyAllWindows()
