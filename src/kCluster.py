import cv2
import numpy as np
from matplotlib import pyplot as plt
import Device

from skimage.filters import threshold_otsu

class kCluster(Device): # TODO: KWARGS, ARGS
    def __init__(self, imagePath):
        self.img = cv2.imread(imagePath)
        self.img_rgb=cv2.cvtColor(self.img,cv2.COLOR_BGR2RGB)
        self.img_gray=cv2.cvtColor(self.img_rgb,cv2.COLOR_RGB2GRAY)

    def color_quantization(self, image, k):
        """Performs color quantization using K-means clustering algorithm"""

        # Transform image into 'data':
        data = np.float32(image).reshape((-1, 3))
        # print(data.shape)

        # Define the algorithm termination criteria (the maximum number of iterations and/or the desired accuracy):
        # In this case the maximum number of iterations is set to 20 and epsilon = 1.0
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)

        # Apply K-means clustering algorithm:
        ret, label, center = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

        # At this point we can make the image with k colors
        # Convert center to uint8:
        center = np.uint8(center)
        # Replace pixel values with their center value:
        result = center[label.flatten()]
        result = result.reshape(self.img.shape)
        return result

    def figgin(self):
        fig = plt.figure(figsize=(16, 8))
        plt.suptitle("Color quantization using K-means clustering algorithm", fontsize=14, fontweight='bold')
        fig.patch.set_facecolor('silver')

    def imagging(self):
        img_rgb=cv2.cvtColor(self.img,cv2.COLOR_BGR2RGB)
        img_gray=cv2.cvtColor(img_rgb,cv2.COLOR_RGB2GRAY)

    def filter_image(self, image, mask):
        r = image[:,:,0] * mask
        g = image[:,:,1] * mask
        b = image[:,:,2] * mask
        return np.dstack([r,g,b])

    def iDunno(self):
        thresh = self.threshold_otsu(self.img_gray)
        img_otsu  = self.img_gray < thresh
        filtered = self.filter_image(self.img, img_otsu)

    def plottin(self):
        # Plot the images:
        self.show_img_with_matplotlib(self.img, "original image", 1)
        # show_img_with_matplotlib(color_3, "color quantization (k = 3)", 2)
        # show_img_with_matplotlib(color_5, "color quantization (k = 5)", 3)
        self.color_quantizationshow_img_with_matplotlib(self.filtered, "color quantization (k = 5)", 2)
        # show_img_with_matplotlib(color_20, "color quantization (k = 20)", 5)
        # show_img_with_matplotlib(color_40, "color quantization (k = 40)", 6)

        # Show the Figure:
        plt.show()
# Apply color quantization:
# color_3 = color_quantization(img, 3)
# color_5 = color_quantization(img, 5)
# color_11 = color_quantization(img,  10)
# color_10 = color_quantization(img, 4)
# color_20 = color_quantization(img, 20)
# color_40 = color_quantization(img, 40)




