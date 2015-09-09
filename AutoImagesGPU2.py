import os

def removeIfExists(filename):
    if os.path.exists(filename):
        os.remove(filename)


exitStatus = os.system('python AutoImagesGPU.py')

SEGFAULT = 35584

while exitStatus == SEGFAULT:
    exitStatus = os.system('python ImportAutoImages.py')
    
removeIfExists('AutoImagesSettings.txt')
removeIfExists('imageNumber.txt')
