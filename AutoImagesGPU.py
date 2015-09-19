import GPU

#GPU.platform_id = -1 #Remove the # at the start of the line to choose platform

import numpy as np
import random
try:
    import Image
except:
    from PIL import Image
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
numlist = ['x', 'y', 'Constant']

def randFunction(functionLength, singleweight, numberweight):
    hasx = False
    hasy = False
    while not(hasx and hasy):
        #Types: b for binary, s for single, f for first, n for number
        function = ''
        lasttype = 'f'
        thistype = 0
        hasx = False
        hasy = False
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

clProgramTemplate = open('AutoImagesGPU.cl').read()

def createImage(width, height, functionLength, singleWeight, numberWeight):

    rfunction = randFunction(functionLength, singleWeight, numberWeight)
    gfunction = randFunction(functionLength, singleWeight, numberWeight)
    bfunction = randFunction(functionLength, singleWeight, numberWeight)
    
    clProgram = replace(clProgramTemplate, '<WIDTH>', str(width))
    clProgram = replace(clProgram, '<RFUNCTION>', rfunction)
    clProgram = replace(clProgram, '<GFUNCTION>', gfunction)
    clProgram = replace(clProgram, '<BFUNCTION>', bfunction)

    gpu.readFromString(clProgram)

    globalSize = (width*height*3,)

    output = np.zeros(globalSize, dtype=np.float32) % 255

    gpu.setup([], output)

    output = gpu.run('AutoImage', globalSize)

    output.resize(height, width, 3, refcheck=False)

    img = Image.fromarray(output.astype(np.uint8), 'RGB')
    img.save(directory + '/' +
             ' '.join([namemaker3.generate() for i in range(3)]) + '.png')


def createImages():
    
    global goToMenuButton, finishedLabel
    try:
        width = int(widthVar.get())
        height = int(heightVar.get())
        functionLength = float(functionLengthVar.get())
        singleWeight = float(singleWeightVar.get())
        numberWeight = float(numberWeightVar.get())
        numImages = int(numImagesVar.get())
    except:
        errorLabel.config(text='Error: All settings must be numbers')
        return

    f = open('AutoImagesSettings.txt', 'w')
    f.write(' '.join([str(width), str(height), str(functionLength),
                      str(singleWeight), str(numberWeight), str(numImages),
                      directory]))
    f.close()
    try:
        menu.destroy()
    except:
        pass
    loadingLabel = tk.Label(root, text='Creating images...')
    loadingLabel.grid(row=2, column=0)

    
    for i in range(numImages):
        f = open('imageNumber.txt', 'w')
        f.write(str(i))
        f.close()
        loadingLabel.config(text='Creating images... ' + str(i)\
                            + '/' + str(numImages), font=('Helvetica', 16))

        root.update()

        createImage(width, height, functionLength, singleWeight, numberWeight)


    loadingLabel.destroy()
    
    finishedLabel = tk.Label(root, text='AutoImages has finished creating your\
 images.')
    finishedLabel.grid(row=2, column=0)

    goToMenuButton = tk.Button(root, text='Go back to menu', command=goToMenu)
    goToMenuButton.grid(row=3, column=0)

   
    
def chooseDir():
    global directory
    directory = filedialog.askdirectory(title=\
                                        'Choose a directory for your images')
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

    tk.Label(menu, text='Function length: ').grid(row=2, column=0, sticky=tk.E)
    tk.Entry(menu, textvariable=functionLengthVar).grid(row=2, column=1)

    tk.Label(menu, text='Single operation weight: ').grid(row=3,
                                                          column=0, sticky=tk.E)
    tk.Entry(menu, textvariable=singleWeightVar).grid(row=3, column=1)

    tk.Label(menu, text='Number weight: ').grid(row=4, column=0, sticky=tk.E)
    tk.Entry(menu, textvariable=numberWeightVar).grid(row=4, column=1)

    tk.Label(menu, text='Number of images: ').grid(row=5, column=0, sticky=tk.E)
    tk.Entry(menu, textvariable=numImagesVar).grid(row=5, column=1)


    tk.Button(menu, text='Choose Directory',
              command=chooseDir).grid(row=6, column=0, sticky=tk.E)
    directoryLabel = tk.Label(menu, text=directory)
    directoryLabel.grid(row=6, column=1, sticky=tk.W)
    
    tk.Button(menu, text='Create', command=createImages).grid(row=7, column=0)

    errorLabel = tk.Label(menu, text='', fg='red')
    errorLabel.grid(row=8, column=0)

root = tk.Tk()
root.title('AutoImages')
root.geometry('800x500+0+0')



if __name__ == '__main__':
    widthVar = tk.StringVar(root, '1280')
    heightVar = tk.StringVar(root, '720')
    functionLengthVar = tk.StringVar(root, '80')
    singleWeightVar = tk.StringVar(root, '1')
    numberWeightVar = tk.StringVar(root, '1')
    numImagesVar = tk.StringVar(root, '1')

    tk.Label(root, text='AutoImages',
             font=('Helvetica', 24)).grid(row=0, column=0) #Title label

    goToMenu()

    root.mainloop()

else:
    w, h, l, s, number, nImages, directory = \
       open('AutoImagesSettings.txt').read().strip('\n').split(' ')

    

    numImages = int(nImages) - int(open('imageNumber.txt').read().strip('\n'))

    widthVar = tk.StringVar(root, w)
    heightVar = tk.StringVar(root, h)
    functionLengthVar = tk.StringVar(root, l)
    singleWeightVar = tk.StringVar(root, s)
    numberWeightVar = tk.StringVar(root, number)
    numImagesVar = tk.StringVar(root, str(numImages))

    tk.Label(root, text='AutoImages',
             font=('Helvetica', 24)).grid(row=0, column=0) #Title label

    root.after(1000, createImages)
    root.mainloop()
