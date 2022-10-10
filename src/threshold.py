"""
Simple thresholding applied to a real image using np.arange() to create the different threshold values
"""

# Import required packages:

from cv2 import threshold
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

    def thresholding(self):
        # Create the dimensions of the figure and set title and color:
        plt.suptitle("Thresholding using np.arange() to create the different threshold values", fontsize=14, fontweight='bold')
        
        # Load the image and convert it to grayscale:
        gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        # Plot the grayscale images and the histograms:
        # self.show_img_with_matplotlib(cv2.cvtColor(gray_image, cv2.COLOR_GRAY2BGR), "img", 1)
        ima = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2BGR)
        while True:
            cv2.imshow('Zdjecie',self.frame)
            if cv2.waitKey(1) == ord('q'):
                break

        ret, thresh = cv2.threshold(gray_image, 70, 255, cv2.THRESH_BINARY) #THRESH_TRUNC

        self.show_img_with_matplotlib(cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR), "img", 2)

        # Get the array with the values for thresholding in the range [60-130] with step 10:
        # This function returns an array of evenly spaced values:
        threshold_values = np.arange(start=60, stop=140, step=10)
        # print(threshold_values)

        # Apply cv2.threshold() with the different threshold values defined in 'threshold_values'
        thresholded_images = []
        for threshold in threshold_values:
            ret, thresh = cv2.threshold(gray_image, threshold, 255, cv2.THRESH_BINARY)
            thresholded_images.append(thresh)

        # Show the thresholded images:
        # for index, (thresholded_image, threshold_value) in enumerate(zip(thresholded_images, threshold_values)):
            # show_img_with_matplotlib(cv2.cvtColor(thresholded_image, cv2.COLOR_GRAY2BGR), "threshold = " + str(threshold_value),
                                    #  index + 2)

        # Show the Figure:
        plt.show()

        return "ther is going to be thresholded image path! in near future..."
        # return 
