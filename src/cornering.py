import numpy as np
import cv2
from matplotlib import pyplot as plt


def show_img_with_matplotlib(color_img, title, pos):
    """Shows an image using matplotlib capabilities"""

    # Convert BGR image to RGB
    img_RGB = color_img[:, :, ::-1]

    ax = plt.subplot(2, 1, pos)
    plt.imshow(img_RGB)
    plt.title(title)
    plt.axis('off')

def matplot(img, title):
    img_RGB = img[:, :, ::-1]

    plt.imshow(img_RGB)
    plt.title(title)
    plt.show()

fig = plt.figure(figsize=(2, 2))
plt.suptitle("road angle", fontsize = 14, fontweight='bold')
fig.patch.set_facecolor('silver')

image = np.zeros((400, 400, 3), dtype="uint8")

image[:] = (220, 220, 220)


# int width = 500;
# float miny = -1, maxy = 1;
# Mat image = Mat::zeros(width,width,CV_8UC3);
# vector<Point2f> list_point(width);
# for(int i = 0; i < width; i++){
#    list_point[i].x = i;
#    float real_y = miny + ((maxy-miny)*i)/width;
#    list_point[i].y = real_y*real_y;
# }
# //Draw the curve
# for(int i = 1; i < width; i++) line(image,list_point[i-1],list_point[i],Scalar(255,255,255));
# imshow("image",image);
# waitKey();

width = 400

def draw_parabola_road(miny, maxy):

    point_list = [[],[]]
    for count in range(400):
        point_list[0].append(count)
        real_y = miny + (maxy-miny)*count/width
        point_list[1].append(real_y*real_y)

    miny, maxy = miny*2, maxy*2
    point_list2 = [[],[]]

    for count in range(400):
        point_list2[0].append(count)
        real_y = miny + (maxy-miny)*count/width
        point_list2[1].append(real_y*real_y)


    for count in range(1, 400):
        cv2.line(image, (point_list2[0][count-1], int(point_list2[1][count-1])+maxy*5), (point_list2[0][count], int(point_list2[1][count]+maxy*5)), (255, 0, 255), 3)
        cv2.line(image, (point_list[0][count-1], int(point_list[1][count-1])), (point_list[0][count], int(point_list[1][count])), (255, 0, 255), 3)


draw_parabola_road(-20, 20)

matplot(image, 'tytul')