import sqlalchemy

engine = sqlalchemy.create_engine('mysql+pymysql://root:qazwsxedcrfv@localhost:3306/stats')
#Connection engine to the database
connection = engine.connect()
#Connection

def roster(year, team):
    #This function gets the roster from season 'year'
    query = 'SELECT Player FROM 2k'+ str(year) + ' WHERE Tm = '+ '\'' + team + '\''
    resultProxy = connection.execute(query)
    ''' This executes the query statement, 'query', from dB in connection and
    stores it in resultProxy '''
    #resultProxy is the object returned by .execute() method
    resultSet = resultProxy.fetchall()
    #Actual data requested when using fetch method on resultProxy

    x = []
    for row in resultSet:
        x.append (row[0])
        #fetchall() return all rows and all fields
        #Need to iterate over the rows to access the fields and get the data
    return x
    #Roster for the year is in a 1D list and returned


def stats(year, team):
    #This function gets the previous season stats of players on roster
    players = roster(year, team)
    #players is a list with players from predict year

    playerStats = []

    for i in players:
        query = 'SELECT * FROM 2k'+ str(year - 1) + ' WHERE Player = ' + '\''+ i + '\' and Tm = \'TOT\' '
        ''' Players who played for multiple teams will have multiple records in the table
        This is to Query for just the reccord of their totals as oppose to a specific team '''
        resultProxy = connection.execute(query)
        resultSet = resultProxy.fetchall()

        if not resultSet:
            #If list is empty
            query = 'SELECT * FROM 2k'+ str(year - 1) + ' WHERE Player = ' + '\''+ i + '\' '
            resultProxy = connection.execute(query)
            resultSet = resultProxy.fetchall()

        if resultSet:
            for row in resultSet:
                playerStats.append( {'eFG%': row [16], 'FGA': row[8], 'FTA': row[18], 'TOV' : row[26], 'FT': row[17], 'ORB': row[20]})

    return playerStats
    #This is a list with dictionaries as elements

def get(year, team):
    x = stats(year, team)

    return x
