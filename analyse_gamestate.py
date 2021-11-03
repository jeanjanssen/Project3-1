
import cv2
import imutils

"""
need to find away to split the image among the grid so we can see in which box the symbol falls
    find contour coordinates and split? or create boxes along side the contour? 
    
 symbol detection works
"""


# load frame to analyse
image = cv2.imread("invertedthreshold.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# find all contours
cnts = cv2.findContours(gray.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)



# loop over the contours
for (i, c) in enumerate(cnts):
    # compute the area of the contour along with the bounding box
    area = cv2.contourArea(c)
    (x, y, w, h) = cv2.boundingRect(c)
    # contours grid its self
    #cv2.drawContours(image, [c], -1, (0, 255, 0), 2)


    # compute the convex hull of the contour, then use the area of the
    # original contour and the area of the convex hull to compute the
    # solidity
    hull = cv2.convexHull(c)
    hullArea = cv2.contourArea(hull)
    solidity = area / float(hullArea)


    char = "?"

    # if the solidity >0.9 = `O`
    if solidity > 0.9:
        char = "O"

    # if solidity <0.9 and >0.5 = "X"
    elif solidity > 0.5:
        char = "X"

    # mark undecided contours
    if char != "?":
        cv2.drawContours(image, [c], -1, (0, 255, 0), 3)
        cv2.putText(image, char, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.25,
                    (0, 255, 0), 4)

    # show the contour properties
    print("{} (Contour #{}) -- solidity={:.2f}".format(char, i + 1, solidity))

# show the output image
cv2.imshow("Output", image)
cv2.waitKey(0)