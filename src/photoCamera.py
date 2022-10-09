from Device import Device
import sys  
import cv2 as cv
import os
import numpy as np
from matplotlib import pyplot as plt

from pathlib import Path
import logging

class photoCamera(Device):
    def __init__(self):
        self.cap = None
        self.ret = None
        self.frame = None

    def connect_output(self, imagePath):
        self.frame = cv.imread(imagePath)
        # self.cap = cv.VideoCapture(0)

        if self.cap.isOpened():
            logging.info("Succesfully opened a connection.")