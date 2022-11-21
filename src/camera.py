from Device import Device
import sys  
import cv2 as cv
import os
import numpy as np
from matplotlib import pyplot as plt
from pathlib import Path

import logging # TODO: just one logger on whole project eh?

class Camera(Device):
    def __init__(self, videoPath=''):
        self.cap = None
        self.ret = None
        self.frame = None
        self.videoPath = videoPath
        self.current_frame = 0
        self.fps_calculator_previous = 0
        self.every_x_sec = 0.5

        self.connect_output()
        self.video_player()

    def connect_output(self, isLive=False):
        self.cap = cv.VideoCapture(0) if isLive else cv.VideoCapture(self.videoPath)

        if self.cap.isOpened():
            logging.warning("Succesfully opened a connection.")

    def video_player(self):
        while True:
            # capture frame-by-frame
            self.ret, self.frame = self.cap.read()        
            
            if not self.ret:
            #if frame is read correctly ret is True
                print("Cant receive frame (stream end?). Exiting..")
                break

            self.captured_video_save_data('/home/norbert/Documents/repos/engineerka/data/cam_calib')

            #display the resulting frame
            cv.imshow('frame', self.frame)   
            if cv.waitKey(1) == ord('q'):
                break
            
        self.cap.release()
        cv.destroyAllWindows()

    def captured_video_save_data(self, dataPath):

        # dataPath = '/data/unlabeled_test' # TODO: try if Path() is available here
        try:
            if not os.path.exists(dataPath):
                os.makedirs(dataPath)
        except OSError:
            logging.error('Tworzenie sciezki', dataPath)

        frame_per_second = self.cap.get(cv.CAP_PROP_FPS)

        current_frame_name_purpose = self.current_frame/15
        if self.ret:
            name = dataPath + '/cam_calib' + str(int(current_frame_name_purpose)) + '.png'
            print(name)
            fps_calculator = (self.current_frame / 15) % self.every_x_sec
            if (fps_calculator - self.fps_calculator_previous < 0):
                print("Klatka")
                cv.imwrite(name, self.frame)
            self.fps_calculator_previous = fps_calculator
            self.current_frame += 1
            current_frame_name_purpose = self.current_frame/15


    def capturedCanny(self):
        gray = cv.cvtColor(self.frame, cv.COLOR_BGR2GRAY)
        blur = cv.GaussianBlur(gray, (3,3), 0)
        edges = cv.Canny(image=blur, threshold1=50, threshold2=100)

        return edges

    def threshold_data(self, dataPath):
        # dataPath = 'data/thresholded'
        try:
            if not os.path.exists(dataPath):
                os.makedirs(dataPath)

        except OSError:
            logging.error('Creating directory of ', dataPath)
        
        unlabeledDataPath = 'data/unlabeled'
        
        for image in os.listdir(unlabeledDataPath):
            image_path = unlabeledDataPath + image
            img = cv.imread(image_path)
            gray_image = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            ret, thresh = cv.threshold(gray_image, 80, 255, cv.THRESH_TOZERO)
            name = './' + dataPath + '/' + image
            cv.imwrite(name, thresh)