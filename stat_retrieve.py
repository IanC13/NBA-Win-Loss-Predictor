import pandas as pd
#'as pd' so can use pd.command instead of pandas.command
import sqlalchemy

def sqlconnection():
    #This function creates the connection engine between python and the database in mysql
    engine = sqlalchemy.create_engine('mysql+pymysql://root:qazwsxedcrfv@localhost:3306/stats')
    #dialect+driver://username:password@host:port/database
    return engine

def savetosql(df, num):
    #This function puts the called dataframe into the database using the connection
    engine = sqlconnection()
    df.to_sql(name = '2k1' + num , con = engine, index = False,  if_exists = 'replace')
    # name = table name, con = connection if_exists (if the table already exists, replace everything in it)


def editSQL(num):
    #Some players' name have apostrophe in them. This cause problems later onself.
    #This function removes all the apostrophes in every name in every table
    engine = sqlconnection()
    connection = engine.connect()
    query = "UPDATE 2k1" + str(num) + " SET Player = REPLACE (Player,  '\\''  , '')"
    resultProxy = connection.execute(query)

    if num == 3 or num == 4:
        query = "UPDATE 2k1" + str(num) + " SET Tm = REPLACE (Tm, 'CHA', 'CHO')"
        resultProxy = connection.execute(query)
        #There was a team name change
        #This just changes it to match the new name


for i in range(3,10):
    yearNum = str(i)
    stats, = pd.read_html ('https://www.basketball-reference.com/leagues/NBA_201'+yearNum+'_totals.html', header = None)
    #The ',' is used to unpack the tuple of values
    #   Right Hand Side returns a tuple of values that can be unpacked into the left hand side using ','
    #Read_html is a built in function in the Pandas library to scrape tabular data from html pages

    stats.drop('Rk', axis = 1, inplace = True)
    #This line removes the column 'Rk'
    #axis = 1 is a way to tell pandas that it is a column
    #by default drop() funtionz only displays the changed dataframe and not save it. intplace = True replaces the dataframe

    stats = stats[~stats['Player'].isin(['Player'])]
    # This get rids of all the weird rows which are headings in the middle of the table

    stats.rename(columns={'FG%':'FGp', '3P%':'3Pp', '2P%':'2Pp', 'eFG%':'eFGp', 'FT%':'FTp'} , inplace = True )
    #Headings violate mysql rules with special characters. Changes headings to fit those rules.

    stats = stats.apply(pd.to_numeric, errors = 'ignore')
    #Changes all datatypes from string to double instead of numbers in text
    #errors = ignore, keeps all the columns with just text as string

    savetosql(stats, yearNum)

    editSQL(i)

print('DONE')
