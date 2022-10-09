import sys
import os
import logging

from matplotlib import image
from dataHandler import dataHandler
from pathlib import Path
from mainAPI import mainAPI

try:
    if not os.path.exists('data'):
        os.makedirs('data')
except OSError:
    logging.error('Creating directory of data')

class Interface(dataHandler):
    def __init__(self):
        self.something = False
        self.log = logging.getLogger("BRUH")
        self.API = mainAPI()

    def thresholdThisPicture(self, imagePath):
        thresholdedImagePath = self.API.threshold(imagePath)

    def kClusterThisPicture(self, imagePath):
        self.API.kCluster(imagePath)
        