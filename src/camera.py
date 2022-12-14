from Device import Device
import sys  
import cv2 as cv
import os
import numpy as np
from matplotlib import pyplot as plt
from pathlib import Path

import logging

currentDir = os.getcwd()
class Camera(Device):
    def __init__(self, videoPath=''):
        self.cap = None
        self.ret = None
        self.frame = None
        self.videoPath = videoPath
        self.current_frame = 0
        self.fps_calculator_previous = 0
        self.every_x_sec = 0.5

        self.connectOutput()
        self.videoPlayer()

    def connectOutput(self, isLive=False):
        """Wlaczenie kamery lub pliku wideo podanego w sciezce self.videoPath"""
        self.cap = cv.VideoCapture(0) if isLive else cv.VideoCapture(self.videoPath)

        if self.cap.isOpened():
            print("Otwarto polaczenie.")

    def videoPlayer(self):
        """Metoda wyswietlajaca plik wideo i wykonywujaca self.capturedVideoSaveData"""
        while True:
            # Przypisanie kazdej klatki do zmiennej
            self.ret, self.frame = self.cap.read()        
            
            if not self.ret:
                print("Cant receive frame (stream end?). Exiting..")
                break

            self.capturedVideoSaveData(currentDir + '/data/cam_calib')

            #Pokaz klatke wyjsciowa
            cv.imshow('frame', self.frame)   
            if cv.waitKey(1) == ord('q'):
                break
            
        self.cap.release()
        cv.destroyAllWindows()

    def capturedVideoSaveData(self, dataPath):
        """Metoda zapisujaca klatke pliku wideo do podanej sciezki"""
        try:
            if not os.path.exists(dataPath):
                os.makedirs(dataPath)
        except OSError:
            print('Tworzenie sciezki', dataPath)

        frame_per_second = self.cap.get(cv.CAP_PROP_FPS)

        current_frame_name_purpose = self.current_frame/15
        if self.ret:
            name = dataPath + '/cam_calib' + str(int(current_frame_name_purpose)) + '.png'
            logging.debug(name)
            fps_calculator = (self.current_frame / 15) % self.every_x_sec
            if (fps_calculator - self.fps_calculator_previous < 0):
                logging.debug("Klatka")
                cv.imwrite(name, self.frame)
            self.fps_calculator_previous = fps_calculator
            self.current_frame += 1
            current_frame_name_purpose = self.current_frame/15
