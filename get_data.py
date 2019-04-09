import sqlalchemy

engine = sqlalchemy.create_engine('mysql+pymysql://root:qazwsxedcrfv@localhost:3306/stats')
# Engine for connection
connection = engine.connect()

def roster(year, team):
    query = 'SELECT Player FROM 2k'+ str(year) + ' WHERE Tm = '+ '\'' + team + '\''
    resultProxy = connection.execute(query)
    ''' This executes the query statement, 'query', from dB in connection and
    stores it in resultProxy '''
    # resultProxy is the object returned by .execute() method
    resultSet = resultProxy.fetchall()
    # Actual data requested when using fetch method on resultProxy

    x = []
    for row in resultSet:
        x.append (row[0])
        ''' fetchall() return all rows and all fields. Need to iterate over the rows to access the fields and get the data '''
    return x

def stats(year, team):
    players = roster(year, team)
    # players is a list with players from predict year
    playerStats = []
    for i in players:
        query = 'SELECT * FROM 2k'+ str(year - 1) + ' WHERE Player = ' + '\''+ i + '\' and Tm = \'TOT\' '
        ''' Players who played for multiple teams will have multiple records in the table
        This is to Query for just the reccord of their totals as oppose to a specific team '''
        resultProxy = connection.execute(query)
        resultSet = resultProxy.fetchall()

        if not resultSet:
            query = 'SELECT * FROM 2k'+ str(year - 1) + ' WHERE Player = ' + '\''+ i + '\' '
            resultProxy = connection.execute(query)
            resultSet = resultProxy.fetchall()

        if resultSet:
            for row in resultSet:
                playerStats.append( {'eFG%': row [16], 'FGA': row[8], 'FTA': row[18], 'TOV' : row[26], 'FT': row[17], 'ORB': row[20]})

    return playerStats

def get(year, team):
    x = stats(year, team)

    return x
