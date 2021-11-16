


import cv2
import numpy as np


MIN_CONTOUR_AREA=20
def Detect_Corners(frame):
    """ uses  harris corners to find corners of sheet of paper

    somehow statistics works better then centroids....(sub-pixel accuracy?)


    """
    corner_list = cv2.cornerHarris(frame, 5, 3, 0.1)
    corner_list = cv2.dilate(corner_list, None)
    corner_list = cv2.threshold(corner_list, 0.01 * corner_list.max(), 255, 0)[1]
    corner_list = corner_list.astype(np.uint8)
    _, labels, statistics, centroids = cv2.connectedComponentsWithStats(
        corner_list, connectivity=4)

    return statistics



def computeContourArea(cont):
     Area = cv2.contourArea(cont)
     return cont

def return_contourdbox(frame):
    """
    Returns bbox  frames
    find contours, biggest object is the whole image, second biggest is the ROI
    """

    try :
     c,h = cv2.findContours(frame, 1, 2)
     #area = cv2.contourArea(c) # find contours, biggest object is the whole image, second biggest is the ROI


     contours_Sorted = sorted(c, key=lambda cntr: cv2.contourArea(cntr))
     rect = cv2.boundingRect(contours_Sorted[-2])
     #print(rect)
     return rect
    except : print("bbox failed ")
    pass


def Frame_PRE_proccsing(frame):
    """Preprocess image to match model's input shape for shape detection"""
    frame = cv2.resize(frame, (32, 32))
    # Expand both channel_last and batch size
    frame = np.expand_dims(frame, axis=-1)
    frame = np.expand_dims(frame, axis=0)
    return frame.astype(np.float32) / 255



