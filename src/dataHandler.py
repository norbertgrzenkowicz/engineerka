import os
from pathlib import Path

class dataHandler:
    def __init__(self):
        self.testImagePath = Path("")

def rename(dataPath, prefix='empty'):
    """Zmienia nazwe oraz numeracje plikow w zbiorze danych np. prefix=road, count = 30 => road_30.png"""
    for count, image_name in enumerate(os.listdir(dataPath)):
        name = prefix + '_' + str(int(count)) + '.png'
        src = f"{dataPath}/{image_name}" 
        dst = f"{dataPath}/{name}"
        os.rename(src, dst)

def renameDict(dataPath):
    """Szuka i zamienia odpowiedni ciag znakow zapisany w slowniku types"""
    for count, image_name in enumerate(os.listdir(dataPath)):
        types = {'.png_pose': '_pose'}
        for key, values in types.items():
            if key in image_name:
                src = f"{dataPath}/{image_name}"  
                dst = f"{dataPath}/{image_name.replace(key, values)}"
                os.rename(src, dst)

def add_pose(dataPath):
    """Dla kazdego pliku w zbiorze danych tworzy plik tesktowy z suffixem _pose"""
    for count, image_name in enumerate(os.listdir(dataPath)):
        name = image_name + '_pose.txt'
        src = f"{dataPath}/{image_name}"  
        dst = f"{dataPath}/{name}"

        with open(dst, 'w') as fp:
            pass

