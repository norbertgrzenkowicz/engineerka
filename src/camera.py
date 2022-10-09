from Device import Device
import sys  
import cv2 as cv
import os
import numpy as np
from matplotlib import pyplot as plt
from pathlib import Path

import logging # TODO: just one logger on whole project eh?

class Camera(Device):
    def __init__(self):
        self.cap = None
        self.ret = None
        self.frame = None
        self.connect_output()

    def connect_output(self, isLive=False):
        self.cap = cv.VideoCapture(0) if isLive else cv.VideoCapture('supermoto-evening.mp4')

        if self.cap.isOpened():
            logging.info("Succesfully opened a connection.")

    def grayer(self, frame):
        return cv.cvtColor(frame, cv.COLOR_BGR2GRAY) 

    def captured_video_save_data(self):

        dataPath = 'data/unlabeled' # TODO: try if Path() is available here

        try:
            if not os.path.exists(dataPath):
                os.makedirs(dataPath)
        except OSError:
            logging.error('Creating directory of ', dataPath)

        frame_per_second = self.cap.get(cv.CAP_PROP_FPS)

        current_frame = 0
        fps_calculator_previous = 0
        every_x_sec = 3
        current_frame_name_purpose = current_frame/30

        if self.ret:
            name = './' + dataPath + str(int(current_frame_name_purpose)) + '.png'
            fps_calculator = (current_frame / 30) % every_x_sec

            if (fps_calculator - fps_calculator_previous < 0):
                logging.info("frameshooting")
                cv.imwrite(name, self.frame)
            fps_calculator_previous = fps_calculator
            current_frame += 1
            current_frame_name_purpose = current_frame/30
        
            #gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            #cv.imshow('frame', frame)

    def capturedCanny(self):
        # if not cap.isOpened():
        #     print("Cannot open camera")
        #     exit()
            #our operations on the frame come here

            gray = cv.cvtColor(self.frame, cv.COLOR_BGR2GRAY)
            blur = cv.GaussianBlur(gray, (3,3), 0)
            edges = cv.Canny(image=blur, threshold1=50, threshold2=100) # Canny Edge Detection

            #display the resulting frame
            cv.imshow('Canny Edge Detection', edges)

    def threshold_data(self):
        dataPath = 'data/thresholded'
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

    def augment_namefiles(self, dataPath):
        # dataPath = '/home/norbert/Documents/repos/engineerka/jupyter/~/bike_dataset/images'
        for count, image_name in enumerate(os.listdir(dataPath)):
            name = 'bike' + str(int(count)) + '.png'
            src = f"{dataPath}/{image_name}" 
            dst = f"{dataPath}/{name}"
            os.rename(src, dst)