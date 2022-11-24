import cv2
import numpy as np
from random import randint
import logging

class Corners():
    def __init__(self, OGmediaPath = '', mediaPath = ''):
        self.mediaPath = mediaPath
        self.img = cv2.imread(mediaPath)
        self.OGimg = cv2.imread(OGmediaPath)
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

        self.leftLine = None
        self.RightLine = None

        self.leftTrajectory = None
        self.rightTrajectory = None

    def definePoints(self):
        """Zamien wysegmentowane zdjecie na liste koordynatow kazdego piksela 
        nie bedacego czarnym pikselem po obrobce zdjecia przez algorytm canny edge detection"""
        edges = cv2.Canny(self.img, 100, 255)
        indices = np.where(edges != [0])
        coordinates = zip(indices[0], indices[1])
        self.list_of_cords = list(coordinates)
    
        # self.list_of_cords = self.list_of_cords[::5] # Wyrzucenie co piątego elementu listu w celu zmniejszenia ilości punktów do przetworzenia

        # for i, cord in enumerate(self.list_of_cords):
        #     if cord[0] > 750:
        #         self.list_of_cords.pop(i) 
      
    def whichSide(self):
        """Metoda przyporzadkujacy dany koordynat do listy przedstawiajaca lewa badz prawa strone drogi"""
        _ , prev = self.list_of_cords[-1]

        for i in self.list_of_cords[::-1]:
            if abs(prev - i[1]) > 10 and prev > i[1]:
                self.isRight = False
            elif abs(prev - i[1]) > 10 and prev < i[1]:
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
        """Redukcja odleglosci listy w przypadku roznicy dlugosci dwoch stron"""
        for i in range(len(self.xRight)):
            if self.xRight[i] in self.xLeft:
                last = i
                break
        self.xRight = self.xRight[last:]
        self.yRight = self.yRight[last:]


    def fittedCurvePoints(self):
        """Kalkulacja koordynatow trajektorii ruchu"""
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

        cornerIndex = 0

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
        """Ucinanie dluzszej listy zawierajacej punkty osi X lub Y jednej z stron"""
        toCut = abs(len(listX) - len(listY))
        if len(listX) > len(listY):
            listX = listX[:-toCut]
        elif len(listX) > len(listY):
            listY = listY[:-toCut]
        return listX, listY

    def removeDuplicates(self, list):
        """Usuwa kolejne wystapienia jednej wartosci osi X dla jednej z stron"""
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
        """Kalkulacja parametrow wielomianow drogi"""
        self.leftLine = np.linspace(min(self.xLeft),max(self.xLeft),300).reshape(-1,1)
        self.rightLine = np.linspace(min(self.xRight),max(self.xRight),300).reshape(-1,1)

        fittedPolynomialLeft = np.polyfit(self.xLeft, self.yLeft, self.polyRank)
        fittedPolynomialRight = np.polyfit(self.xRight, self.yRight, self.polyRank)

        for i in range(self.polyRank + 1):
            self.trajectoryCoeffs.append((fittedPolynomialLeft[i] + fittedPolynomialRight[i]) / 2)

        logging.info('coeffs to left polynomial:\n', fittedPolynomialLeft)
        logging.info('coeffs to right polynomial:\n', fittedPolynomialRight)
        logging.info('coeffs to right polynomial:\n', self.trajectoryCoeffs)

        self.leftSide = np.poly1d(fittedPolynomialLeft)
        self.rightSide = np.poly1d(fittedPolynomialRight)

    def fittingTrajectory(self):
        """Kalkulacja trajektorii ruchu"""
        self.trajectoryLane =  np.linspace(min(self.xT),max(self.xT),300).reshape(-1,1)
        fittedPolynomialTraj = np.polyfit(self.xT, self.yT, self.polyRank)

        middleSide = np.poly1d(self.trajectoryCoeffs)
        trj = np.poly1d(fittedPolynomialTraj)

        self.trajectory = np.polyval(trj, self.trajectoryLane)
        self.polyTrajectory = np.polyval(middleSide, self.trajectoryLane)

        self.leftTrajectory =np.polyval(self.leftSide, self.trajectoryLane)
        self.rightTrajectory =np.polyval(self.rightSide, self.trajectoryLane)


    def find_minimum(self, poly):
        """Zanjdz lokalne minimum w wielomianie"""
        roots = np.real(np.roots(poly.deriv()))
        return roots[np.argmin(poly(roots))]

    def find_maximum(self, poly):
        """Zanjdz lokalne maksimum w wielomianie"""
        roots = np.real(np.roots(poly.deriv()))
        return roots[np.argmax(poly(roots))]

    def findApex(self):
        """Znajdz szczyt zakretu (Apex)"""
        if self.isRight:
            x = self.find_minimum(self.rightSide)
            self.apex = (x, self.rightSide(x))
        else:
            x = self.find_maximum(self.leftSide)
            self.apex = (x, self.leftSide(x))

        logging.info('punkt szczytowy zakretu:\n', self.apex)


    def drawTrajectory(self, func, img):
        """Metoda rysuje za pomoca cv2.polylines wielomian danej trajektorii"""
        y, x = func()
        verts = np.array(list(zip(x, y)))
        cv2.polylines(img,np.int32([verts]),False,(randint(0, 255),randint(0, 255),randint(0, 255)),thickness=3)

    def predApex(self):
        """Proces predykcji szczytu zakretu"""
        self.definePoints()
        self.whichSide()
        self.fittingCurve()
        self.findApex()
        self.fittedCurvePoints()
        self.fittingTrajectory()
        logging.debug('apex: ', self.apex)

    def returnApex(self):
        """Zwroc koordynaty szczytu zakretu"""
        return self.apex
    
    def returnTrajectoryPoints(self):
        """Zwroc punkty trajektorii"""
        return self.xT, self.yT

    def returnTrajectory(self):
        """Zwroc Trajektorie"""
        return self.trajectoryLane, self.trajectory

    def returnPolyTrajectory(self):
        """Zwroc wielomian bedacego polowa drogi"""
        return self.trajectoryLane, self.polyTrajectory
    
    def returnleftSide(self):
        """Zwroc przebieg lewej strony drogi"""
        return self.trajectoryLane, self.leftTrajectory

    def returnRightSide(self):
        """Zwroc przebieg prawej strony drogi"""
        return self.trajectoryLane, self.rightTrajectory