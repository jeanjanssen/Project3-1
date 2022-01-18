import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('/Users/stijnoverwater/Documents/GitHub/Project3-1/start frame copy.png',0)


thresh1 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,
                                    cv2.THRESH_BINARY,11,2)
thresh2 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,
                                    cv2.THRESH_BINARY,31,2)
thresh3 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,
                                    cv2.THRESH_BINARY,51,2)
thresh4 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,
                                    cv2.THRESH_BINARY,71,2)
thresh5 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,
                                    cv2.THRESH_BINARY,91,2)
thresh6 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,
                                    cv2.THRESH_BINARY,111,2)
thresh7 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,
                                    cv2.THRESH_BINARY,131,2)
thresh8 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,
                                    cv2.THRESH_BINARY,151,2)
thresh9 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,
                                    cv2.THRESH_BINARY,171,2)





#thresh3 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
      #                              cv2.THRESH_BINARY,11,2)

plt.subplot(331), plt.imshow(thresh1,'gray')
plt.title('block size: 11')
plt.subplot(332), plt.imshow(thresh2, 'gray')
plt.title('block size: 31')
plt.subplot(333), plt.imshow(thresh3, 'gray')
plt.title('block size: 51')
plt.subplot(334), plt.imshow(thresh4, 'gray')
plt.title('block size: 71')
plt.subplot(335), plt.imshow(thresh5, 'gray')
plt.title('block size: 91')
plt.subplot(336), plt.imshow(thresh6, 'gray')
plt.title('block size: 111')
plt.subplot(337), plt.imshow(thresh7, 'gray')
plt.title('block size: 131')
plt.subplot(338), plt.imshow(thresh8, 'gray')
plt.title('block size: 151')
plt.subplot(339), plt.imshow(thresh9, 'gray')
plt.title("block size: 171")

plt.savefig('MeanThresholdtest.png')

plt.show()
thresh1 = cv2.adaptiveThreshold(img,255,cv2.CALIB_CB_ADAPTIVE_THRESH,
                                    cv2.THRESH_BINARY,11,2)
thresh2 = cv2.adaptiveThreshold(img,255,cv2.CALIB_CB_ADAPTIVE_THRESH,
                                    cv2.THRESH_BINARY,31,2)
thresh3 = cv2.adaptiveThreshold(img,255,cv2.CALIB_CB_ADAPTIVE_THRESH,
                                    cv2.THRESH_BINARY,51,2)
thresh4 = cv2.adaptiveThreshold(img,255,cv2.CALIB_CB_ADAPTIVE_THRESH,
                                    cv2.THRESH_BINARY,71,2)
thresh5 = cv2.adaptiveThreshold(img,255,cv2.CALIB_CB_ADAPTIVE_THRESH,
                                    cv2.THRESH_BINARY,91,2)
thresh6 = cv2.adaptiveThreshold(img,255,cv2.CALIB_CB_ADAPTIVE_THRESH,
                                    cv2.THRESH_BINARY,111,2)
thresh7 = cv2.adaptiveThreshold(img,255,cv2.CALIB_CB_ADAPTIVE_THRESH,
                                    cv2.THRESH_BINARY,131,2)
thresh8 = cv2.adaptiveThreshold(img,255,cv2.CALIB_CB_ADAPTIVE_THRESH,
                                    cv2.THRESH_BINARY,151,2)
thresh9 = cv2.adaptiveThreshold(img,255,cv2.CALIB_CB_ADAPTIVE_THRESH,                                    cv2.THRESH_BINARY,171,2)
plt.subplot(331), plt.imshow(thresh1,'gray')
plt.title('block size: 11')
plt.subplot(332), plt.imshow(thresh2, 'gray')
plt.title('block size: 31')
plt.subplot(333), plt.imshow(thresh3, 'gray')
plt.title('block size: 51')
plt.subplot(334), plt.imshow(thresh4, 'gray')
plt.title('block size: 71')
plt.subplot(335), plt.imshow(thresh5, 'gray')
plt.title('block size: 91')
plt.subplot(336), plt.imshow(thresh6, 'gray')
plt.title('block size: 111')
plt.subplot(337), plt.imshow(thresh7, 'gray')
plt.title('block size: 131')
plt.subplot(338), plt.imshow(thresh8, 'gray')
plt.title('block size: 151')
plt.subplot(339), plt.imshow(thresh9, 'gray')
plt.title("block size: 171")

plt.savefig('GBThresholdtest.png')

plt.show()