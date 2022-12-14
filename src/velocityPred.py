import numpy as np
import logging
from math import floor

class velocityPred():
    def __init__(self, currentVel = 120, desiredVel = 70, calibrationList = [], apexPoint = (0, 0)):
        self.g = 9.81

        self.maxbf = 0.52 * self.g
        self.normbf = 0.12 * self.g

        self.lengthToApex = 0
        self.apexPoint = apexPoint[0]

        self.vel = currentVel / 3.6
        self.vel2 = desiredVel / 3.6

        self.timeToApply = 0.75

        self.lToApply = 0.75 * self.vel
        self.lToSlowDown = 0
        self.calcLength(calibrationList)
        self.calcLengthToSlowDown(self.normbf)

    def calcLengthToSlowDown(self, brakeForce):
        """Rownanie matematyczne obliczenia odleglosci do wyhamowania przy danej predkosci i sile hamowania"""
        self.lToSlowDown = self.lToApply + self.vel**2 / (self.vel2**2 + 2 * brakeForce)
        print(f'Odleglosc do zatrzymania sie do predkosci {round(self.vel2 * 3.6)} rozpoczynajac od {round(self.vel * 3.6)}(km/h):  {round(self.lToSlowDown)}\n')

    def canWeSlowDown(self):
        """Porownuje i zwraca wynik z porownania odleglosci do szczytu zakretu i odleglosci do wyhamowania"""
        return self.lToSlowDown < self.lengthToApex

    def calcLength(self, cal):
        """Obliczenie odleglosci do szczytu zakretu z pomocą bisekcji w poszukiwaniu indeksu w zmiennej cal bedacego szczytem zakretu"""
        cal = cal[::-1]
        from bisect import bisect
        index = bisect(cal, self.apexPoint)


        if index > 0 and index < len(cal):
            pixelLengthBetween = cal[index] - cal[index-1]
            pixelLengthTo = self.apexPoint - cal[index-1]
            # logging.debug('pixelLengthBetween: ',int(pixelLengthBetween), int(pixelLengthTo))
            # logging.debug('pixelLengthTo: ', int(pixelLengthTo))
            self.lengthToApex = - pixelLengthTo / pixelLengthBetween * 10 + 10 * (len(cal) - index + 1)
        elif index < 1:
            self.lengthToApex = 60
        else:
            self.lengthToApex = 10

        cal = cal[::-1]

        print(f'Odleglosc pojazdu do szczytu zakretu: {round(self.lengthToApex)}\n')

