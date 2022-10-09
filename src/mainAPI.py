from matplotlib import image
import threshold
from threshold import threshold
from scikitThreshold import scikitThreshold
from kCluster import kCluster
from curveDetect import curveDetection

class mainAPI:
    def __init__(self):
        self.dupa = True

    def threshold(imagePath):
        thresholder = threshold(imagePath)
        return thresholder.thresholding()

    def scikitThreshold(imagePath):
        scikitThresholder = scikitThreshold(imagePath)
        scikitThresholder.scikitThresholding()
    
    def kCluster(imagePath):
        kClusterer = kCluster(imagePath)
        kClusterer.kClustering()
    
    def curveDetect(imagePath):
        curveDetector = curveDetection(imagePath)
        # TODO: implement plotting for curve decector
        # # font = cv2.FONT_HERSHEY_SIMPLEX
        # # cv2.putText(inputImage,"Tracks Detected", (500, 250), font, 0.5, 255)
        # # cv2.imshow("Trolley_Problem_Result", inputImage)
        # # cv2.imshow('edge', inputImage)
        # cv2.waitKey(0)
