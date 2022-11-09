import numpy as np
import cv2
from matplotlib import pyplot as plt

class CornerAPI: # TODO: create "mainAPI" class to be parent of kCluster/thresholders?
    def __init__(self):

        self.fig = plt.figure(figsize=(2, 2))
        plt.suptitle("road angle", fontsize = 14, fontweight='bold')
        self.fig.patch.set_facecolor('silver')
        self.width = 800
        self.image = np.zeros((self.width, self.width, 3), dtype="uint8")
        self.image[:] = (220, 220, 220)

        # def show_img_with_matplotlib(color_img, title, pos):
        #     """Shows an image using matplotlib capabilities"""
        #TODO IMPLEMENT PARENT CLASS WITH show_img_with_matplotlib and colors dict

    def matplot(self, img, title):
        img_RGB = img[:, :, ::-1]

        plt.imshow(img_RGB)
        plt.title(title)
        plt.show()

    def draw_parabola_road(self, miny, maxy):

        point_list = [[],[]]
        for count in range(self.width):
            point_list[0].append(count)
            real_y = miny + (maxy-miny)*count/self.width 
            point_list[1].append(real_y**2)

        miny, maxy = miny*2, maxy*2
        point_list2 = [[],[]]

        for count in range(self.width):
            point_list2[0].append(count)
            real_y = miny + (maxy-miny)*count/self.width
            point_list2[1].append(real_y**2)

        for count in range(1, self.width):
            cv2.line(self.image, (point_list2[0][count-1], int(point_list2[1][count-1])+maxy*5), (point_list2[0][count], int(point_list2[1][count]+maxy*5)), (255, 0, 255), 3)
            cv2.line(self.image, (point_list[0][count-1], int(point_list[1][count-1])), (point_list[0][count], int(point_list[1][count])), (255, 0, 255), 3)
            cv2.line(self.image, (point_list[0][count-1], int(point_list[1][count-1])+maxy*4), (point_list[0][count], int(point_list[1][count]+maxy*4)), (255, 0, 255), 3)

        self.matplot(self.image, 'bottomtext')




road_angle = CornerAPI()

road_angle.draw_parabola_road(-20, 20)
