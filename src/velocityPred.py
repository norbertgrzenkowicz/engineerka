import numpy as np

class velocityPred():
    def __init__(self, currentVel = 50, desiredVel = 20, calibrationList = [], apexPoint = (0, 0)):
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
        self.lToSlowDown = self.lToApply + self.vel**2 / (self.vel2**2 + 2 * brakeForce)

    def canWeSlowDown(self):
        return self.lToSlowDown > self.lengthToApex

    def calcLength(self, cal):
        from bisect import bisect

        cal = cal[::-1]

        from bisect import bisect
        index = bisect(cal, self.apexPoint)

        if index > 0 and index < len(cal):
            pixelLengthBetween = cal[index] - cal[index-1]
            pixelLengthTo = self.apexPoint - cal[index-1]
            print(pixelLengthBetween, pixelLengthTo)
            self.lengthToApex = - pixelLengthTo / pixelLengthBetween * 10 + 10 * (len(cal) - index + 1)
        elif index < 1:
            self.lengthToApex = 60
        else:
            self.lengthToApex = 10

        cal = cal[::-1]

