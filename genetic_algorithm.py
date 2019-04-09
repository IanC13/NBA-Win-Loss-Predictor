import random
from determine_record import *

west = teams('west')
east = teams('east')

def individual(N,min,max):
    x = []
    for i in range(N):
        x.append( random.randint(min,max) / 100 )
    return x

    '''randomly generates a number between min, max and appends them into a list. does it N times '''
    # Creates an individual in a population

def population(count,N,min,max):
    x = []
    for i in range(count):
        x.append(individual(N,min,max))
    return x

    # Creates the population using the individual function

def fitnessFunction(conference, numbers, target,  cNum, tNum, year):
    # numbers is the list of coefficients
    print(numbers)
    if conference == 'east':
        observed = simulateEast(east[cNum][tNum], cNum, tNum, year, numbers)
    elif conference == 'west':
        observed = simulateWest(west[cNum][tNum], cNum , tNum, year, numbers)

    score = abs(target - observed)
    print(score, 'fitness score')
    return score

    # Takes in a LIST and a target
    # Generates a score based on the difference between the sum of the list and the target


def evolution(prevPop, target, conf, cNum, tNum, year):
    newPop = []
    targetLength = len(prevPop)
    noHP = (1/3)
    noLP = (1/3)

    while len(newPop) != int(targetLength * noHP):
        min = 100
        for i in range(len(prevPop)):
            x = fitnessFunction(conf, prevPop[i], target, cNum, tNum, year)
            if x <= 0:
                return prevPop[i]
                ''' If we find the solution within the predefined population we return it straight away
                 there is no need for evolution '''
            else:
                if x <= min:
                    k = i
                    min = x

        newPop.append(prevPop[k])
        prevPop.pop(k)
    ''' loop through everything
    if the individual is in our desired range of the target, we return it straight away
    otherwise , take the SMALLEST fitnessfunction score individuals (which would be 1D list)
    (smaller fitnessFunction scores are BETTER performers)
    (one of the arrays in the 2D array)
    put in new pop
    pop it off prevPop '''

    # Randomly select lesser performers
    for i in range(int(targetLength * noLP)):
        ran = random.randint(0, len(prevPop)-1)
        newPop.append(prevPop[ran])
        prevPop.pop(ran)

    # newPop are parents of next generation
    # 2/3 is selected to be parents
    # 1/3 is breeded

    # Breeding
    parentsLength = len(newPop)

    children = []
    child1 = []
    child2 =[]
    childrenTargetLength = targetLength - parentsLength

    while len(children) != childrenTargetLength:
        fatherNo = random.randint(0, parentsLength - 1)
        motherNo = random.randint(0, parentsLength - 1)
        ''' Randomly chooses mother and father from the group of parents
         With some high performers and some lower performers '''

        if fatherNo != motherNo:
            # Ensures father and mother are not the same
            father = newPop[fatherNo]
            mother = newPop[motherNo]

            firstPoint = random.randint(0, len(father)-1)
            secondPoint = random.randint(0, len(father) - 1)
            # Multipoint crossover: Chooses two points in an individual as crossover points

            if firstPoint != secondPoint and secondPoint > firstPoint:
                # First point != second point (otherwise no crossover)
                # Second point > first point (prevents weird stuff from happening because of how child1 and child2 are defined)
                child1 = father[:firstPoint] + mother[firstPoint: secondPoint] + father[secondPoint:]
                child2 = mother[:firstPoint] + father[firstPoint: secondPoint] + mother[secondPoint:]

                children.append(child1)
                children.append(child2)

    # Mutations
    chanceToMutate = random.randint(1,20)
    # 5% chance
    if chanceToMutate == 1:
        individualToMutate = random.randint(0,len(children)-1)
        geneToMutate = random.randint(0, len(children[individualToMutate])-1)
        # Randomly chooses which individual and which gene in that individual to mutate

        children[individualToMutate][geneToMutate] =  random.randint(75, 125) / 100
        # randint is any number for generating individual

        print(individualToMutate, geneToMutate, 'mutated')

    newPop.extend(children)

    print(newPop)
    return newPop


def runGA(target, conference, cNum, tNum, year ):
    size = 12
    # not 4
    test = population(size ,4,75,125)
    repeat = True
    count = 0

    while repeat == True:
        count = count + 1
        test = evolution(test, target, conference, cNum, tNum, year)
        solution = test
        print(count, 'evolution(s)')
        if len(solution) != size:
            return solution
            repeat = False
            break
            ''' If the returning value is a solution, the len of the 1 d list will be Four
             this is not 'size' so we know that what was returned was the solution

             if returning value is the new population for next evolution, the length
             will be 6 and the same as size so we know this is the pop for next evolution
             so these functions are not executed '''
