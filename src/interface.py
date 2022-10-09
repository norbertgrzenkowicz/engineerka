import sys
import os
import logging
from pathlib import Path

try:
    if not os.path.exists('data'):
        os.makedirs('data')
except OSError:
    logging.error('Creating directory of data')

class Interface:
    def __init__(self):
        self.something = False
        self.log = logging.getLogger("BRUH")
        self.testSegmentedImagePath = Path("/home/norbert/Documents/datasets/segmentedRoads/curvy/R0.jpg")
        self.testImagePath = Path("augment_the_curve.jpg")

    def CameraCall(self):
        from camera import Camera

        GoPro = Camera()
        GoPro.connect_output()
        self.log.info("yo ma men your camera is connected")

    def photoCameraCall(self):
        from photoCamera import photoCamera

        Images = photoCamera()
        self.log.info("photo picutred")


    def scikitThreshold(self):
        from scikitThreshold import scikitThreshold
        Image = "something"
        Augmenter = scikitThreshold(self.testImagePath)
        self.log.info("we do a little bit of figgin brother")
        Augmenter.figging()

    def kCluster(self):
        from kCluster import kCluster
        Cluster = kCluster(self.testImagePath)
        self.log.ino("yee ive klustrd someting for ya")