import sys
import os
import logging
import warnings

from dataHandler import dataHandler
from Invoker import Invoker

import getopt

try:
    if not os.path.exists('data'):
        os.makedirs('data')
except OSError:
    print('Creating directory of data')

class Interface(dataHandler):
    def __init__(self):
        self.something = False
        self.path = ''
        self.window = True
        warnings.filterwarnings("ignore")
        logging.basicConfig(filename='debug.log', level=logging.DEBUG)
        self.invAPI = Invoker()
        self.passingArgs(sys.argv)
        self.media = self.invAPI.camOrPhoto(self.window)

    def passingArgs(self, argv):
        """Podawanie argumentow podanych w konsoli oraz wykonanie odpowiednich funkcji zwiazanych z podanymi parametrami"""
        if __name__ == "__main__":
            arg_help = "{0} -p <path of footage> \n-t <threshold> \n-s <scikit_threshold>".format(argv[0])

            parameters = ["help", "input=", 
                "user=", "output=", "path=", 'threshold', 'scikitThreshold', 'kCluster', 'datahandler', 'apex', 'prediction', 'resize', 'noWindow']

            try:
                opts, args = getopt.getopt(argv[1:], "hi:u:o:", parameters)
            except:
                print("Nieznane parametry. Sprobuj ponownie.")
                print(arg_help)
                sys.exit(2)
            
            for parameter, argument in opts:
                if parameter in ("-h", "--help"):
                    print(arg_help)
                    sys.exit(2)
                elif parameter in ("-p", "--path"):
                    self.path = argument
                    logging.debug(self.path)
                    self.invAPI.setPath(self.path)

                elif parameter in ("-p", "--prediction"):
                    print('Czy motocyklista przygotuje sie do zakretu?')
                    print('Tak')if self.predictCorner() else print('Motocyklista nie przygotuje sie odpowiednio do zakretu')
                elif parameter in ("-t", "--threshold"):
                    print('Wykreslanie zdjec po transformacji threshold')
                    self.threshold()
                elif parameter in ("-s", "--scikitThreshold"):
                    print('Wykreslanie zdjec po transformacji scikitThreshold')
                    self.scikitThreshold()
                elif parameter in ("-k", "--kCluster"):
                    print('Wykreslanie zdjec po transformacji k-means cluster')
                    self.kCluster()
                elif parameter in ("-d", "--datahandler"):
                    print('Zmienianie nazwy plikow w: ', self.path)
                    dataHandler.rename2(self.path)
                elif parameter in ("-r", "--resize"):
                    print('Zmienianie rozdzielczosci plikow w: ', self.path)
                    self.resizeThisDataset(self.path)
                elif parameter in ("--noWindow"):
                    print('Podano parametr noWindow, plik zdjeciowy nie zostanie wypisany przez openCV', self.path)
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

print("Start Aplikacji.")
iface = Interface()
print("Zamkniecie Aplikacji.")
