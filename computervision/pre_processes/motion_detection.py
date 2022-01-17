


import cv2   # use pip instal opencv
from computervision import test_player
import time
import imutils
import datetime
# set is first iterartion by intilization set to None

def video_cut(frame):
    cropped_image = frame[100:600, 200:900]
    return cropped_image


video = cv2.VideoCapture(0)
print("[INFO] warming up...")
lastUploaded = datetime.datetime.now()
motionCounter = 0
def motiondection(video):

    baseline_frame = None
    avg_frame = None
# loop video
    while True:

        # Read in frame from webcam
        check, frame = video.read()
        kernelsize = 21
        frame_cut =video_cut(frame)
        frame2 = frame
        timestamp = datetime.datetime.now()
        text = "Unoccupied"
        frame2 = imutils.resize(frame2, width=700)
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.GaussianBlur(gray2, (21, 21), 0)
        if avg_frame is None:
            print("[INFO] starting background model...")
            avg_frame = gray2.copy().astype("float")
            continue
        cv2.accumulateWeighted(gray2, avg_frame, 0.03)
        frameDelta = cv2.absdiff(gray2, cv2.convertScaleAbs(avg_frame))
        threshdelta = cv2.adaptiveThreshold(frameDelta, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 199,6)
        threshdelta = cv2.dilate(threshdelta, None, iterations=2)
        cntsdelta= cv2.findContours(threshdelta.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cntsdelta = imutils.grab_contours(cntsdelta)
        # loop over the contours
        for c in cntsdelta:
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < 100:
                continue
            # compute the bounding box for the contour, draw it on the frame,
            # and update the text
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame2, (x, y), (x + w, y + h), (0, 255, 0), 2)
            text = "Occupied"




        # draw the text and timestamp on the frame
        ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
        cv2.putText(frame2, "board Status: {}".format(text), (10, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(frame2, ts, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.35, (0, 0, 255), 1)





        cv2.imshow("new motion", baseline_frame)
        cv2.imshow('newmoetions', frame2)
        key = cv2.waitKey(1)

        time.sleep(0.015)
        if key == ord('q'):  # kill switch is q
              break



    video.release()

    # Destroying all the windows
    cv2.destroyAllWindows()
def main():
    vcap = cv2.VideoCapture(0)
    motiondection(vcap)

# webcam

if __name__ == '__main__':
        main()
