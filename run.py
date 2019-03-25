from determine_record import *
from genetic_algorithm import runGA
import time
start_time = time.time()

west = westTeams()
east = eastTeams()

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
        # exception handling

west2018 = {'HOU': 65, 'GSW': 58, 'POR': 49, 'OKC': 48, 'UTA': 48, 'NOP': 48, 'SAS': 47, 'MIN' : 47, 'DEN': 46, 'LAC': 42, 'LAL': 35, 'SAC': 27, 'DAL': 24, 'MEM': 22, 'PHO': 21 }
east2018 = {'TOR': 59, 'BOS': 55, 'PHI': 52, 'CLE': 50, 'IND': 48, 'MIA': 44, 'MIL': 44, 'WAS' : 43, 'DET': 39, 'CHO': 36, 'NYK': 29, 'BRK': 28, 'CHI': 27, 'ORL': 25, 'ATL': 24 }

west2017 = {'HOU': 55, 'GSW': 67, 'POR': 41, 'OKC': 47, 'UTA': 51, 'NOP': 38, 'SAS': 61, 'MIN' : 31, 'DEN': 40, 'LAC': 51, 'LAL': 26, 'SAC': 32, 'DAL': 33, 'MEM': 43, 'PHO': 24 }
east2017 = {'TOR': 51, 'BOS': 53, 'PHI': 28, 'CLE': 51, 'IND': 42, 'MIA': 41, 'MIL': 42, 'WAS' : 49, 'DET': 37, 'CHO': 36, 'NYK': 31, 'BRK': 20, 'CHI': 41, 'ORL': 29, 'ATL': 43 }

west2016 = {'HOU': 41, 'GSW': 73, 'POR': 44, 'OKC': 55, 'UTA': 40, 'NOP': 30, 'SAS': 67, 'MIN' : 29, 'DEN': 33, 'LAC': 53, 'LAL': 17, 'SAC': 33, 'DAL': 42, 'MEM': 42, 'PHO': 23 }
east2016 = {'TOR': 56, 'BOS': 48, 'PHI': 10, 'CLE': 57, 'IND': 45, 'MIA': 48, 'MIL': 33, 'WAS' : 41, 'DET': 44, 'CHO': 48, 'NYK': 32, 'BRK': 21, 'CHI': 42, 'ORL': 35, 'ATL': 48 }

west2015 = {'HOU': 56, 'GSW': 67, 'POR': 51, 'OKC': 45, 'UTA': 38, 'NOP': 45, 'SAS': 55, 'MIN' : 16, 'DEN': 30, 'LAC': 56, 'LAL': 21, 'SAC': 29, 'DAL': 50, 'MEM': 55, 'PHO': 39 }
east2015 = {'TOR': 49, 'BOS': 40, 'PHI': 18, 'CLE': 53, 'IND': 38, 'MIA': 37, 'MIL': 41, 'WAS' : 46, 'DET': 32, 'CHO': 33, 'NYK': 17, 'BRK': 38, 'CHI': 50, 'ORL': 25, 'ATL': 60 }

west2014 = {'HOU': 54, 'GSW': 51, 'POR': 54, 'OKC': 59, 'UTA': 25, 'NOP': 34, 'SAS': 62, 'MIN' : 40, 'DEN': 36, 'LAC': 57, 'LAL': 27, 'SAC': 28, 'DAL': 49, 'MEM': 50, 'PHO': 48 }
east2014 = {'TOR': 48, 'BOS': 25, 'PHI': 19, 'CLE': 33, 'IND': 56, 'MIA': 54, 'MIL': 15, 'WAS' : 44, 'DET': 29, 'CHO': 43, 'NYK': 37, 'BRK': 44, 'CHI': 48, 'ORL': 23, 'ATL': 38 }

# Teams as key, wins as value. By year and conference

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

if co == 'west' and year == 18:
    record = west2018[t]

elif co == 'west' and year == 17:
    record = west2017[t]

elif co == 'west' and year == 16:
    record = west2016[t]

elif co == 'west' and year == 15:
    record = west2015[t]

elif co == 'west' and year == 14:
    record = west2014[t]

elif co == 'east' and year == 18:
    record = east2018[t]

elif co == 'east' and year == 17:
    record = east2017[t]

elif co == 'east' and year == 16:
    record = east2016[t]

elif co == 'east' and year == 15:
    record = east2015[t]

elif co == 'east' and year == 14:
    record = east2014[t]


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
