"""Useful functions for matrix transformations"""

import cv2
import numpy as np


def smart_resize(frame, new_size):
    """Resize image and maintain its ratio"""
    height, width = frame.shape[:2]
    ratio = height / width
    return cv2.resize(frame, (new_size, int(ratio * new_size)))


def smart_cut(frame):
    cropped_image = frame[100:600, 200:900]
    return cropped_image
