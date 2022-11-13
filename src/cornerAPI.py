import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


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

    def definePoints(self):
        edges = cv2.Canny(self.img, 100, 255)
        indices = np.where(edges != [0])
        coordinates = zip(indices[0], indices[1])
        self.list_of_cords = list(coordinates)
    
        self.list_of_cords = self.list_of_cords[::5] # Wyrzucenie co piątego elementu listu w celu zmniejszenia ilości punktów do przetworzenia

        for i, cord in enumerate(self.list_of_cords):
            if cord[0] > 750:
                self.list_of_cords.pop(i)  
      
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


    def fittingCurve(self):


        leftLine = np.linspace(min(self.xLeft),max(self.xLeft),300).reshape(-1,1)
        rightLine = np.linspace(min(self.xRight),max(self.xRight),300).reshape(-1,1)

        fittedPolynomialLeft = np.polyfit(self.xLeft, self.yLeft, self.polyRank)
        fittedPolynomialRight = np.polyfit(self.xRight, self.yRight, self.polyRank)

        trajectoryCoeffs = []

        print(len(self.leftPointsList), len(self.rightPointsList))

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

    def printPlot(self):
        # plt.scatter(*zip(*self.list_of_cords))
        plt.scatter(self.xLeft, self.yLeft)
        plt.scatter(self.xRight, self.yRight)
        plt.scatter(self.apex[0], self.apex[1])

        plt.plot(self.leftLine, np.polyval(self.fittedPolynomialLeft, self.leftLine), color="black")
        plt.plot(self.rightLine, np.polyval(self.fittedPolynomialRight, self.rightLine), color="black")
        plt.plot(self.leftLine, np.polyval(self.trajectory, self.leftLine), color="black")

        plt.show()


    def predApex(self):
        self.definePoints()
        self.whichSide()
        self.fittingCurve()
        self.findApex()
        print(self.apex)

    def returnApex(self):
        return self.apex

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
