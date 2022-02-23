import numpy as np
import cv2 as cv
import time
import os

streamed = False #TRUE - LIVE, FALSE - ALREADY CAPTURED VIDEO

try:
    if not os.path.exists('data'):
        os.makedirs('data')

except OSError:
    print('Error: Creating directory of data')

if streamed:
    cap = cv.VideoCapture(0)

    if not cap.isOpened():
        
        print("Cannot open camera")
        exit()

    while True:
        
        # capture frame-by-frame
        ret, frame = cap.read()        
        
        #if frame is read correctly ret is True
        if not ret:
            print("Cant receive frame (stream end?). Exiting..")
            break
        
        #our operations on the frame come here
        gray = cv. cvtColor(frame, cv.COLOR_BGR2GRAY)
        
        #display the resulting frame
        cv.imshow('frame', gray)
        if cv.waitKey(1) == ord('q'):
            break


if streamed == False:

    cap = cv.VideoCapture('videos/supermoto_evening.mp4')
    frame_per_second = cap.get(cv.CAP_PROP_FPS)

    current_frame = 0
    fps_calculator_previous = 0
    every_x_sec = 3
    current_frame_name_purpose = current_frame/30

    while cap.isOpened():    

        ret, frame = cap.read()

        if ret:
            name = './data/supermoto_evening' + str(int(current_frame_name_purpose)) + '.jpg'

            fps_calculator = (current_frame / 30) % every_x_sec

            if (fps_calculator - fps_calculator_previous < 0):
                print("frameshotting")
                cv.imwrite(name, frame)
            fps_calculator_previous = fps_calculator
            current_frame += 1
            current_frame_name_purpose = current_frame/30

        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        
        #gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        #cv.imshow('frame', frame)

        if cv.waitKey(1) == ord('q'):
            break

#when everything done, release the capture
cap.release()
cv.destroyAllWindows()