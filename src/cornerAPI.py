import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from random import randint

class Corners():
    def __init__(self, mediaPath):
        self.mediaPath = mediaPath
        self.img = cv2.imread(mediaPath)

        self.polyRank = 6
        self.listOfCords = []
        self.isRight = True

        self.leftSide = []
        self.rightSide = []

        self.leftPointsList = []
        self.rightPointsList = []
        self.xLeft = []
        self.yLeft = []
        self.xRight = []
        self.yRight = []

        self.apex = ()

        self.xT = []
        self.yT = []

        self.trajectoryCoeffs = []

        self.polyTrajectory = None

        self.trajectory = None
        self.trajectoryLane = None

    def definePoints(self):
        edges = cv2.Canny(self.img, 100, 255)
        indices = np.where(edges != [0])
        coordinates = zip(indices[0], indices[1])
        self.list_of_cords = list(coordinates)
    
        # self.list_of_cords = self.list_of_cords[::5] # Wyrzucenie co piątego elementu listu w celu zmniejszenia ilości punktów do przetworzenia

        # for i, cord in enumerate(self.list_of_cords):
        #     if cord[0] > 750:
        #         self.list_of_cords.pop(i) 
      
    def whichSide(self):
        _ , prev = self.list_of_cords[-1]

        for i in self.list_of_cords[::-1]:
            if abs(prev - i[1]) > 40 and prev > i[1]:
                self.isRight = False
            elif abs(prev - i[1]) > 40 and prev < i[1]:
                self.isRight = True

            prev = i[1]
            self.rightPointsList.append(i) if self.isRight else self.leftPointsList.append(i)

        for point in self.leftPointsList:
            self.xLeft.append(point[0])
            self.yLeft.append(point[1])

        for point in self.rightPointsList:
            self.xRight.append(point[0])
            self.yRight.append(point[1])

        if self.xRight[0] > self.xLeft[0]:
            self.reducingLengths()
        elif self.xRight[0] < self.xLeft[0]:
            self.reducingLengths()
 

    def reducingLengths(self):
        for i in range(len(self.xRight)):
            if self.xRight[i] in self.xLeft:
                last = i
                break
        self.xRight = self.xRight[last:]
        self.yRight = self.yRight[last:]


    def fittedCurvePoints(self):

        cordX = list(zip(self.xRight, self.yRight))
        cordY = list(zip(self.xLeft, self.yLeft))

        cordX, _, Y = self.removeDuplicates(cordX)
        cordY, _, Y = self.removeDuplicates(cordY)


        cordX, cordY = self.cutLongerList(cordX, cordY)

        assert len(cordX) == len(cordY)

        wideness = []

        beginplace = 0.7
        endplace2 = 0.7
        beginplace2 = 0.7
        endplace = 0.1

        for i in range(len(cordX)):
            wideness.append(cordX[i][1] - cordY[i][1])
        
        wideness = np.array(wideness)

        assert self.apex != ()

        import math

        apexI = math.floor(self.apex[0])

        for i, cord in enumerate(cordX):
            if apexI == cord[0]:
                cornerIndex = i
        
        cornerStart = len(cordX) - cornerIndex

        sideness = np.linspace(beginplace,endplace2,len(cordX) - cornerStart)
        sidenessCorner = np.linspace(beginplace2,endplace, cornerStart)
        sideness = np.append(sideness, sidenessCorner)

        traj = list(zip(_, sideness * wideness + Y))

        for point in traj:
            self.xT.append(point[0])
            self.yT.append(point[1])

    def cutLongerList(self, listX, listY):

        toCut = abs(len(listX) - len(listY))
        if len(listX) > len(listY):
            listX = listX[:-toCut]
        elif len(listX) > len(listY):
            listY = listY[:-toCut]
        return listX, listY

    def removeDuplicates(self, list):
        x = list[0][0]
        indexes = []
        xcords = []
        ycords = []
        for i, value in enumerate(list):
            if x != list[i][0]:
                x = list[i][0]
                indexes.append(value)
                xcords.append(value[0])
                ycords.append(value[1])
        return indexes, xcords, ycords

    def fittingCurve(self):

        leftLine = np.linspace(min(self.xLeft),max(self.xLeft),300).reshape(-1,1)
        rightLine = np.linspace(min(self.xRight),max(self.xRight),300).reshape(-1,1)

        fittedPolynomialLeft = np.polyfit(self.xLeft, self.yLeft, self.polyRank)
        fittedPolynomialRight = np.polyfit(self.xRight, self.yRight, self.polyRank)

        for i in range(self.polyRank + 1):
            self.trajectoryCoeffs.append((fittedPolynomialLeft[i] + fittedPolynomialRight[i]) / 2)

        print('coeffs to left polynomial:\n', fittedPolynomialLeft)
        print('coeffs to right polynomial:\n', fittedPolynomialRight)
        print('coeffs to right polynomial:\n', self.trajectoryCoeffs)

        self.leftSide = np.poly1d(fittedPolynomialLeft)
        self.rightSide = np.poly1d(fittedPolynomialRight)

    def fittingTrajectory(self):
        self.trajectoryLane =  np.linspace(min(self.xT),max(self.xT),300).reshape(-1,1)
        fittedPolynomialTraj = np.polyfit(self.xT, self.yT, self.polyRank)

        middleSide = np.poly1d(self.trajectoryCoeffs)
        trj = np.poly1d(fittedPolynomialTraj)
        self.trajectory = np.polyval(trj, self.trajectoryLane)
        self.polyTrajectory = np.polyval(middleSide, self.trajectoryLane)


    def find_minimum(self, poly):
        roots = np.real(np.roots(poly.deriv()))
        return roots[np.argmin(poly(roots))]

    def find_maximum(self, poly):
        roots = np.real(np.roots(poly.deriv()))
        return roots[np.argmax(poly(roots))]

    def findApex(self):
        if self.isRight:
            x = self.find_minimum(self.rightSide)
            self.apex = (x, self.rightSide(x))
        else:
            x = self.find_maximum(self.leftSide)
            self.apex = (x, self.leftSide(x))

        print('punkt szczytowy zakretu:\n', self.apex)


    def drawTrajectory(self, func, img):
        y, x = func()
        verts = np.array(list(zip(x, y)))
        cv2.polylines(img,np.int32([verts]),False,(randint(0, 255),randint(0, 255),randint(0, 255)),thickness=3)

    def printPlot(self):
        plt.scatter(*zip(*self.list_of_cords))
        self.findApex()
        plt.scatter(self.xLeft, self.yLeft)
        plt.scatter(self.xRight, self.yRight)
        plt.scatter(self.xT, self.yT)
        plt.scatter(self.apex[0], self.apex[1])

        # plt.plot(leftLine, np.polyval(fittedPolynomialLeft, leftLine), color="black")
        # plt.plot(rightLine, np.polyval(fittedPolynomialRight, rightLine), color="black")
        # plt.plot(leftLine, np.polyval(trajectory, rightLine), color="black")
        # plt.plot(leftLine, np.polyval(fittedPolynomialTraj, trajLine), color="black")
        plt.show()

    def predApex(self):
        self.definePoints()
        self.whichSide()
        self.fittingCurve()
        self.findApex()
        self.fittedCurvePoints()
        self.fittingTrajectory()
        print(self.apex)

    def returnApex(self):
        return self.apex
    
    def returnTrajectoryPoints(self):
        return self.xT, self.yT

    def returnTrajectory(self):
        return self.trajectoryLane, self.trajectory

    def returnPolyTrajectory(self):
        return self.trajectoryLane, self.polyTrajectory
