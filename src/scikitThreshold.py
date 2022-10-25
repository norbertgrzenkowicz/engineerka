"""
Thresholding example (Otsu's binarization algorithm) using scikit-image
"""

# Import required packages:
import cv2
import matplotlib.pyplot as plt
from skimage.filters import (threshold_otsu, threshold_triangle, threshold_niblack, threshold_sauvola)
from skimage import img_as_ubyte
from threshold import Threshold

class scikitThreshold(Threshold):
    def __init__(self, imagePath):
        self.image = cv2.imread(imagePath)
        self.gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.setSubPlot(3, 3)
        self.figging()

    def figging(self):
        # Create the dimensions of the figure and set title:
        fig = plt.figure(figsize=(12, 8))
        plt.suptitle("Thresholding scikit-image (Otsu, Triangle, Niblack, Sauvola)", fontsize=14, fontweight='bold')
        fig.patch.set_facecolor('silver')

    def calcHist(self):
        # Calculate histogram (only for visualization):
        self.hist = cv2.calcHist([self.gray_image], [0], None, [256], [0, 256])

    def someAlgos(self):
                
        # Trying Otsu's scikit-image algorithm:
        thresh_otsu = threshold_otsu(self.gray_image)
        binary_otsu = self.gray_image > thresh_otsu
        binary_otsu = img_as_ubyte(binary_otsu)

        # Trying Niblack's scikit-image algorithm:
        thresh_niblack = threshold_niblack(self.gray_image, window_size=25, k=0.8)
        binary_niblack = self.gray_image > thresh_niblack
        binary_niblack = img_as_ubyte(binary_niblack)

        # Trying Sauvola's scikit-image algorithm:
        thresh_sauvola = threshold_sauvola(self.gray_image, window_size=25)
        binary_sauvola = self.gray_image > thresh_sauvola
        binary_sauvola = img_as_ubyte(binary_sauvola)

        # Trying triangle scikit-image algorithm:
        thresh_triangle = threshold_triangle(self.gray_image)
        binary_triangle = self.gray_image > thresh_triangle
        binary_triangle = img_as_ubyte(binary_triangle)

        # Plot all the images:
        self.show_img_with_matplotlib(self.image, "image", 1)
        self.show_img_with_matplotlib(cv2.cvtColor(self.gray_image, cv2.COLOR_GRAY2BGR), "gray img", 2)
        self.show_img_with_matplotlib(cv2.cvtColor(binary_otsu, cv2.COLOR_GRAY2BGR), "Otsu's binarization (scikit-image)", 3)
        self.show_img_with_matplotlib(cv2.cvtColor(binary_triangle, cv2.COLOR_GRAY2BGR), "Triangle binarization (scikit-image)", 4)
        self.show_img_with_matplotlib(cv2.cvtColor(binary_niblack, cv2.COLOR_GRAY2BGR), "Niblack's binarization (scikit-image)", 5)
        self.show_img_with_matplotlib(cv2.cvtColor(binary_sauvola, cv2.COLOR_GRAY2BGR), "Sauvola's binarization (scikit-image)", 6)

        # Show the Figure:
        plt.show()

    def scikitThresholding(self):
        self.calcHist()
        self.someAlgos()

        return "path in future"