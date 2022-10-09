import numpy as np
import cv2
import os

import Device as Device


class curveDetection(Device):
    def __init__(self, imagePath):
        self.inputImage = cv2.imread(imagePath, cv2.IMREAD_GRAYSCALE)
        self.minLineLength = 30
        self.maxLineGap = 5
        self.houghing()

    def houghing(self):
        lines = cv2.HoughLinesP(self.inputImage,cv2.HOUGH_PROBABILISTIC, np.pi/180, 30, self.minLineLength,self.maxLineGap)
        for x in range(0, len(lines)):
            for x1,y1,x2,y2 in lines[x]:
                cv2.line(self.inputImage,(x1,y1),(x2,y2),(0,128,0),2, cv2.LINE_AA)
                pts = np.array([[x1, y1 ], [x2 , y2]], np.int32)
                # cv2.polylines(inputImage, [pts], True, (0,255,0))
    


# captured_canny()

# # font = cv2.FONT_HERSHEY_SIMPLEX
# # cv2.putText(inputImage,"Tracks Detected", (500, 250), font, 0.5, 255)
# # cv2.imshow("Trolley_Problem_Result", inputImage)
# # cv2.imshow('edge', inputImage)
# cv2.waitKey(0)