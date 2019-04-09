from get_data import *

def teamScore(year, team, coefficients):
    co = coefficients
    eFGp = 0
    TOV = 0
    FGA = 0
    FTA = 0
    ORB = 0
    FT = 0
    count = 0
    x = get(year, team)

    for i in x:
        if x[count]['eFG%'] != None:
            eFGp = eFGp + x[count]['eFG%']
        if x[count]['TOV'] != None:
            TOV = TOV + x[count]['TOV']
        if x[count]['FGA'] != None:
            FGA = FGA + x[count]['FGA']
        if x[count]['FTA'] != None:
            FTA = FTA + x[count]['FTA']
        if x[count]['ORB'] != None:
            ORB = ORB + x[count]['ORB']
        if x[count]['FT'] != None:
            FT = FT + x[count]['FT']
        # Gets the sum of all players for all these stats
        count = count + 1

    #Four factors
    eFGp = eFGp / count
    TOVp = TOV / (FGA + 0.44 * FTA + TOV)
    ORB = ORB / 82 / 100
    FT = FT / FGA

    score =  co[0] * eFGp + co[1] * ORB +  co[2] * FT -  co[3] * TOVp
    return score
