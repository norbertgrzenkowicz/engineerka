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
        self.vel = 120
        self.window = True
        warnings.filterwarnings("ignore")
        logging.basicConfig(filename='debug.log', level=logging.DEBUG)
        self.invAPI = Invoker()
        self.passingArgs(sys.argv)
        self.media = self.invAPI.camOrPhoto(self.window)

    def passingArgs(self, argv):
        """Podawanie argumentow podanych w konsoli oraz wykonanie odpowiednich funkcji zwiazanych z podanymi parametrami"""
        if __name__ == "__main__":
            arg_help = "Przykladowe uzycie komendy:\n\n   {0} -path=<sciezka zdjecia> --threshold \n\n  Komendy:\n\n      help                   - wydrukowanie tresci pomocy \n\n      path=<sciezka medium>  - podanie sciezki do zdjecia\n\n      threshold              - wykonanie progowania globalnego \n\n      scikitThreshold        - wykonanie progowania globalnego i lokalnego\n\n      kCluster               - wykonanie algorytmu kmeans cluster \n\n      datahandler            - zamiana nazwy plikow z podanej sciezki w path \n\n      prediction             - wykonanie predykcji trajektorii ruchu i predkosci \n\n      resize                 - zmiana rozdzielczosci plikow w podanej sciezce bazy danych w path \n\n      noWindow               - blokuje wypisanie zdjecia na ekran za pomoca OpenCV\n".format(argv[0])

            parameters = ["help", "input=", 
                "user=", "output=", "path=", 'threshold', 'scikitThreshold', 'kCluster', 'datahandler', 'prediction=', 'resize', 'noWindow']

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
                elif parameter in ("--prediction"):
                    self.vel = int(argument)
                    print(f'Czy motocyklista przygotuje sie do zakretu jadac z predkoscia {self.vel}?\n')
                    if self.predictCorner():
                        print('Tak, motocyklista przygotuje sie odpowiednio do zakretu.\n')
                    else: 
                        print('Motocyklista nie przygotuje sie odpowiednio do zakretu.\n')

                if parameter in ("--noWindow"):
                    print('Podano parametr noWindow, plik zdjeciowy nie zostanie wypisany przez openCV\n', self.path)
                    self.window = False
                # elif parameter in ("--prediction"):
                #     print('Czy motocyklista przygotuje sie do zakretu?')
                #     self.vel = int(argument)
                #     if self.predictCorner():
                #         print('Tak, motocykla przygotuje sie odpowiednio do zakretu.')
                #     else: 
                #         print('Motocyklista nie przygotuje sie odpowiednio do zakretu')

                elif parameter in ("--threshold"):
                    print('Wykreslanie zdjec po transformacji threshold')
                    self.invAPI.threshold()
                elif parameter in ("--scikitThreshold"):
                    print('Wykreslanie zdjec po transformacji scikitThreshold')
                    self.invAPI.scikitThreshold()
                elif parameter in ("--kCluster"):
                    print('Wykreslanie zdjec po transformacji k-means cluster')
                    self.invAPI.kCluster()
                elif parameter in ("--datahandler"):
                    print('Zmienianie nazwy plikow w: ', self.path)
                    dataHandler.renameDict(self.path)
                elif parameter in ("--crop"):
                    print('Zmienianie rozdzielczosci plikow w: ', self.path)
                    self.invAPI.cropThisDataset(self.path)

    def predictCorner(self):
        """Predykcja zdjec"""
        canWeSlowDown = self.invAPI.predictPhoto(self.vel)
        return canWeSlowDown

    def threshold(self):
        self.invAPI.threshold()

    def scikitThreshold(self):
        self.invAPI.scikitThreshold()

    def kCluster(self):
        self.invAPI.kCluster()

    def cropThisDataset(self, inputPath):
        self.invAPI.cropDataset(inputPath)


print("Start Aplikacji.")
iface = Interface()
print("Zamkniecie Aplikacji.")
