import cv2 as cv
from matplotlib import pyplot as plt
from os import getcwd

currentDir = getcwd()

class Device:
    def __init__(self):
        self.subplot_row = 1
        self.subplot_col = 1


    def videoPlayer(self, func):
        """Wyswietla podany plik wideo po transformacji klatek z podanej funkcji func"""
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

    def showImgWithMatplotlib(self, color_img, title, pos, img_name):
        """Metoda wyswietlania zdjec poprzez wygodniejsza biblioteke matplotlib"""
        cv.imwrite(currentDir + '/photos/' + img_name + '.png', color_img)
        img_RGB = color_img[:, :, ::-1]

        ax = plt.subplot(self.subplot_row, self.subplot_col, pos)
        plt.imshow(img_RGB)
        plt.title(title)
        plt.axis('off')

    def setSubPlot(self, rows, cols):
        self.subplot_row = rows
        self.subplot_col = cols
