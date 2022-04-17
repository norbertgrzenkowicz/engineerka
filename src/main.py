import sys  
import cv2 as cv
import os
import numpy as np

print(cv.__version__)
print(sys.version)

try:
    if not os.path.exists('data'):
        os.makedirs('data')

except OSError:
    print('Error: Creating directory of data')

#base cap
cap = cv.VideoCapture(0)
cap = cv.VideoCapture('videos/supermoto_evening.mp4')


def streamed_video():

    if not cap.isOpened():
        
        print("Cannot open camera")
        exit()

    while True:
        
        # capture frame-by-frame
        ret, frame = cap.read()        
        
        if not ret:
        #if frame is read correctly ret is True
            print("Cant receive frame (stream end?). Exiting..")
            break
        
        #our operations on the frame come here
        gray = cv. cvtColor(frame, cv.COLOR_BGR2GRAY)
        
        #display the resulting frame
        cv.imshow('frame', gray)
        if cv.waitKey(1) == ord('q'):
            break

def captured_video_save_data():
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

def captured_just_canny():
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
        blur = cv.GaussianBlur(gray, (3,3), 0)
        edges = cv.Canny(image=blur, threshold1=50, threshold2=100) # Canny Edge Detection

        #display the resulting frame
        cv.imshow('Canny Edge Detection', edges)
        if cv.waitKey(1) == ord('q'):
            break


cap.release()
cv.destroyAllWindows()