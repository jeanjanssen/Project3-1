"""Useful functions for matrix transformations"""

import cv2
import numpy as np


def FPT_HELPER_(points):
    """
    Helper function for four_point_transform.

    Order points: top-left, top-right, bottom-right and top-left

    top-left will have smallest sum and  bottom-right the biggest

    top-right will have smallest difference, and bottom-left will have the largest one

    """

    rectangle = np.zeros((4, 2), dtype=np.float32)
    points_sum = points.sum(axis=1)
    try:
        rectangle[0] = points[np.argmin(points_sum)]
        rectangle[2] = points[np.argmax(points_sum)]
    except Exception:
        pass

    points_differance = np.diff(points, axis=1)
    try:
        rectangle[1] = points[np.argmin(points_differance)]
        rectangle[3] = points[np.argmax(points_differance)]
    except Exception:
        pass
    return rectangle


def FPT_BIRDVIEW(frame, points):
    """uses four point transform to return a bird view of game board


    width of new image will be the max difference between
    bottom-right - bottom-left or top-right - top-left
    as goes for height
    """
    rectangle = FPT_HELPER_(points)
    top_left, top_right, bottom_right, bottom_left = rectangle
    # width of new image
    width_a = np.linalg.norm(bottom_right - bottom_left)
    width_b = np.linalg.norm(top_right - top_left)
    NEW_width = int(round(max(width_a, width_b)))
    # height new image
    height_a = np.linalg.norm(top_right - bottom_right)
    height_b = np.linalg.norm(top_left - bottom_left)
    NEW_height = int(round(max(height_a, height_b)))
    # create destination image
    destination_image = np.array([
        [0, 0], [NEW_width - 1, 0], [NEW_width - 1, NEW_height - 1], [0, NEW_height - 1]],
        dtype=np.float32)
    # apply transform and warp image
    Model = cv2.getPerspectiveTransform(rectangle, destination_image)
    Model_warped = cv2.warpPerspective(frame, Model, (NEW_width, NEW_height))
    return Model_warped


def smart_resize(frame, new_size):
    """Resize image and maintain its ratio"""
    height, width = frame.shape[:2]
    ratio = height / width
    return cv2.resize(frame, (new_size, int(ratio * new_size)))


def smart_cut(frame):
    cropped_image = frame[100:600, 200:900]
    return cropped_image
