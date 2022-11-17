import sys
import getopt
from matplotlib import pyplot as plt, image # from matplotlib import image

import numpy as np

from camera import Camera
from photoCamera import photoCamera
# from clahe import clahe
from kCluster import kCluster
from threshold import Threshold
from scikitThreshold import scikitThreshold
from thresholdToContour import thresholdToContour
from curveDetect import curveDetection
from imageCropper import imageCropper
from cornerAPI import Corners
from velocityPred import velocityPred

class mainAPI:
    def __init__(self):
        self.dupa = True
        self.mediaPath = ''
        self.calibrationList = np.genfromtxt(r'data/cam_calib/cam_calib.txt')

    def camOrPhoto(self):
        if self.mediaPath.endswith('.MP4'):
            media = Camera(videoPath=self.mediaPath)
        elif self.mediaPath.endswith('.png'):
            media = photoCamera(self.mediaPath)
        elif self.mediaPath == '':
            raise NameError('Nie podano sciezki zdjecia/wideo.')
        else :
            raise NameError('Nie obslugiwany format pliku. \nObslugiwane formaty to .mp4 i .png')

        return media

    def setPath(self, mediaPath):
        self.mediaPath = mediaPath

    def cropDataset(self):
        cropper = imageCropper(self.mediaPath)
        cropper.CropData()

    def threshold(self):
        thresholder = Threshold(self.mediaPath)
        return thresholder.thresholding()

    def scikitThreshold(self):
        scikitThresholder = scikitThreshold(self.mediaPath)
        return scikitThresholder.scikitThresholding()

    def thresholdToContour(self):
        thresholder = thresholdToContour(self.mediaPath)
        return thresholder.thresholding()

    def kCluster(self):
        kClusterer = kCluster(self.mediaPath)
        return kClusterer.kClustering()

    def cornering(self):
        pass # TODO: clahe to class

    def predictPhoto(self):
        predicter = Corners(self.mediaPath)
        predicter.predApex()

        self.drawTrajectories(predicter)

        velPredicter = velocityPred(apexPoint=predicter.returnApex(), calibrationList = self.calibrationList)

        return velPredicter.canWeSlowDown()

    def drawTrajectories(self, pred):
        pred.drawTrajectory(pred.returnTrajectoryPoints, pred.img)
        pred.drawTrajectory(pred.returnTrajectory, pred.img)
        pred.drawTrajectory(pred.returnPolyTrajectory, pred.img)

        import cv2
        frame = pred.img
        while True:
            cv2.imshow('Zdjecie',frame)

            if cv2.waitKey(1) == ord('q'):
                break
