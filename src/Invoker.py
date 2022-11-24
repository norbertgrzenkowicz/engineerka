import sys
import getopt
from matplotlib import pyplot as plt, image # from matplotlib import image
import numpy as np
from cv2 import imread, imwrite

from networkLoader import Network
from camera import Camera
from photoCamera import photoCamera
from kCluster import kCluster
from threshold import Threshold
from scikitThreshold import scikitThreshold
from imageCropper import imageCropper
from cornerAPI import Corners
from velocityPred import velocityPred

class Invoker:
    def __init__(self):
        self.mediaPath = ''
        self.calibrationList = np.genfromtxt(r'data/cam_calib/cam_calib.txt')

    def camOrPhoto(self, window):
        if self.mediaPath.endswith('.MP4'):
            media = Camera(videoPath=self.mediaPath)
        elif self.mediaPath.endswith('.png'):
            media = photoCamera(self.mediaPath, window=window)
        elif self.mediaPath == '':
            raise NameError('Nie podano sciezki zdjecia/wideo.')
        elif self.mediaPath.endswith('labeled') or self.mediaPath.endswith('labeled'):
            return None
        else:
            raise NameError('Nie obslugiwany format pliku. \nObslugiwane formaty to .mp4 i .png')

        return media

    def setPath(self, mediaPath):
        """Ustawienie podanej w terminalu sciezki pliku wideo/zdjeciowego"""
        self.mediaPath = mediaPath

    def cropDataset(self, mediaPath):
        """Uciecie rozdzielczosci podanego zbioru danych"""
        cropper = imageCropper(mediaPath)
        cropper.CropData()

    def resizeDataset(self, mediaPath):
        """Zmiana rozdzielczosci poprzez rozszerzenie podanego zbiory danych"""
        resizer = imageCropper(mediaPath)
        resizer.resizeData()

    def threshold(self):
        """Wykonanie operacji threshold"""
        thresholder = Threshold(self.mediaPath)
        thresholder.thresholding()

    def scikitThreshold(self):
        """Wykonanie operacji threshold z biblioteki scikit-image"""
        scikitThresholder = scikitThreshold(self.mediaPath)
        scikitThresholder.scikitThresholding()

    def kCluster(self):
        """Wykonanie algorytmu k-means cluster"""
        kClusterer = kCluster(self.mediaPath)
        kClusterer.kClustering()

    def segmentPhoto(self, mediaPath):
        """Segmentacja zdjecia"""
        nNetwork = Network(mediaPath)
        return nNetwork.savePreds()

    def predictPhoto(self):
        """Predykcja trajektorii ruchu i predkosci na wysegmentowanym pliku zdjeciowym"""
        self.saveToBePredictedPhoto()
        segmentedPhotoPath = self.segmentPhoto(self.mediaPath)

        predicter = Corners(OGmediaPath=self.mediaPath, mediaPath = segmentedPhotoPath)
        predicter.predApex()
        self.drawTrajectories(predicter)

        velPredicter = velocityPred(apexPoint=predicter.returnApex(), calibrationList = self.calibrationList)
        return velPredicter.canWeSlowDown()

    def drawTrajectories(self, pred):
        """Rysowanie trajektorii"""
        # pred.drawTrajectory(pred.returnTrajectoryPoints, pred.img, (0, 0, 255))
        pred.drawTrajectory(pred.returnTrajectory, pred.img, (255, 120, 120))
        pred.drawTrajectory(pred.returnPolyTrajectory, pred.img, (120, 120, 255))
        pred.drawTrajectory(pred.returnleftSide, pred.img, (120, 120, 120))
        pred.drawTrajectory(pred.returnRightSide, pred.img, (120, 120, 120))
        pred.drawApex()

        self.mediaPath = '/home/norbert/Documents/repos/engineerka/photos/preds/predictedRoad.png'
        imwrite(self.mediaPath, pred.img)            

    def saveToBePredictedPhoto(self):
        """Zapisanie zdjecia wraz z wszystkimi predykcjami"""
        img = imread(self.mediaPath)
        imwrite('/home/norbert/Documents/repos/engineerka/photos/preds/toBePredictedRoad.png', img)
