import GPU
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
import wave
import struct
import time

directory = os.path.realpath(__file__)

try:
    directory = directory[:directory.rindex('/')]
except:
    directory = directory[:directory.rindex('\\')]

single = ['cos', 'sin'] #Operations on a single number
binary = ['*', '+', '-'] #Operations for 2 numbers
numlist = ['x', 'Constant']

def randFunction(length, singleweight, numberweight):
    hasx = False
    while not hasx:
        #Types: b for binary, s for single, f for first, n for number
        function = ''
        lasttype = 'f'
        thistype = 0
        hasx = False
        chanceend = 0
        length = 1 #Number of operations done so far
        while True:
            chanceend = (1.0 - (1.0 / length)) ** 12.0
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

clProgramTemplate = open('AutoAudioGPU.cl').read()

def createAudio(length, sampleRate, functionLength, singleWeight, numberWeight):
    function = randFunction(functionLength, singleWeight, numberWeight)

    clProgram = replace(clProgramTemplate, '<FUNCTION>', function)

    gpu.readFromString(clProgram)

    globalSize = (length*sampleRate,)

    output = np.zeros(globalSize, dtype=np.float32)


    gpu.setup([], output)

    output = gpu.run('AutoAudio', globalSize) % (32767 * 2) - 32767

    name = directory + '/' + \
             ' '.join([namemaker3.generate() for i in range(3)]) + '.wav'

    outputFile = wave.open(name, 'w')
    outputFile.setparams((1, 1, sampleRate, 0, 'NONE', 'not compressed'))

    outputFile.writeframes(output)

    outputFile.close()

def createAudios():
    global goToMenuButton, finishedLabel
    try:
        length = int(lengthVar.get())
        sampleRate = int(sampleRateVar.get())
        functionLength = float(functionLengthVar.get())
        singleWeight = float(singleWeightVar.get())
        numberWeight = float(numberWeightVar.get())
        numAudios = int(numAudiosVar.get())
    except:
        errorLabel.config(text='Error: All settings must be numbers')
        return

    menu.destroy()
    
    loadingLabel = tk.Label(root, text='Creating audio files...')
    loadingLabel.grid(row=2, column=0)

    
    for i in range(numAudios):
        
        loadingLabel.config(text='Creating audio files... ' + str(i)\
                            + '/' + str(numAudios), font=('Helvetica', 16))

        root.update()

        createAudio(length, sampleRate, functionLength, singleWeight,
                    numberWeight)


    loadingLabel.destroy()
    
    finishedLabel = tk.Label(root, text='AutoAudio has finished creating your\
 audio files.')
    finishedLabel.grid(row=2, column=0)

    goToMenuButton = tk.Button(root, text='Go back to menu', command=goToMenu)
    goToMenuButton.grid(row=3, column=0)
    
def chooseDir():
    global directory
    directory = filedialog.askdirectory(title='Choose a directory for your\
 audio files')
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


    tk.Label(menu, text='Length: ').grid(row=0, column=0, sticky=tk.E)
    tk.Entry(menu, textvariable=lengthVar).grid(row=0, column=1)

    tk.Label(menu, text='Sample rate: ').grid(row=1, column=0, sticky=tk.E)
    tk.Entry(menu, textvariable=sampleRateVar).grid(row=1, column=1)

    tk.Label(menu, text='Function length: ').grid(row=2, column=0, sticky=tk.E)
    tk.Entry(menu, textvariable=functionLengthVar).grid(row=2, column=1)

    tk.Label(menu, text='Single operation weight: ').grid(row=3,
                                                          column=0, sticky=tk.E)
    tk.Entry(menu, textvariable=singleWeightVar).grid(row=3, column=1)

    tk.Label(menu, text='Number weight: ').grid(row=4, column=0, sticky=tk.E)
    tk.Entry(menu, textvariable=numberWeightVar).grid(row=4, column=1)

    tk.Label(menu, text='Number of audio files: ').grid(row=5, column=0,
                                                        sticky=tk.E)
    tk.Entry(menu, textvariable=numAudiosVar).grid(row=5, column=1)


    tk.Button(menu, text='Choose Directory',
              command=chooseDir).grid(row=6, column=0, sticky=tk.E)
    directoryLabel = tk.Label(menu, text=directory)
    directoryLabel.grid(row=6, column=1, sticky=tk.W)
    
    tk.Button(menu, text='Create', command=createAudios).grid(row=7, column=0)

    errorLabel = tk.Label(menu, text='', fg='red')
    errorLabel.grid(row=8, column=0)

root = tk.Tk()
root.title('AutoAudio')
root.geometry('800x500+0+0')
lengthVar = tk.StringVar(root, '5')
sampleRateVar = tk.StringVar(root, '44100')
functionLengthVar = tk.StringVar(root, '80')
singleWeightVar = tk.StringVar(root, '1')
numberWeightVar = tk.StringVar(root, '1')
numAudiosVar = tk.StringVar(root, '5')

tk.Label(root, text='AutoAudio',
         font=('Helvetica', 24)).grid(row=0, column=0) #Title label

goToMenu()

root.mainloop()
