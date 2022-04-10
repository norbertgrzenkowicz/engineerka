import numpy as np
import cv2
import os

try:
    if not os.path.exists('data'):
        os.makedirs('data')

except OSError:
    print('Error: Creating directory of data')

inputImage = cv2.imread("data\blind_curve\supermoto_evening_mask24.jpg")
minLineLength = 30
maxLineGap = 5
lines = cv2.HoughLinesP(inputImage,cv2.HOUGH_PROBABILISTIC, np.pi/180, 30, minLineLength,maxLineGap)
for x in range(0, len(lines)):
    for x1,y1,x2,y2 in lines[x]:
        #cv2.line(inputImage,(x1,y1),(x2,y2),(0,128,0),2, cv2.LINE_AA)
        pts = np.array([[x1, y1 ], [x2 , y2]], np.int32)
        cv2.polylines(inputImage, [pts], True, (0,255,0))

font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(inputImage,"Tracks Detected", (500, 250), font, 0.5, 255)
cv2.imshow("Trolley_Problem_Result", inputImage)
cv2.imshow('edge', inputImage)
cv2.waitKey(0)