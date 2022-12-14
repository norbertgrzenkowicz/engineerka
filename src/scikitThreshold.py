import cv2
import matplotlib.pyplot as plt
from skimage.filters import (threshold_otsu, threshold_triangle, threshold_niblack, threshold_sauvola)
from skimage import img_as_ubyte
from threshold import Threshold

class scikitThreshold(Threshold):
    def __init__(self, imagePath):
        self.image = cv2.imread(imagePath)
        self.gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.setSubPlot(2, 3)
        self.figging()

    def figging(self):
        fig = plt.figure(figsize=(12, 8))
        plt.suptitle("scikitThreshold (Otsu, Triangle, Niblack, Sauvola)", fontsize=14, fontweight='bold')
        fig.patch.set_facecolor('silver')

    def calcHist(self):
        # kalkulacja histogramu
        self.hist = cv2.calcHist([self.gray_image], [0], None, [256], [0, 256])

    def useScikitThresholds(self):
                
        # Otsu's scikit-image algorytm:
        thresh_otsu = threshold_otsu(self.gray_image)
        binary_otsu = self.gray_image > thresh_otsu
        binary_otsu = img_as_ubyte(binary_otsu)

        # Niblack's scikit-image algorytm:
        thresh_niblack = threshold_niblack(self.gray_image, window_size=25, k=0.8)
        binary_niblack = self.gray_image > thresh_niblack
        binary_niblack = img_as_ubyte(binary_niblack)

        # Sauvola's scikit-image algorytm:
        thresh_sauvola = threshold_sauvola(self.gray_image, window_size=25)
        binary_sauvola = self.gray_image > thresh_sauvola
        binary_sauvola = img_as_ubyte(binary_sauvola)

        # triangle scikit-image algorytm:
        thresh_triangle = threshold_triangle(self.gray_image)
        binary_triangle = self.gray_image > thresh_triangle
        binary_triangle = img_as_ubyte(binary_triangle)

        # Wykreslanie wynikow:
        self.showImgWithMatplotlib(self.image, "Oryginalne zdjecie", 1, 'scikit/org_sck_thresh')
        self.showImgWithMatplotlib(cv2.cvtColor(self.gray_image, cv2.COLOR_GRAY2BGR), "Szare zdjecie", 2, 'scikit/org_gray_sck_thresh')
        self.showImgWithMatplotlib(cv2.cvtColor(binary_otsu, cv2.COLOR_GRAY2BGR), "Binarizacja Otsu (scikit-image)", 3, 'scikit/otsu_sck_thresh')
        self.showImgWithMatplotlib(cv2.cvtColor(binary_triangle, cv2.COLOR_GRAY2BGR), "Binarizacja Triangle (scikit-image)", 4, 'scikit/traingle_sck_thresh')
        self.showImgWithMatplotlib(cv2.cvtColor(binary_niblack, cv2.COLOR_GRAY2BGR), "Binarizacja Niblack (scikit-image)", 5, 'scikit/niblack_sck_thresh')
        self.showImgWithMatplotlib(cv2.cvtColor(binary_sauvola, cv2.COLOR_GRAY2BGR), "Binarizacja Sauvola (scikit-image)", 6, 'scikit/sauvola_sck_thresh')

        plt.show()

    def scikitThresholding(self):
        self.calcHist()
        self.useScikitThresholds()