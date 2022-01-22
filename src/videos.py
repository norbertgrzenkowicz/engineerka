import numpy as np
import cv2 as cv

streamed = True #TRUE - LIVE, FALSE - ALREADY CAPTURED VIDEO

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
    cap = cv.VideoCapture('vtest.avi')
     
    while cap.isOpened():
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        cv.imshow('frame', gray)
        if cv.waitKey(1) == ord('q'):
            break

#when everything done, release the capture
cap.release()
cv.destroyAllWindows()