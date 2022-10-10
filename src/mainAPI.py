import sys
import getopt
from matplotlib import pyplot as plt, image # from matplotlib import image

from camera import Camera
from photoCamera import photoCamera
from clahe import clahe
from kCluster import kCluster
from threshold import Threshold
from scikitThreshold import scikitThreshold
from thresholdToContour import thresholdToContour
from curveDetect import curveDetection
from imageCropper import imageCropper



class mainAPI:
    def __init__(self):
        self.dupa = True
        self.mediaPath = ''

    def camOrPhoto(self):
        if self.mediaPath.endswith('.mp4'):
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
        scikitThresholder.scikitThresholding()

    def thresholdToContour(self):
        thresholder = thresholdToContour()
        thresholder.thresholding()

    def kCluster(self):
        kClusterer = kCluster(self.mediaPath)
        kClusterer.kClustering()
    
    
    # def curveDetect(self.path):
    #     curveDetector = curveDetection(self.path)
    #     # TODO: implement plotting for curve decector
    #     # # font = cv2.FONT_HERSHEY_SIMPLEX
    #     # # cv2.putText(inputImage,"Tracks Detected", (500, 250), font, 0.5, 255)
    #     # # cv2.imshow("Trolley_Problem_Result", inputImage)
    #     # # cv2.imshow('edge', inputImage)
    #     # cv2.waitKey(0)

    def cornering(self):
        pass # TODO: clahe to class

    def predictPhoto(self):
        pass #TODO: class for predicting roads from loaded model
