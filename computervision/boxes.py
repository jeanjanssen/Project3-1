import cv2
import numpy as np

# TODO fix loop problem TypeError: 'int' object is not callable
# Read image
im = cv2.imread("/Users/stijnoverwater/Downloads/Hough-Rectangle-and-Circle-Detection-main/cases/dots2.png",
                cv2.IMREAD_GRAYSCALE)

# Set up the detector with default parameters.
# detector = cv2.SimpleBlobDetector()

# Setup SimpleBlobDetector parameters.
params = cv2.SimpleBlobDetector_Params()

# Change thresholds
params.minThreshold = 10
params.maxThreshold = 200

# Filter by Area.
params.filterByArea = True
params.minArea = 1

# Filter by Circularity
params.filterByCircularity = True
params.minCircularity = 0.1

# Filter by Convexity
params.filterByConvexity = True
params.minConvexity = 0.87

# Filter by Inertia
params.filterByInertia = True
params.minInertiaRatio = 0.01

detector = cv2.SimpleBlobDetector_create(params)

# Detect blobs.
keypoints = detector.detect(im)
print(len(keypoints))
range = len(keypoints)
board = []
pts = cv2.KeyPoint_convert(keypoints)
width = 0

cols = pts[:, 0]
rows = pts[:, 1]
if rows[0] == rows[1]:
    count = 2
    if rows[1] == rows[2]:
        count = count + 1
        if rows[2] == rows[3]:
            count = count + 1
            if rows[3] == rows[4]:
                count = count + 1
                if rows[4] == rows[5]:
                    count = count + 1
                    if rows[5] == rows[6]:
                        count = count + 1
                        if rows[6] == rows[7]:
                            count = count + 1
                            if rows[7] == rows[8]:
                                count = count + 1
                                if rows[8] == rows[9]:
                                    count = count + 1
                                    if rows[9] == rows[10]:
                                        count = count + 1
print(count)
width = float(count)
print(width, "width")
height = range / count
print(height, "height")


def create_tab(rows, columns):
    """
    generates a table of rows*columns
    :param rows: the number of rows for the table
    :param columns: the number of columns fot the table
    :return:
    """
    tab = []
    for x in range(rows):
        col = []

        for i in range(columns):
            col.append('+')

            if i == columns - 1:
                pass
            else:
                col.append(1)

        tab.append(col)

        col = []

        if x == rows - 1:
            return tab

        for i in range(columns):
            if i == 0:
                col.append(1)
            elif int(i) % 2 == 0:
                col.append(1)
            else:
                col.append(1)

            if i == columns - 1:
                pass
            else:
                col.append(' ')

        tab.append(col)

    return tab


def print_tab(table):
    """
    prints the table received
    :param table: the table
    """
    print(' ', end=' ')
    for x in range(len(table[0])):
        if x % 2 != 0:
            print(' ', end=' ')
        else:
            print(x // 2, end=' ')
    print()

    cont = 0

    for line in table:
        if cont % 2 != 0:
            print(' ', end=' ')
        else:
            print(cont // 2, end=' ')

        for column in line:
            if column == 1 or column == '1':
                print(' ', end=' ')
            else:
                print(column, end=' ')
        print()
        cont = cont + 1


if __name__ == "__main__":
    t = create_tab(width, height)
    print_tab(t)

# Draw detected blobs as red circles.
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (255, 0, 0),
                                      cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

# Show keypoints
cv2.imshow("Keypoints", im_with_keypoints)
cv2.waitKey(0)
