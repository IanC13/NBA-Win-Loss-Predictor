import random
def individual(N,min,max):
    x = []
    for i in range(N):
        x.append(random.randint(min,max))
    return x

    #randomly generates a number between min, max and appends them into
    #a list. does it N times
    #Creates an individual in a population
    #E.g. [2,4,6,2,7]


def population(count,N,min,max):
    x = []
    for i in range(count):
        x.append(individual(N,min,max))
    return x

    #Uses the individual function and creates a 2D array with count
    #number of elements and each element as an individual
    #E.g. [[3,4,6,5,3],[2,8,2,5,1],[8,9,3,6,1]]

def fitnessFunction(numbers,target):
    x = sum(numbers)
    score = abs(target - x)
    return score

    #Takes in a LIST and a target
    #Generates a score based on the difference between the sum of the
    #list and the target
    #THE SMALLER THE BETTER


def evolution(prevPop, target):
    #prevPop is a 2D array
    #Taking a portion of the previous gen population
    #determine the number of individuals taken from previous population
    newPop = []
    targetLength = len(prevPop)
    noHP = 0.1
    noLP = 0.1

    while len(newPop) != int(targetLength * noHP):
        min = fitnessFunction(prevPop[0], target)
        for i in range(len(prevPop)):
            if fitnessFunction(prevPop[i], target) <= min:
                k = i
                min = fitnessFunction(prevPop[i], target)

        newPop.append(prevPop[k])
        prevPop.pop(k)
    #loop through everything
    #take the SMALLEST fitnessfunction score individuals (which would be 1D list)
    #(smaller fitnessFunction scores are BETTER performers)
    #(one of the arrays in the 2D array)
    #put in new pop
    #pop it off prevPop


    #Randomly select lesser performers
    for i in range(int(targetLength * noLP)):
        ran = random.randint(0, len(prevPop)-1)
        newPop.append(prevPop[ran])
        prevPop.pop(ran)

    #newPop are parents of next generation
    #40% is selected to be parents
    #60% is breeded

    #Breeding
    #Multipoint crossover
    parentsLength = len(newPop)
    children = []
    child1 = []
    child2 =[]
    childrenTargetLength = targetLength - parentsLength

    while len(children) != childrenTargetLength:
        fatherNo = random.randint(0, parentsLength - 1)
        motherNo = random.randint(0, parentsLength - 1)
        #Randomly chooses mother and father from the group of parents
        #With some high performers and some lower performers

        if fatherNo != motherNo:
            #Ensures father and mother are not the same
            father = newPop[fatherNo]
            mother = newPop[motherNo]

            firstPoint = random.randint(0, len(father)-1)
            secondPoint = random.randint(0, len(father) - 1)
            #Multipoint crossover: Chooses two points in an individual as crossover points

            if firstPoint != secondPoint and secondPoint > firstPoint:
                #First point != second point (otherwise no crossover)
                #Second point > first point (prevents weird stuff from happening because of how child1 and child2 are defined)
                child1 = father[:firstPoint] + mother[firstPoint: secondPoint] + father[secondPoint:]
                child2 = mother[:firstPoint] + father[firstPoint: secondPoint] + mother[secondPoint:]

                children.append(child1)
                children.append(child2)

    #Mutations

    chanceToMutate = random.randint(1,100)
    #1% chance
    if chanceToMutate == 1:
        individualToMutate = random.randint(0,len(children)-1)
        geneToMutate = random.randint(0, len(children[individualToMutate])-1)
        #Randomly chooses which individual and which gene in that individual to mutate

        children[individualToMutate][geneToMutate] =  random.randint(0,100)
        #randint is any number for generating individual

        print(individualToMutate, geneToMutate, 'mutated')


    newPop.extend(children)

    return newPop


#Usage code
target = 250
repeat = True
testPop = population(100,5,0,100)

count = -1

while repeat == True:
    for i in testPop:
        if fitnessFunction(i,target) == 0:
            count = count + 1
            print('Solution found after', count,'evolution(s)')
            print(i)
            repeat = False
            break

        else:
            count = count + 1
            print(count,'evolution(s)')
            print(testPop)
            testPop = evolution(testPop,target)
        break
