import cv2

def show_image(image, message):
    cv2.imshow(message, image)
    cv2.waitKey(0)
 
# Read the original image
img = cv2.imread("C:/users/Sk4re/engineerka/images/curve.png") 
# Display original image
#show_image(img, 'Original')

# Convert to graycsale
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# Blur the image for better edge detection
img_blur = cv2.GaussianBlur(img_gray, (3,3), 0) 

# Canny Edge Detection
edges = cv2.Canny(image=img_blur, threshold1=150, threshold2=50) # Canny Edge Detection t1 = 100 t2 = 200 the beginning

show_image(edges, 'Canny Edge Detection')

cv2.destroyAllWindows()
