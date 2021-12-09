


import cv2   # use pip instal opencv


# set is first iterartion by intilization set to None

video = cv2.VideoCapture(0)

def motiondection(video):
    detected= False
    baseline_image_1 = None
    baseline_image_2 = None
    baseline_image_3 = None
# loop video
    while True:

        # Read in frame from webcam
        check, frame = video.read()
        kernelsize = 21
        # Initializing motion
        motion = 0

        #gray-scale image
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        gray = cv2.GaussianBlur(gray, (kernelsize, kernelsize), 0)

        #print(gray.shape)
        height, width = gray.shape
        frame_partONE=gray[0:height, 0:width-1050]
        cv2.imshow("frame_part_one", frame_partONE)

        frame_partTWO = gray[height-100:height, 0:width]  ## bottem
        cv2.imshow('frame_part_two', frame_partTWO)

        frame_partTHREE= gray[0:height,950:width]
        cv2.imshow('frame_part_three', frame_partTHREE)


    # filter image gaussian blur. removes noise of moving objects.



   # set first frame as baseline
        if baseline_image_1 is None:
            baseline_image_1 = frame_partONE
            continue

        if baseline_image_2 is None:
            baseline_image_2= frame_partTWO
            continue

        if baseline_image_3 is None:
            baseline_image_3 = frame_partTHREE
            continue


        # Difference between baseline and current frame
        diff_frame_1 = cv2.absdiff(baseline_image_1, frame_partONE)
        diff_frame_2 = cv2.absdiff(baseline_image_2, frame_partTWO)
        diff_frame_3 = cv2.absdiff(baseline_image_3, frame_partTHREE)
        '''
        if differance in current image and the baseline is bigger then intensity threshold set pixel value white (255)
        intensity difference we will have to calibrate accoriding to the webcam 
    
        '''
        intensity_threshold = 100
        #thresh_frame = cv2.threshold(diff_frame, intensity_threshold, 255, cv2.THRESH_BINARY)[1]
        thresh_frame_1=cv2.adaptiveThreshold(diff_frame_1, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 21, 5)
        thresh_frame_2 = cv2.adaptiveThreshold(diff_frame_2, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 21,
                                           5)
        thresh_frame_3 = cv2.adaptiveThreshold(diff_frame_3, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 21,
                                           5)
        #dilate for better coheracne
        #thresh_frame = cv2.dilate(thresh_frame, None, iterations=1)

        # Finding contour of moving object
        cnts_1, _ = cv2.findContours(thresh_frame_1.copy(),
                               cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts_2, _ = cv2.findContours(thresh_frame_2.copy(),
                                 cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts_3, _ = cv2.findContours(thresh_frame_3.copy(),
                                 cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour_1 in cnts_1:
             #if cv2.contourArea(contour) > 50000 and cv2.contourArea(contour) <1000000000000000000000 :  # detection threshold contour area
            if cv2.contourArea(contour_1) <(1000/2) :

                continue
            else :
                detected= False
            (x, y, w, h) = cv2.boundingRect(contour_1)
            detected= True

            #cv2.rectangle(thresh_frame_1, (x, y), (x + w, y + h), (0, 255, 0), 3)
            #cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
            #return detected



        for contour_2 in cnts_2:
        # if cv2.contourArea(contour) > 50000 and cv2.contourArea(contour) <1000000000000000000000 :  # detection threshold contour area
            if cv2.contourArea(contour_2) < (1000 / 10):  # smaller area
                continue
            else :
                detected= False
            (x, y, w, h) = cv2.boundingRect(contour_2)
            detected =True
            #cv2.rectangle(thresh_frame_1, (x, y), (x + w, y + h), (0, 255, 0), 3)
            #cv2.rectangle(frame, (x, y+620), (x + w, y+620 + h), (0, 0, 255), 3) #red
            #return detected
        for contour_3 in cnts_3:
                # if cv2.contourArea(contour) > 50000 and cv2.contourArea(contour) <1000000000000000000000 :  # detection threshold contour area
            if cv2.contourArea(contour_3) < (1000 / 3):
                continue
            else:
                detected = False

            (x, y, w, h) = cv2.boundingRect(contour_3)
            detected = True
            #cv2.rectangle(thresh_frame_1, (x, y), (x + w, y + h), (0, 255, 0), 3)
            #cv2.rectangle(frame, (x+950, y), (950+x + w, y + h), ( 255, 0,0), 3)
            #return detected


        motion = 1
        winner = detected
        height = frame.shape[0]
        text = 'Collistion detections is {}!!'.format(str(winner))
        cv2.putText(frame, text, (250, height - 550),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0), 3)
        detected = False
        # draw green rectangle

        #cv2.imshow("Gray Frame", gray)
        #cv2.imshow("Difference Frame", diff_frame_1)
        #cv2.imshow("Threshold Frame", thresh_frame_1)
        cv2.imshow("Color Frame", frame)

        key = cv2.waitKey(1)

        if key == ord('q'):        # kill switch is q

            break
        #return detected



    video.release()

    # Destroying all the windows
    cv2.destroyAllWindows()
def main():
    vcap = cv2.VideoCapture(0)
    motiondection(vcap)

# webcam

if __name__ == '__main__':
        main()
