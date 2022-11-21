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

        if isinstance(imagePath, str):
            self.frame = cv.imread(imagePath)
        else:
            self.frame = imagePath

        logging.warning("Otwarto polaczenie.")
        while True:
            cv.imshow('Zdjecie',self.frame)

            if cv.waitKey(1) == ord('q'):
                break

        # if self.cap.isOpened():
        #     logging.warning("Otwarto polaczenie.")

    def overwritePhoto(self, img):
        self.frame = img
