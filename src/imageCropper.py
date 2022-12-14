1
	# Import packages

import cv2
import os
import logging

class imageCropper:
    def __init__(self, inputPath):
        self.inputPath = inputPath
        self.outputPath = self.inputPath
        self.pathList = os.listdir(inputPath)

    def CropData(self):
        """Zmniejsz rozdzielczosc poprzez uciecie danego fragmentu cropped_image"""
        for image in self.pathList:

            print('inputImage:', self.inputPath + '/' + image)
            img = cv2.imread(self.inputPath + '/' + image)
            cropped_image = img[1000:, :]
            cv2.imwrite(self.outputPath + '/' + image, cropped_image)
