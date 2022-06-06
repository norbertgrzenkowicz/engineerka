from abc import abstractmethod
import sys  
import cv2 as cv
import os
import numpy as np

print(cv.__version__)
# print(sys.version)

try:
    if not os.path.exists('data'):
        os.makedirs('data')

except OSError:
    print('Error: Creating directory of data')

class Device:
    def __init__(self):
        pass

    @abstractmethod
    def streamed_video():
        pass

    @abstractmethod
    def captured_video_save_data():
        pass

    @abstractmethod
    def captured_canny():
        pass

    def connect_output(self):
        self.cap = cv.VideoCapture('data/supermoto-evening.mp4')
        # self.cap = cv.VideoCapture(0)

        if self.cap.isOpened():
            print("Succesfully opened a connection.")

    def video_player(self, func):
        while True:
            # capture frame-by-frame
            self.ret, self.frame = self.cap.read()        
            
            if not self.ret:
            #if frame is read correctly ret is True
                print("Cant receive frame (stream end?). Exiting..")
                break

            media_output = func(self.frame)

            #display the resulting frame
            cv.imshow('frame', media_output)            
            if cv.waitKey(1) == ord('q'):
                break
            
        self.cap.release()
        cv.destroyAllWindows()


class Camera(Device):
    def __init__(self):
        self.cap = None
        self.ret = None
        self.frame = None
        self.connect_output()

    def grayer(self, frame):
        #our operations on the frame come here
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        
        return gray

    def captured_video_save_data(self):
        frame_per_second = self.cap.get(cv.CAP_PROP_FPS)

        current_frame = 0
        fps_calculator_previous = 0
        every_x_sec = 3
        current_frame_name_purpose = current_frame/30

        if self.ret:
            name = './data/supermoto_evening' + str(int(current_frame_name_purpose)) + '.jpg'
            fps_calculator = (current_frame / 30) % every_x_sec

            if (fps_calculator - fps_calculator_previous < 0):
                print("frameshotting")
                cv.imwrite(name, self.frame)
            fps_calculator_previous = fps_calculator
            current_frame += 1
            current_frame_name_purpose = current_frame/30
        
            #gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            #cv.imshow('frame', frame)

    def captured_canny(self):
        # if not cap.isOpened():
        #     print("Cannot open camera")
        #     exit()
            #our operations on the frame come here
            gray = cv. cvtColor(self.frame, cv.COLOR_BGR2GRAY)
            blur = cv.GaussianBlur(gray, (3,3), 0)
            edges = cv.Canny(image=blur, threshold1=50, threshold2=100) # Canny Edge Detection

            #display the resulting frame
            cv.imshow('Canny Edge Detection', edges)

    def threshold_data(self):
        try:
            if not os.path.exists('data/thresholded'):
                os.makedirs('data/thresholded')

        except OSError:
            print('Error: Creating directory of data/thresholded')
        
        data_dir = 'data/raw'
        
        for image in os.listdir(data_dir):
            image_path = "data/raw/" + image
            img = cv.imread(image_path)
            gray_image = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            ret, thresh = cv.threshold(gray_image, 80, 255, cv.THRESH_TOZERO)
            name = './data/thresholded/' + image
            cv.imwrite(name, thresh)


gopro_footage = Camera()
gopro_footage.captured_canny()
