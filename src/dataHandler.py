import os
from pathlib import Path

class dataHandler:
    def __init__(self):
        self.testImagePath = Path("augment_the_curve.jpg")

def rename(dataPath, prefix='empty'):
    for count, image_name in enumerate(os.listdir(dataPath)):
        name = prefix + '_' + str(int(count)) + '.png'
        src = f"{dataPath}/{image_name}" 
        dst = f"{dataPath}/{name}"
        os.rename(src, dst)

def rename2(dataPath):
# rename2("/home/norbert/Documents/repos/engineerka/data/road/labeled")
    for count, image_name in enumerate(os.listdir(dataPath)):
        # name = 'bike' + str(int(count)) + '.png'

        types = {'um_lane': 'um', 'um_road': 'um', 'umm_road': 'umm', 'uu_road': 'uu'}
        types = {'.png_pose': '_pose'}
        for key, values in types.items():
            if key in image_name:
                src = f"{dataPath}/{image_name}"  
                dst = f"{dataPath}/{image_name.replace(key, values)}"
                os.rename(src, dst)

def add_pose(dataPath):
# rename2("/home/norbert/Documents/repos/engineerka/data/road/labeled")
    for count, image_name in enumerate(os.listdir(dataPath)):
        # name = 'bike' + str(int(count)) + '.png'
        name = image_name + '_pose.txt'
        src = f"{dataPath}/{image_name}"  
        dst = f"{dataPath}/{name}"

        with open(dst, 'w') as fp:
            pass

rename2('/home/norbert/Documents/repos/engineerka/data/apex')