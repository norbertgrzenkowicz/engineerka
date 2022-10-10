from abc import abstractmethod
import sys  
import cv2 as cv
import os
import numpy as np
from matplotlib import pyplot as plt
import logging # TODO: passing logging next please

# print(cv.__version__)
# print(sys.version)
# print (sys.executable)

class Device:
    def __init__(self):
        pass

    def video_player(self, func):
        while True:
            # capture frame-by-frame
            self.ret, self.frame = self.cap.read()        
            
            if not self.ret:
            #if frame is read correctly ret is True
                ("Cant receive frame (stream end?). Exiting..")
                break

            media_output = func()

            #display the resulting frame
            cv.imshow('frame', media_output)            
            if cv.waitKey(1) == ord('q'):
                break
            
        self.cap.release()
        cv.destroyAllWindows()

    def show_img_with_matplotlib(self, color_img, title, pos):
        """Shows an image using matplotlib capabilities"""

        # Convert BGR image to RGB
        img_RGB = color_img[:, :, ::-1]

        ax = plt.subplot(1, 3, pos)
        plt.imshow(img_RGB)
        plt.title(title)
        plt.axis('off')

# gopro_footage = Camera()
# gopro_footage.video_player(gopro_footage.captured_canny)
# gopro_footage.captured_canny()
