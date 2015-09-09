import random
def getTrigrams(filename):
    #Gets trigrams from the file
    f = open(filename)
    d = {}
    for line in f:
        key = line[:3]
        value = line.strip('\n')[4:]
        d[key] = int(value)
    return d

trigrams = getTrigrams('trigrams.txt')



def nextchar(previous=False):
    if previous != False:
        possibleTrigrams = {}
        for trigram in trigrams:
            if trigram[0:2] == previous:
                possibleTrigrams[trigram] = trigrams[trigram]

        possibleSum = 0
        for trigram in possibleTrigrams:
            possibleSum += possibleTrigrams[trigram]

        trigramChosen = random.randrange(possibleSum)
        x = 0 #The variable for the sum of all the previous trigrams
        for trigram in possibleTrigrams:
            x += possibleTrigrams[trigram]
            if trigramChosen <= x:
                return trigram[2]
    
    else:
        firstTrigrams = {}
        for trigram in trigrams:
            if trigram[0] == ' ':
                firstTrigrams[trigram] = trigrams[trigram]
                
        firstSum = 0
        for trigram in firstTrigrams:
            firstSum += firstTrigrams[trigram]
            
        trigramChosen = random.randrange(firstSum)
        x = 0 #The variable for the sum of all the previous trigrams
        for trigram in firstTrigrams:
            x += firstTrigrams[trigram]
            if trigramChosen <= x:
                if ' ' in trigram[1:]: #If there's a space in the trigram, try again
                    return nextchar()
                else:
                    return trigram[1:]

def generate():
    char = nextchar()
    name = ''
    while char != ' ':
        name += char
        char = nextchar(name[-2:])
    return name.capitalize()

if __name__ == '__main__':
    print('Welcome to NameMaker!')
    print('Please enter the number of names you want to print out!')

    while True:
        number = int(input('Number: '))
        for i in range(number):
            print(generate())
