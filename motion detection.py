


import cv2   # use pip instal opencv


# set is first iterartion by intilization set to None
baseline_image = None

# webcam
video = cv2.VideoCapture(0)

# loop video
while True:

    # Read in frame from webcam
    check, frame = video.read()

    # Initializing motion
    motion = 0

    #gray-scale image
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    kernelsize =15
    # filter image gaussian blur. removes noise of moving objects.

   # gray = cv2.GaussianBlur(gray, (kernelsize, kernelsize), 0)

   # set first frame as baseline
    if baseline_image is None:
        baseline_image = gray
        continue

    # Difference between baseline and current frame
    diff_frame = cv2.absdiff(baseline_image, gray)
    '''
    if differance in current image and the baseline is bigger then intensity threshold set pixel value white (255)
    intensity difference we will have to calibrate accoriding to the webcam 
    
    '''
    intensity_threshold = 200
    thresh_frame = cv2.threshold(diff_frame, intensity_threshold, 255, cv2.THRESH_BINARY)[1]


    #dilate for better coheracne
    #thresh_frame = cv2.dilate(thresh_frame, None, iterations=1)

    # Finding contour of moving object
    cnts, _ = cv2.findContours(thresh_frame.copy(),
                               cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        #if cv2.contourArea(contour) > 5000 and cv2.contourArea(contour) <10000000000 :  # detection threshold contour area
        if cv2.contourArea(contour) <(10000/1.6) :
            continue
        motion = 1

        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
    # draw green rectangle

    cv2.imshow("Gray Frame", gray)
    cv2.imshow("Difference Frame", diff_frame)
    cv2.imshow("Threshold Frame", thresh_frame)
    cv2.imshow("Color Frame", frame)

    key = cv2.waitKey(1)

    if key == ord('q'):        # kill switch is q

        break


video.release()

# Destroying all the windows
cv2.destroyAllWindows()