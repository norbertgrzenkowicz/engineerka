import os
from pathlib import Path

class dataHandler:
    def __init__(self):
        self.dataThresholdPath = 'data/thresholded'
        self.testSegmentedImagePath = Path("/home/norbert/Documents/datasets/segmentedRoads/curvy/R0.png")
        self.testImagePath = Path("augment_the_curve.jpg")
    # dataPath = '/home/norbert/Documents/repos/engineerka/jupyter/~/bike_dataset/images'

def augment_namefiles(dataPath):
    for count, image_name in enumerate(os.listdir(dataPath)):
        name = 'bike' + str(int(count)) + '.png'
        src = f"{dataPath}/{image_name}" 
        dst = f"{dataPath}/{name}"
        os.rename(src, dst)