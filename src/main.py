import sys  
import cv2 as cv

print(cv.__version__)
print(sys.version)

cap = cv.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    # capture frame-by-frame
    ret, frame = cap.read()        
    #if frame is read correctly ret is True
    if not ret:
        print("Cant receive frame (stream end?). Exiting..")
        break
    #our operations on the frame come here
    gray = cv. cvtColor(frame, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (3,3), 0)
    edges = cv.Canny(image=blur, threshold1=50, threshold2=100) # Canny Edge Detection

    #display the resulting frame
    cv.imshow('Canny Edge Detection', edges)
    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()