import cv2 as cv
import sys


#cv.samples.addSamplesDataSearchPath("../images/samples/data")

img = cv.imread("C:/users/Sk4re/engineerka/images/angryman.jpg")

if img is None:
    sys.exit("Could not read the image.")

cv.imshow("Display window", img)
k = cv.waitKey(0)

if k == ord("s"):
    cv.imwrite("angryman.png", img)

