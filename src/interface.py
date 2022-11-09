import sys
import os
import logging

from matplotlib import image
from dataHandler import dataHandler
from pathlib import Path
from mainAPI import mainAPI

import getopt

try:
    if not os.path.exists('data'):
        os.makedirs('data')
except OSError:
    logging.error('Creating directory of data')

class Interface(dataHandler):
    def __init__(self):
        self.something = False
        self.path = ''
        self.API = mainAPI()
        self.passing_args(sys.argv)
        self.API.camOrPhoto()
        self.log = logging.getLogger("BRUH")

    def passing_args(self, argv):
        if __name__ == "__main__":
            arg_help = "{0} -p <path of footage> \n-t <threshold> \n-s <scikit_threshold>".format(argv[0])
            
            try:
                opts, args = getopt.getopt(argv[1:], "hi:u:o:", ["help", "input=", 
                "user=", "output=", "path=", 'threshold', 'scikitThreshold', 'clahe', 'kCluster', 'contour', 'datahandler'])
            except:
                print("Nieznane parametry. Sprobuj ponownie.")
                print(arg_help)
                sys.exit(2)
            
            for opt, arg in opts:
                if opt in ("-h", "--help"):
                    print(arg_help)
                    sys.exit(2)
                elif opt in ("-p", "--path"):
                    self.path = arg
                    print(self.path)
                    self.API.setPath(self.path)

                elif opt in ("-t", "--threshold"):
                    print(self.thresholdThisPicture())
                    
                elif opt in ("-s", "--scikitThreshold"):
                    print(self.scikitThresholdThisPicture())

                elif opt in ("-c", "--clahe"):
                    print("clahe placeholder")
                elif opt in ("-k", "--kCluster"):
                    print(self.kClusterThisPicture())
                    print("kCluster placeholder")
                elif opt in ("-tc", "--contour"):
                    print(self.thresholdToContourThisPicture())
                    print("contour placeholder") 
                elif opt in ("-d", "--datahandler"):
                    dataHandler.rename2(self.path)

    def thresholdThisPicture(self):
        return self.API.threshold()

    def scikitThresholdThisPicture(self):
        return self.API.scikitThreshold()

    def thresholdToContourThisPicture(self):
        return self.API.thresholdToContour()

    def kClusterThisPicture(self):
        return self.API.kCluster()

    def cropThisDataset(self, inputPath, outputPath):
        pass #TODO

iface = Interface()
