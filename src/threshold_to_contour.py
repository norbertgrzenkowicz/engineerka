"""
Thresholding color images
"""

# Import required packages:
import cv2
from Device import Device

class thresholdToContour(Device):
    def __init__(self):
        """hehe"""

    def thresholding(self):
        # Load the image and convert it to grayscale:
        image = cv2.imread('data/supermoto_evening99.jpg')

        # Plot the image:
        self.show_img_with_matplotlib(image, "image", 1)

        # Apply cv2.threshold():
        ret1, thresh1 = cv2.threshold(image, 80, 255, cv2.THRESH_BINARY)

        # Apply cv2.threshold():
        (b, g, r) = cv2.split(image)
        ret2, thresh2 = cv2.threshold(b, 80, 255, cv2.THRESH_BINARY)
        ret3, thresh3 = cv2.threshold(g, 80, 255, cv2.THRESH_BINARY)
        ret4, thresh4 = cv2.threshold(r, 80, 255, cv2.THRESH_BINARY)
        bgr_thresh = cv2.merge((thresh2, thresh3, thresh4))

        # Plot the created images
        self.show_img_with_matplotlib(thresh1, "threshold (120) BGR image", 2)
        self.show_img_with_matplotlib(bgr_thresh, "threshold (120) each channel and merge", 3)

# Thresh = Threshold()

# # Create the dimensions of the figure and set title and color:
# fig = plt.figure(figsize=(12, 4))
# plt.suptitle("Thresholding BGR images", fontsize=14, fontweight='bold')
# fig.patch.set_facecolor('silver')

# Thresh.thresholding()
# # Show the Figure:
# plt.show()