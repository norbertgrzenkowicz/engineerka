import sys
import os
import logging

from matplotlib import image
from dataHandler import dataHandler
from Invoker import Invoker

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
        self.window = True
        self.invAPI = Invoker()
        self.passingArgs(sys.argv)
        self.media = self.invAPI.camOrPhoto(self.window)
        self.log = logging.getLogger("BRUH")

    def passingArgs(self, argv):
        """Podawanie argumentow podanych w konsoli oraz wykonanie odpowiednich funkcji zwiazanych z podanymi parametrami"""
        if __name__ == "__main__":
            arg_help = "{0} -p <path of footage> \n-t <threshold> \n-s <scikit_threshold>".format(argv[0])

            parameters = ["help", "input=", 
                "user=", "output=", "path=", 'threshold', 'scikitThreshold', 'kCluster', 'datahandler', 'apex', 'prediction', 'resize', 'noWindow']

            try:
                opts, args = getopt.getopt(argv[1:], "hi:u:o:", parameters)
            except:
                logging.error("Nieznane parametry. Sprobuj ponownie.")
                logging.info(arg_help)
                sys.exit(2)
            
            for parameter, argument in opts:
                if parameter in ("-h", "--help"):
                    logging.info(arg_help)
                    sys.exit(2)
                elif parameter in ("-p", "--path"):
                    self.path = argument
                    logging.debug(self.path)
                    self.invAPI.setPath(self.path)

                elif parameter in ("-p", "--prediction"):
                    logging.info(self.predictCorner())
                elif parameter in ("-t", "--threshold"):
                    self.threshold()
                elif parameter in ("-s", "--scikitThreshold"):
                    self.scikitThreshold()
                elif parameter in ("-k", "--kCluster"):
                    self.kCluster()
                elif parameter in ("-d", "--datahandler"):
                    dataHandler.rename2(self.path)
                elif parameter in ("-r", "--resize"):
                    self.resizeThisDataset(self.path)
                elif parameter in ("--noWindow"):
                    self.window = False

    def predictCorner(self):
        """Predykcja zdjec"""
        canWeSlowDown = self.invAPI.predictPhoto()
        return canWeSlowDown

    def threshold(self):
        self.invAPI.threshold()

    def scikitThreshold(self):
        self.invAPI.scikitThreshold()

    def kCluster(self):
        self.invAPI.kCluster()

    def cropThisDataset(self, inputPath):
        self.invAPI.cropDataset(inputPath)

    def resizeThisDataset(self, inputPath):
        self.invAPI.resizeDataset(inputPath)

iface = Interface()
