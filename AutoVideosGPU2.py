import os

def removeIfExists(filename):
    if os.path.exists(filename):
        os.remove(filename)


exitStatus = os.system('python AutoVideosGPU.py')

SEGFAULT = 35584

while exitStatus == SEGFAULT:
    exitStatus = os.system('python ImportAutoVideos.py')
    
removeIfExists('AutoVideosSettings.txt')
removeIfExists('videoNumber.txt')
