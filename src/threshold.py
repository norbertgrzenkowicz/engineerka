"""
Simple thresholding applied to a real image using np.arange() to create the different threshold values
"""

# Import required packages:

from Device import Device
from dataHandler import dataHandler
from matplotlib import pyplot as plt
import numpy as np
import cv2

class Threshold(Device):
    def __init__(self, mediaPath):
        self.fig = plt.figure(figsize=(9, 9))
        self.fig.patch.set_facecolor('silver')
        self.image = cv2.imread(mediaPath)

        self.setSubPlot(3, 3)

    def thresholding(self):
        plt.suptitle("Thresholding using np.arange() to create the different threshold values", fontsize=14, fontweight='bold')
        
        # Zaladuj zdjecie w Grayscale:
        gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        # Wykresl szare zdjecie:
        self.showImgWithMatplotlib(cv2.cvtColor(gray_image, cv2.COLOR_GRAY2BGR), "img", 1, 'thresh/gray_thresh')
        ima = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2BGR)
        while True:
            cv2.imshow('Zdjecie',self.image)
            if cv2.waitKey(1) == ord('q'):
                break

        ret, thresh = cv2.threshold(gray_image, 70, 255, cv2.THRESH_BINARY) #THRESH_TRUNC

        self.showImgWithMatplotlib(cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR), "img", 2, 'thresh/thresh_' + str(70))

        # tablica z wartosciami od 60 do 130 z krokiem = 10 
        threshold_values = np.arange(start=60, stop=140, step=10)

        # cv2.threshold() z roznymi wartosciami thresholdu zdefinowanych w 'threshold_values'
        thresholded_images = []
        for threshold in threshold_values:
            ret, thresh = cv2.threshold(gray_image, threshold, 255, cv2.THRESH_BINARY)
            thresholded_images.append(thresh)

        # pokaz zdjecia po transformacji:
        for index, (thresholded_image, threshold_value) in enumerate(zip(thresholded_images, threshold_values)):
            self.showImgWithMatplotlib(cv2.cvtColor(thresholded_image, cv2.COLOR_GRAY2BGR), "threshold = " + str(threshold_value),
                                     index + 2, 'thresh/thresh_' + str(threshold_value))

        plt.show()

