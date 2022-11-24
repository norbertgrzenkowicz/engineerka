from Device import Device
import sys  
import cv2 as cv
import os
import numpy as np
from matplotlib import pyplot as plt

from pathlib import Path
import logging

class photoCamera(Device):
    def __init__(self, imagePath, window=True):
        self.cap = None
        self.ret = None
        self.frame = None
        self.window = window
        if self.window:
            self.connectOutput(imagePath)

    def connectOutput(self, imagePath):
        "Wyswietlenie podanego pliku zdjeciowego"
        if isinstance(imagePath, str):
            self.frame = cv.imread(imagePath)
        else:
            self.frame = imagePath

        logging.warning("Otwarto polaczenie.")
        while True:
            cv.imshow('Zdjecie',self.frame)

            if cv.waitKey(1) == ord('q'):
                break

    def overwritePhoto(self, img):
        self.frame = img
