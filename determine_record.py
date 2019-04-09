from combine_data import *
import random


def teams(conference):
    if conference == 'west':
        file = open('western.txt','r')
    elif conference == 'east':
        file = open('eastern.txt','r')

    count = 1
    x=[]
    y=[]
    z=[]
    team = []
    for line in file:
        line = line.rstrip()
        if count == 1 or count == 2 or count == 3 or count == 4 or count == 5:
            x.append(line)
            count += 1
            # These teams are in one division

        elif count == 6 or count == 7 or count == 8 or count == 9 or count == 10:
            y.append(line)
            count += 1
            # These teams are in another division
        else:
            z.append(line)
            count += 1
            # These teams are in the final division for this conference

    team.append(x)
    team.append(y)
    team.append(z)
    file.close()
    return team
    #Returns a 2d list, each list in this list are the 5 teams that are in the same division

def simulateMainAtHome(main,t1, t2, year):
    '''This function simulates the chance that team 1 wins against team 2 or vice versa in ONE
    Head to head game. It accounts for some randomness and home court advantage.
    This one game is simulated many times and the team that wins majority of the time will
    be considered to be the winner of this game '''
    home = t1
    away = t2
    x = [1,1,1,1]
    homeInit = main

    awayInit = teamScore(year, away, x)
    #Get home and away team score first

    homeWin = 0
    awayWin = 0

    for i in range(0,1000):

        randomHome = random.randint(0,25) / 100
        # Home team has advantage
        randomAway = random.randint(0,15) / 100

        homeScore = homeInit + randomHome
        awayScore = awayInit + randomAway


        if homeScore >= awayScore:
            homeWin = homeWin + 1
        else:
            awayWin = awayWin + 1

    if homeWin > awayWin:
        print(home, 'won', homeWin / 10 ,'% of the time')
        return 'won'
    else:
        print(away, 'won' , awayWin / 10 ,'% of the time')
        return 'lost'

''' One function for home and one for away because our coefficients will only modify the main team we are testing
 The main team will be sometimes home and sometimes away so we need the coefficients parameter to be passed
 to the homeInit or the awayInit when calling teamScore() '''

def simulateMainAtAway(t1, t2, main, year):
    home = t1
    away = t2
    x = [1,1,1,1]
    homeInit = teamScore(year, home, x)

    awayInit = main
    #Get home and away team score first

    homeWin = 0
    awayWin = 0


    for i in range(0,1000):

        randomHome = random.randint(0,25) / 100
        # Home team has advantage
        randomAway = random.randint(0,15) / 100

        homeScore = homeInit + randomHome
        awayScore = awayInit + randomAway


        if homeScore >= awayScore:
            homeWin = homeWin + 1
        else:
            awayWin = awayWin + 1

    if homeWin > awayWin:
        print(home, 'won', homeWin / 10 ,'% of the time')
        return 'won'
    else:
        print(away, 'won' , awayWin / 10 ,'% of the time')
        return 'lost'

def simulateWest(team, division, index, year, coefficients):
    ''' division and index is the position of the team in the list of teams.
    Passed into the function to use as conditions so the team doesn't play themselves'''
    mainScore = teamScore(year, team, coefficients)

    west = teams('west')
    east = teams('east')
    wins = 0

    if division == 0:
        d1 = 1
        d2 = 2
    elif division == 1:
        d1 = 0
        d2 = 2
    elif division == 2:
        d1 = 0
        d2 = 1
    # used to know the other two divisions when randoming the teams later

    for i in range(2):
        for j in range(0,5):
            if j != index:
                x = simulateMainAtHome(mainScore, team, west[division][j],year)
                if x == 'won':
                    wins += 1
    # Plays every team in the same divion twice at HOME

    for i in range(2):
        for j in range(0,5):
            if j != index:
                x = simulateMainAtAway(west[division][j],team, mainScore, year)
                if x == 'lost':
                    wins += 1
    # Plays every team in the same divion twice at AWAY


    for i in range(0,3):
        for j in range(0,5):
            x = simulateMainAtHome(mainScore, team, east[i][j],year)
            if x == 'won':
                wins += 1
    # Plays every team in the oppsing conference once at HOME

    for i in range(0,3):
        for j in range(0,5):
            x = simulateMainAtAway(east[i][j],team, mainScore, year)
            if x == 'lost':
                wins += 1
    # Plays every team in the oppsing conference once at AWAY

    # Random 6 teams in same conference but differet division to play 2 home 2 away
    rd1 = [0,1,2,3,4]
    rd2 = [0,1,2,3,4]

    for i in range(6):
        if len(rd1) != 0 and len(rd2) != 0:
            n = random.choice([d1,d2])
            # If they are both not empty, randomly choose one of the conferences
            if n == d1:
                y = random.choice(rd1)
                # Randomly choose a team in this conference
                for i in range(2):
                    x = simulateMainAtHome(mainScore, team, west[d1][y],year)
                    if x == 'won':
                        wins += 1
                        # Play 2 games at HOME

                for i in range(2):
                    x = simulateMainAtAway(west[d1][y],team, mainScore, year)
                    if x == 'lost':
                        wins +=1
                        # Play 2 games AWAY
                rd1.remove(y)

            elif n == d2:
                y = random.choice(rd2)
                for i in range(2):
                    x = simulateMainAtHome(mainScore, team, west[d2][y],year)
                    if x == 'won':
                        wins += 1

                for i in range(2):
                    x = simulateMainAtAway(west[d2][y], team, mainScore, year)
                    if x == 'lost':
                        wins +=1
                rd2.remove(y)


        elif len(rd1) == 0:
            # If one of the list is empty (because it was picked) i.e. teams have all been played
            y = random.choice(rd2)
            # Choose from the other list
            for i in range(2):
                x = simulateMainAtHome(mainScore, team, west[d2][y],year)
                if x == 'won':
                    wins += 1  # 2 at HOME

            for i in range(2):
                x = simulateMainAtAway(west[d2][y], team, mainScore, year)
                if x == 'lost':
                    wins +=1 # 2 AWAY
            rd2.remove(y)

        elif len(rd2) == 0:
            y = random.choice(rd1)
            for i in range(2):
                x = simulateMainAtHome(mainScore, team, west[d1][y],year)
                if x == 'won':
                    wins += 1


            for i in range(2):
                x = simulateMainAtAway(west[d1][y], team, mainScore, year)
                if x == 'lost':
                    wins +=1
            rd1.remove(y)


    # next have to random 2 teams to play 2 home games and 1 away game
    for i in range(2):
        if len(rd1) == 0:
            # if conference 1 is empty, random 2 teams from conference 2
            g = d2
            f = random.randint(0, len(rd2)-1)
        elif len(rd2) == 0:
            g = d1
            f = random.randint(0,len(rd1)-1)
        else:
            g = random.choice([d1,d2])
            # both not empty, random conference then random team
            if g == d1:
                f= random.randint(0, len(rd1) - 1)
            elif g == d2:
                f = random.randint(0, len(rd2) - 1)

        for i in range(2):
            x = simulateMainAtHome(mainScore, team, west[g][f], year)
            if x == 'won':
                wins += 1  # 2 at HOME

        x = simulateMainAtAway(west[g][f], team, mainScore,year)
        if x == 'lost':
            wins += 1  # 1 AWAY

        if g == d1:
            rd1.remove(rd1[f])
        else:
            rd2.remove(rd2[f])


    # Last 2 teams, 1 away 1 home
    while len(rd1) != 0:
        # Take all teams from this conference. At this point, there is either 2 left, or 1 or none
        for i in range(len(rd1)):
            x = simulateMainAtHome(mainScore, team, west[d1][i],year)
            if x == 'won':
                wins += 1  # 1 at HOME

            for i in range(2):
                x = simulateMainAtAway(west[d1][i], team, mainScore,year)
                if x == 'lost':
                    wins +=1  # 1 AWAY
        rd1 = []  # Remove all from list

    while len(rd2) != 0:
        # Same as above
        for i in range(len(rd2)):
            x = simulateMainAtHome(mainScore, team, west[d2][i], year)
            if x == 'won':
                wins += 1

            for i in range(2):
                x = simulateMainAtAway(west[d2][i], team, mainScore, year)
                if x == 'lost':
                    wins +=1
        rd2 = []

    print(wins, 'wins')
    return(wins)


def simulateEast(team, division, index, year, coefficients):
    ''' This and simulateWest are essentially the same function but one is for a team in the western conference
     and the other in the eastern conference. Two functions are needed because of the difference
     in the teams and the number of games they play per team due to them being different conferences '''

    mainScore = teamScore(year, team, coefficients)

    west = teams('west')
    east = teams('east')
    wins = 0

    if division == 0:
        d1 = 1
        d2 = 2
    elif division == 1:
        d1 = 0
        d2 = 2
    elif division == 2:
        d1 = 0
        d2 = 1

    for i in range(2):
        for j in range(0,5):
            if j != index:
                x = simulateMainAtHome(mainScore, team, east[division][j],year)
                if x == 'won':
                    wins += 1

    for i in range(2):
        for j in range(0,5):
            if j != index:
                x = simulateMainAtAway(east[division][j],team, mainScore, year)
                if x == 'lost':
                    wins += 1


    for i in range(0,3):
        for j in range(0,5):
            x = simulateMainAtHome(mainScore, team, west[i][j],year)
            if x == 'won':
                wins += 1

    for i in range(0,3):
        for j in range(0,5):
            x = simulateMainAtAway(west[i][j],team, mainScore, year)
            if x == 'lost':
                wins += 1

    rd1 = [0,1,2,3,4]
    rd2 = [0,1,2,3,4]

    for i in range(6):
        if len(rd1) != 0 and len(rd2) != 0:

            n = random.choice([d1,d2])
            if n == d1:
                y = random.choice(rd1)
                for i in range(2):
                    x = simulateMainAtHome(mainScore, team, east[d1][y],year)
                    if x == 'won':
                        wins += 1

                for i in range(2):
                    x = simulateMainAtAway(east[d1][y],team, mainScore, year)
                    if x == 'lost':
                        wins +=1
                rd1.remove(y)

            elif n == d2:
                y = random.choice(rd2)
                for i in range(2):
                    x = simulateMainAtHome(mainScore, team, east[d2][y],year)
                    if x == 'won':
                        wins += 1

                for i in range(2):
                    x = simulateMainAtAway(east[d2][y], team, mainScore, year)
                    if x == 'lost':
                        wins +=1
                rd2.remove(y)

        elif len(rd1) == 0:
            y = random.choice(rd2)
            for i in range(2):
                x = simulateMainAtHome(mainScore, team, east[d2][y],year)
                if x == 'won':
                    wins += 1

            for i in range(2):
                x = simulateMainAtAway(east[d2][y], team, mainScore, year)
                if x == 'lost':
                    wins +=1
            rd2.remove(y)

        elif len(rd2) == 0:
            y = random.choice(rd1)
            for i in range(2):
                x = simulateMainAtHome(mainScore, team, east[d1][y],year)
                if x == 'won':
                    wins += 1

            for i in range(2):
                x = simulateMainAtAway(east[d1][y], team, mainScore, year)
                if x == 'lost':
                    wins +=1
            rd1.remove(y)


    for i in range(2):
        if len(rd1) == 0:
            g = d2
            f = random.randint(0, len(rd2)-1)
        elif len(rd2) == 0:
            g = d1
            f = random.randint(0,len(rd1)-1)
        else:
            g = random.choice([d1,d2])
            if g == d1:
                f= random.randint(0, len(rd1) - 1)
            elif g == d2:
                f = random.randint(0, len(rd2) - 1)

        for i in range(2):
            x = simulateMainAtHome(mainScore, team, east[g][f], year)
            if x == 'won':
                wins += 1

        x = simulateMainAtAway(east[g][f], team, mainScore,year)
        if x == 'lost':
            wins += 1

        if g == d1:
            rd1.remove(rd1[f])
        else:
            rd2.remove(rd2[f])


    while len(rd1) != 0:
        for i in range(len(rd1)):
            x = simulateMainAtHome(mainScore, team, east[d1][i],year)
            if x == 'won':
                wins += 1

            for i in range(2):
                x = simulateMainAtAway(east[d1][i], team, mainScore,year)
                if x == 'lost':
                    wins +=1
        rd1 = []

    while len(rd2) != 0:
        for i in range(len(rd2)):
            x = simulateMainAtHome(mainScore, team, east[d2][i], year)
            if x == 'won':
                wins += 1

            for i in range(2):
                x = simulateMainAtAway(east[d2][i], team, mainScore, year)
                if x == 'lost':
                    wins +=1
        rd2 = []

    print(wins, 'wins')
    return(wins)
