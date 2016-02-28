import GPU

GPU.platform_id = -1

import numpy as np
import random
import cv2
try:
    import Tkinter as tk
    import tkFileDialog as filedialog
except:
    import tkinter as tk
    from tkinter import filedialog
import namemaker3
import os

directory = os.path.realpath(__file__)

try:
    directory = directory[:directory.rindex('/')]
except:
    directory = directory[:directory.rindex('\\')]

single = ['cos', 'sin'] #Operations on a single number
binary = ['*', '+', '-'] #Operations for 2 numbers
numlist = ['x', 'y', 't', 'Constant']


def randFunction(functionLength, singleweight, numberweight):
    hasx = False
    hasy = False
    hast = False
    while not(hasx and hasy and hast):
        #Types: b for binary, s for single, f for first, n for number
        function = ''
        lasttype = 'f'
        thistype = 0
        hasx = False
        hasy = False
        hast = False
        chanceend = 0
        length = 1 #Number of operations done so far
        while True:
            chanceend = (1.0 - (1.0 / length)) ** (float(functionLength)/7)
            if lasttype == 'n':
                number = random.random()
                if number < chanceend:
                    break
                function = '(' + function + ')' + random.choice(binary)
                lasttype = 'b'
            elif lasttype == 's' or lasttype == 'b' or lasttype == 'f':
                function += '('
                thistype = random.random()
                if thistype < singleweight / (singleweight + numberweight):
                    function += random.choice(single)
                    lasttype = 's'
                else:
                    what = random.choice(numlist)
                    if what == 'Constant':
                        function += str(random.gauss(150, 50))
                    else:
                        function += what
                        if what == 'x':
                            hasx = True
                        elif what == 'y':
                            hasy = True
                        elif what == 't':
                            hast = True
                    lasttype = 'n'
                    function += ')'
            length += 1
    if function.count('(') > function.count(')'):
        function += ')' * (function.count('(') - function.count(')'))
    return function

def replace(s, substr, newsubstr):
    #Replaces the first instance of substr in s with newsubstr
    return s[:s.index(substr)] + newsubstr + s[s.index(substr)+len(substr):]

gpu = GPU.GPU()

clProgramTemplate = open('AutoVideosGPU.cl').read()

def createVideo(width, height, videoLength, frameRate, functionLength,
                singleWeight, numberWeight):

    rfunction = randFunction(functionLength, singleWeight, numberWeight)
    gfunction = randFunction(functionLength, singleWeight, numberWeight)
    bfunction = randFunction(functionLength, singleWeight, numberWeight)
    
    clProgramTemplate2 = replace(clProgramTemplate, '<WIDTH>', str(width))
    clProgramTemplate2 = replace(clProgramTemplate2, '<RFUNCTION>', rfunction)
    clProgramTemplate2 = replace(clProgramTemplate2, '<GFUNCTION>', gfunction)
    clProgramTemplate2 = replace(clProgramTemplate2, '<BFUNCTION>', bfunction)
    
    try:
        fourcc = cv2.cv.CV_FOURCC(*'XVID')
    except:
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
    name = ' '.join([namemaker3.generate() for i in range(3)]) + '.avi'
    out = cv2.VideoWriter(directory+'/'+name,fourcc, frameRate, (width,height))

    
    for t in range(int(videoLength*frameRate)):
        clProgram = replace(clProgramTemplate2, '<FRAMENUMBER>', str(t))
        gpu.readFromString(clProgram)

        globalSize = (width*height*3,)

        output = np.zeros(globalSize, dtype=np.float32)
        
        gpu.setup([], output)

        output = gpu.run('AutoFrame', globalSize) % 255

        output.resize(height, width, 3, refcheck=False)

        output = output.astype(np.uint8)

        out.write(output[:, :, ::-1])
        
    out.release()

def createVideos():
    
    global goToMenuButton, finishedLabel
    try:
        width = int(widthVar.get())
        height = int(heightVar.get())
        length = float(lengthVar.get())
        frameRate = float(frameRateVar.get())
        functionLength = float(functionLengthVar.get())
        singleWeight = float(singleWeightVar.get())
        numberWeight = float(numberWeightVar.get())
        numVideos = int(numVideosVar.get())
    except:
        errorLabel.config(text='Error: All settings must be numbers')
        return

    f = open('AutoVideosSettings.txt', 'w')
    f.write(' '.join([str(width), str(height), str(length), str(frameRate),
                      str(functionLength), str(singleWeight), str(numberWeight),
                      str(numVideos), directory]))
    f.close()
    try:
        menu.destroy()
    except:
        pass
    loadingLabel = tk.Label(root, text='Creating videos...')
    loadingLabel.grid(row=2, column=0)

    
    for i in range(numVideos):
        f = open('videoNumber.txt', 'w')
        f.write(str(i))
        f.close()
        loadingLabel.config(text='Creating videos... ' + str(i)\
                            + '/' + str(numVideos), font=('Helvetica', 16))

        root.update()

        createVideo(width, height, length, frameRate,
                    functionLength, singleWeight, numberWeight)


    loadingLabel.destroy()
    
    finishedLabel = tk.Label(root, text='AutoVideos has finished creating your\
 videos.')
    finishedLabel.grid(row=2, column=0)

    goToMenuButton = tk.Button(root, text='Go back to menu', command=goToMenu)
    goToMenuButton.grid(row=3, column=0)

   

def chooseDir():
    global directory
    directory = filedialog.askdirectory(title=\
                                        'Choose a directory for your videos')
    directoryLabel.config(text=directory)
    

def goToMenu():
    global menu, errorLabel, directoryLabel

    try:
        goToMenuButton.destroy()
        finishedLabel.destroy()
    except:
        pass
    
    menu = tk.Frame(root)
    menu.grid(row=1, column=0)


    tk.Label(menu, text='Width: ').grid(row=0, column=0, sticky=tk.E)
    tk.Entry(menu, textvariable=widthVar).grid(row=0, column=1)

    tk.Label(menu, text='Height: ').grid(row=1, column=0, sticky=tk.E)
    tk.Entry(menu, textvariable=heightVar).grid(row=1, column=1)

    tk.Label(menu, text='Length: ').grid(row=2, column=0, sticky=tk.E)
    tk.Entry(menu, textvariable=lengthVar).grid(row=2, column=1)

    tk.Label(menu, text='Frame rate: ').grid(row=3, column=0, sticky=tk.E)
    tk.Entry(menu, textvariable=frameRateVar).grid(row=3, column=1)

    tk.Label(menu, text='Function length: ').grid(row=4, column=0, sticky=tk.E)
    tk.Entry(menu, textvariable=functionLengthVar).grid(row=4, column=1)

    tk.Label(menu, text='Single operation weight: ').grid(row=5,
                                                          column=0, sticky=tk.E)
    tk.Entry(menu, textvariable=singleWeightVar).grid(row=5, column=1)

    tk.Label(menu, text='Number weight: ').grid(row=6, column=0, sticky=tk.E)
    tk.Entry(menu, textvariable=numberWeightVar).grid(row=6, column=1)

    tk.Label(menu, text='Number of videos: ').grid(row=7, column=0, sticky=tk.E)
    tk.Entry(menu, textvariable=numVideosVar).grid(row=7, column=1)


    tk.Button(menu, text='Choose Directory',
              command=chooseDir).grid(row=8, column=0, sticky=tk.E)
    directoryLabel = tk.Label(menu, text=directory)
    directoryLabel.grid(row=8, column=1, sticky=tk.W)
    
    tk.Button(menu, text='Create', command=createVideos).grid(row=9, column=0)

    errorLabel = tk.Label(menu, text='', fg='red')
    errorLabel.grid(row=10, column=0)

root = tk.Tk()
root.title('AutoVideos')
root.geometry('800x500+0+0')



if __name__ == '__main__':
    widthVar = tk.StringVar(root, '1280')
    heightVar = tk.StringVar(root, '720')
    lengthVar = tk.StringVar(root, '3')
    frameRateVar = tk.StringVar(root, '24')
    functionLengthVar = tk.StringVar(root, '80')
    singleWeightVar = tk.StringVar(root, '1')
    numberWeightVar = tk.StringVar(root, '1')
    numVideosVar = tk.StringVar(root, '1')

    tk.Label(root, text='AutoVideos',
             font=('Helvetica', 24)).grid(row=0, column=0) #Title label

    goToMenu()

    root.mainloop()

else:
    w, h, l, fr, fl, s, number, nVideos, directory = \
       open('AutoVideosSettings.txt').read().strip('\n').split(' ')

    

    numVideos = int(nVideos) - int(open('videoNumber.txt').read().strip('\n'))

    widthVar = tk.StringVar(root, w)
    heightVar = tk.StringVar(root, h)
    lengthVar = tk.StringVar(root, l)
    frameRateVar = tk.StringVar(root, fr)
    functionLengthVar = tk.StringVar(root, fl)
    singleWeightVar = tk.StringVar(root, s)
    numberWeightVar = tk.StringVar(root, number)
    numVideosVar = tk.StringVar(root, str(numVideos))

    tk.Label(root, text='AutoVideos',
             font=('Helvetica', 24)).grid(row=0, column=0) #Title label

    root.after(1000, createVideos)
    root.mainloop()
