import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from random import randint

class Corners():
    def __init__(self, mediaPath):
        self.mediaPath = mediaPath
        self.img = cv2.imread(mediaPath, 0)

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

        self.polyTrajectory = None

        self.trj = None
        self.trjLn = None

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
            self.reducingLengths(self.xLeft, self.yLeft, self.xRight, self.yRight)
        elif self.xRight[0] < self.xLeft[0]:
            self.reducingLengths(self.xRight, self.yRight, self.xLeft, self.yLeft)
 

    def reducingLengths(self, smallX, smallY, bigX, bigY):
        for i in range(len(self.xRight)):
            if self.xRight[i] in self.xLeft:
                ostatni = i
                break
        self.xRight = self.xRight[ostatni:]
        self.yRight = self.yRight[ostatni:]


    def fittedCurvePoints(self):

        cordX = list(zip(self.xRight, self.yRight))
        cordY = list(zip(self.xLeft, self.yLeft))

        cordX, _, Y = self.removeDuplicates(cordX)
        cordY, _, Y = self.removeDuplicates(cordY)

        cordX = cordX[:-3]
        _ = _[:-3]

        begin = abs(cordX[0][1] - cordY[0][1])
        end = abs(cordX[-20][1] - cordY[-20][1])

        wideness = []

        print('wide', begin, end)

        beginplace = 0.7
        endplace2 = 0.7
        beginplace2 = 0.7
        endplace = 0.1

        for i in range(len(cordX)):
            wideness.append(cordX[i][1] - cordY[i][1])
        
        wideness = np.array(wideness)

        sideness = np.linspace(beginplace,endplace2,len(cordX) - 30)
        sidenessCorner = np.linspace(beginplace2,endplace, 30)
        sideness = np.append(sideness, sidenessCorner)

        traj = list(zip(_, sideness * wideness + Y))
        # traj = traj[:150]

        for point in traj:
            self.xT.append(point[0])
            self.yT.append(point[1])

        print(traj)

        print('lol', len(cordX), len(cordY))



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

        trajectoryCoeffs = []

        leftLine = np.linspace(min(self.xLeft),max(self.xLeft),300).reshape(-1,1)
        rightLine = np.linspace(min(self.xRight),max(self.xRight),300).reshape(-1,1)
        self.trjLn =  np.linspace(min(self.xT),max(self.xT),300).reshape(-1,1)

        fittedPolynomialLeft = np.polyfit(self.xLeft, self.yLeft, self.polyRank)
        fittedPolynomialRight = np.polyfit(self.xRight, self.yRight, self.polyRank)
        fittedPolynomialTraj = np.polyfit(self.xT, self.yT, self.polyRank)

        for i in range(self.polyRank + 1):
            # if fittedPolynomialLeft[i] > 0 and fittedPolynomialRight[0] < 0 or fittedPolynomialLeft[i] < 0 and fittedPolynomialRight[0] > 0:
            #     trajectoryCoeffs.append(-(abs(fittedPolynomialLeft[i]) + abs(fittedPolynomialRight[i])) / 2)
            # elif 
            trajectoryCoeffs.append((fittedPolynomialLeft[i] + fittedPolynomialRight[i]) / 2)

# trajectoryCoeffs[0] = fittedPolynomialLeft[0]
# trajectoryCoeffs[-1] = trajectoryCoeffs[-1] - 100

        print('coeffs to left polynomial:\n', fittedPolynomialLeft)
        print('coeffs to right polynomial:\n', fittedPolynomialRight)
        print('coeffs to right polynomial:\n', trajectoryCoeffs)

        self.leftSide = np.poly1d(fittedPolynomialLeft)
        self.rightSide = np.poly1d(fittedPolynomialRight)
        trajectory = np.poly1d(trajectoryCoeffs)
        trj = np.poly1d(fittedPolynomialTraj)
 
        # self.findApex()
        # plt.scatter(self.xLeft, self.yLeft)
        # plt.scatter(self.xRight, self.yRight)
        # plt.scatter(self.xT, self.yT)
        # # plt.scatter(self.apex[0], self.apex[1])

        self.trj = np.polyval(trj, self.trjLn)
        self.polyTrajectory = np.polyval(trajectory, self.trjLn)

        # plt.plot(leftLine, np.polyval(fittedPolynomialLeft, leftLine), color="black")
        # plt.plot(rightLine, np.polyval(fittedPolynomialRight, rightLine), color="black")
        # plt.plot(leftLine, np.polyval(trajectory, rightLine), color="black")
        # plt.plot(leftLine, np.polyval(fittedPolynomialTraj, trajLine), color="black")

        # plt.show()

# print(leftSide)
# print(rightSide)
# print(xRight[yRight.index(min(yRight))], min(yRight))


    def find_minimum(self, poly):
        roots = np.real(np.roots(poly.deriv()))
        return roots[np.argmin(poly(roots))]

    def find_maximum(self, poly):
        roots = np.real(np.roots(poly.deriv()))
        return roots[np.argmax(poly(roots))]


# print(find_minimum2(leftSide))
# apex = find_maximum2(leftSide)
# apex1 = find_maximum2(rightSide)

# To verify if another function to recognize corner is needed
# if mymodel[0] > 0 and mymodel2[0] > 0:
#     print("zakret prawy")
# elif mymodel[0] <= 0 or mymodel2[0] <= 0:
#     print("zakret lewy")

    def findApex(self):
        if self.isRight:
            x = self.find_minimum(self.rightSide)
            self.apex = (x, self.rightSide(x))
        else:
            x = self.find_maximum(self.leftSide)
            self.apex = (x, self.leftSide(x))

        print('punkt apexu:\n', self.apex)


    def drawTrajectory(self, func, img):

        y, x = func()

        verts = np.array(list(zip(x, y)))
        cv2.polylines(img,np.int32([verts]),False,(randint(0, 255),randint(0, 255),randint(0, 255)),thickness=3)

    def printPlot(self):
        # plt.scatter(*zip(*self.list_of_cords))
        pass


    def predApex(self):
        self.definePoints()
        self.whichSide()
        self.fittedCurvePoints()
        self.fittingCurve()
        self.findApex()
        print(self.apex)


    def returnApex(self):
        return self.apex
    
    def returnTrajectoryPoints(self):
        return self.xT, self.yT

    def returnTrajectory(self):
        return self.trjLn, self.trj

    def returnPolyTrajectory(self):
        return self.trjLn, self.polyTrajectory



# pointCord = list_of_cords[0]

# list_of_cords.pop(0)

# print("PETELKA")
# print(len(list_of_cords))

# cords_in = []

# cords_in.append(pointCord[0])

# for i, cord in enumerate(list_of_cords):
#     if cord[0] == cords_in[-1]:
#         list_of_cords.pop(i)
#     if cord[0] != cords_in[-1]:
#         cords_in.append(cord[0])

# for i, cord in enumerate(list_of_cords):
#     if cord[0] == pointCord[0] and abs(cord[1] - pointCord[1]) > 0:
#         list_of_cords.pop(i)
#     if cord[0] != pointCord[0]:
#         pointCord = list_of_cords[i]
