from determine_record import *
from genetic_algorithm import runGA
import json
import time
start_time = time.time()

west = teams('west')
east = teams('east')

def teamIndex(conf, team):
    # gets the index of the team in the list. Function for determining record takes position as parameter
    for i in range(len(conf)):
        try:
            c = i
            index = conf[i].index(team)
            return (c, index)
            break
        except ValueError:
            pass

def allSs(record, co, num1, num2, year):
    x = []
    sol = []
    sol2 = []
    one = 0
    two = 0
    three = 0
    four = 0

    sol = runGA(record,co,num1, num2, year)
    x.append(sol)

    for i in range(1,3):
        year = year - 1
        sol = runGA(record,co,num1, num2, year)
        x.append(sol)

    for i in range(0,len(x)):
        one += x[i][0]
        two += x[i][1]
        three += x[i][2]
        four += x[i][3]

    sol2.append( round(one / len(x), 2) )
    sol2.append( round(two / len(x), 2) )
    sol2.append( round(three / len(x), 2) )
    sol2.append( round(four / len(x), 2) )
    print(sol2)

    return sol2

def getJson():
    with open('records.json','r') as file:
        x = json.load(file)

    return x
# Teams' record stored in JSON file

allRecords = getJson()

print('')
co = input('The team\'s conference ')
t = input('Input the team initials ')
year = int(input('Input the last two numbers of the year you want to find the record for. e.g. input 18 for 2018 '))

year = year - 1

if co == 'west':
    c = west
    nums = teamIndex(c, t)
elif co == 'east':
    c = east
    nums = teamIndex(c,t)

if co == 'west':
    n = 0
elif co == 'east':
    n = 1

record = allRecords["20" + str(year)][n][t]

#sol = allSs(record, co, nums[0], nums[1], year)
sol = runGA(record, co, nums[0], nums[1], year)

print('')
print(sol)
print('These are the solution coefficients. Using this to predict next season\'s record.')

if co == 'west':
    w = 0
    for i in range(5):
        w = w + simulateWest(west[nums[0]][nums[1]], nums[0], nums[1], year +1, sol )
    w = w // 5
    # because of the randomness, we can take an average
elif co == 'east':
    w = 0
    for i in range(5):
        w = w + simulateEast(east[nums[0]][nums[1]], nums[0], nums[1], year +1, sol )
    w = w // 5

print(t, 'is predicted to win', w, 'games in 20' + str(year + 1), 'Their record:', w , '-' , 82 - w)

print ("My program took", time.time() - start_time, "to run")
