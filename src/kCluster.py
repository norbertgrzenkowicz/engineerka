import cv2
import numpy as np
from matplotlib import pyplot as plt
from Device import Device

from skimage.filters import threshold_otsu

class kCluster(Device):
    def __init__(self, imagePath):
        self.img = cv2.imread(imagePath)
        self.img_rgb=cv2.cvtColor(self.img,cv2.COLOR_BGR2RGB)
        self.img_gray=cv2.cvtColor(self.img_rgb,cv2.COLOR_RGB2GRAY)
        self.filtered = None
        self.setSubPlot(2, 2)
        self.figgin()
        self.imaging()

    def color_quantization(self, image, k):
        """Kwantyzacja kolorow za pomoca algorytmu K-means clustering"""

        # Transformacja zdjecia w macierz 'data':
        data = np.float32(image).reshape((-1, 3))

        # Zdefiniuj kryteria terminacji algorytmu(maksymalna liczba iteracju lub porzadana precyzja)
        # W tym przypadku maksymalna liczba iteracje jest 20 oraz epsilon = 1.0
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)

        # Zastosuj K-means clustering algorytm
        ret, label, center = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

        # Teraz mozna przejsc z danych do zdjecia
        # Skonwertuj center do uint8
        center = np.uint8(center)
        # Zamine wartosci pikseli z ich wycentrowanymi wartosciami
        result = center[label.flatten()]
        result = result.reshape(self.img.shape)
        return result

    def figgin(self):
        fig = plt.figure(figsize=(16, 8))
        plt.suptitle("Kwantyzacja kolorow uzywajac K-means clustering algorytm", fontsize=14, fontweight='bold')
        fig.patch.set_facecolor('silver')

    def imaging(self):
        img_rgb=cv2.cvtColor(self.img,cv2.COLOR_BGR2RGB)
        img_gray=cv2.cvtColor(img_rgb,cv2.COLOR_RGB2GRAY)

    def filter_image(self, image, mask):
        r = image[:,:,0] * mask
        g = image[:,:,1] * mask
        b = image[:,:,2] * mask
        return np.dstack([r,g,b])

    def iDunno(self):
        thresh = threshold_otsu(self.img_gray)
        img_otsu  = self.img_gray < thresh
        self.filtered = self.filter_image(self.img, img_otsu)

    def plottin(self):
        color_3 = self.color_quantization(self.img, 3)
        color_5 = self.color_quantization(self.img, 5)
        # color_11 = self.color_quantization(self.img,  10)
        # color_10 = self.color_quantization(self.img, 4)
        # color_20 = self.color_quantization(self.img, 20)
        # color_40 = self.color_quantization(self.img, 40)

        self.showImgWithMatplotlib(self.img, "Oryginalne zdjecie", 1, 'kcluster/org_kcluster')
        self.showImgWithMatplotlib(color_3, "Kwantyzacja kolorow (k = 3)", 2, 'kcluster/k3cluster')
        self.showImgWithMatplotlib(color_5, "Kwantyzacja kolorow (k = 5)", 3, 'kcluster/k5cluster')
        # self.showImgWithMatplotlib(self.filtered, "Kwantyzacja kolorow (k = 5)", 2)
        # self.showImgWithMatplotlib(color_20, "Kwantyzacja kolorow (k = 20)", 2)
        # self.showImgWithMatplotlib(color_40, "Kwantyzacja kolorow (k = 40)", 3)

        plt.show()
    
    def kClustering(self):
        self.iDunno()
        self.plottin()
