from Device import Device
import sys  
import cv2 as cv
import os
import numpy as np
from matplotlib import pyplot as plt

from pathlib import Path
import logging

class photoCamera(Device):
    def __init__(self, imagePath):
        self.cap = None
        self.ret = None
        self.frame = None
        self.connect_output(imagePath)

    def connect_output(self, imagePath):
        self.frame = cv.imread(imagePath)
        imgray = cv.cvtColor(self.frame, cv.COLOR_BGR2GRAY)
        ret, thresh = cv.threshold(imgray, 127, 255, 0)
        im2, contours, hierarchy, dupa = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        cv.drawContours(im2, contours, -1, (0,255,0), 3)
        logging.warning("Otwarto polaczenie.")
        while True:
            cv.imshow('Zdjecie',im2)

            if cv.waitKey(1) == ord('q'):
                break

        # if self.cap.isOpened():
        #     logging.warning("Otwarto polaczenie.")