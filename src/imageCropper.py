1
	# Import packages

import cv2
import numpy as np
import os

class imageCropper:
    def __init__(self, inputPath, outputPath):
        self.inputPath = inputPath
        self.outputPath = outputPath
        self.pathList = os.listdir(inputPath)

    def CropData(self):
        for image in self.pathList:
            print('inputImage:', self.inputPath + '/' + image)
            img = cv2.imread(self.inputPath + '/' + image)
            cropped_image = img[500:800, :]
            # resized = cv2.resize(cropped_image, (1920, 1000), interpolation = cv2.INTER_AREA)
            cv2.imwrite(self.outputPath + '/' + image, cropped_image)

        cv2.waitKey(0)
        cv2.destroyAllWindows()