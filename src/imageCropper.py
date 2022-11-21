1
	# Import packages

import cv2
import numpy as np
import os

class imageCropper:
    def __init__(self, inputPath):
        self.inputPath = inputPath
        self.outputPath = self.inputPath
        self.pathList = os.listdir(inputPath)

    def CropData(self):
        pass
        # for image in self.pathList:

            # print('inputImage:', self.inputPath + '/' + image)
            # img = cv2.imread(self.inputPath + '/' + image)
            # cropped_image = img[500:800, :]
            # # resized = cv2.resize(cropped_image, (1920, 1000), interpolation = cv2.INTER_AREA)
            # cv2.imwrite(self.outputPath + '/' + image, cropped_image)

    def resizeData(self):
        for image in self.pathList:
            img = cv2.imread(self.inputPath + '/' + image)
            print('Original Dimensions : ',img.shape)
        
            scale_percent = 35 # percent of original size
            scale_percent2 = 35
            width = int(img.shape[1] * scale_percent2 / 100)
            height = int(img.shape[0] * scale_percent2 / 100)
            dim = (width, height)
            
            # resize image
            resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
            cv2.imwrite(self.outputPath + '/' + image, resized)
