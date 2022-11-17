from Device import Device
import sys  
import cv2 as cv
import os
import numpy as np
from matplotlib import pyplot as plt

from pathlib import Path
import logging

class photoCamera(Device):
    def __init__(self, imagePath):
        self.cap = None
        self.ret = None
        self.frame = None
        self.connect_output(imagePath)

    def connect_output(self, imagePath):
        self.frame = cv.imread(imagePath)
     
        import cornerAPI
        dupa = cornerAPI.Corners(imagePath)
        dupa.predApex()

        dupa.drawTrajectory(dupa.returnTrajectoryPoints, self.frame)

        dupa.drawTrajectory(dupa.returnTrajectory, self.frame)

        dupa.drawTrajectory(dupa.returnPolyTrajectory, self.frame)


        # x, y = dupa.returnTrajectoryPoints()

        # verts = np.array(list(zip(y, x)))
        # cv.polylines(self.frame,np.int32([verts]),False,(0,200,255),thickness=3)


        # x, y = dupa.returnTrajectory()

        # verts = np.array(list(zip(x, y)))
        # cv.polylines(self.frame,np.int32([verts]),False,(80,180,180),thickness=3)

        # x, y = dupa.returnPolyTrajectory()

        # verts = np.array(list(zip(x, y)))
        # cv.polylines(self.frame,np.int32([verts]),False,(0,180,180),thickness=3)

        logging.warning("Otwarto polaczenie.")
        while True:
            cv.imshow('Zdjecie',self.frame)

            if cv.waitKey(1) == ord('q'):
                break


        # if self.cap.isOpened():
        #     logging.warning("Otwarto polaczenie.")