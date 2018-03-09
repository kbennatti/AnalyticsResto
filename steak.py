import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
import random as rand
import datetime
import sqlite3

item = 'steak'

#train steak model
df=pd.DataFrame()

time = sorted([rand.randrange(10,21) for element in range(100)])
price = [rand.randrange(15.0,40.0) for element in range(100)]
end_time=20.0
df['Time']=time
df['Time_to_close']=[end_time for row in range(len(time))]-df['Time']
i=0
stock=[]
for i in range(100):
    stock.append(i)
    i+=1

stock=sorted(stock,reverse=True)

df.insert(0,'Current_Price',price,True)
df.insert(0,'Target_Stock',stock,True)

X=df[['Time_to_close','Current_Price']]

clf=linear_model.LinearRegression().fit(df[['Time_to_close','Current_Price']],df[['Target_Stock']])
betaPrice=clf.coef_[0,1]
#end model training

#set inital values - beginning of day

price0=36.0
amount0 = 100
priceAndQ = [[item,price0,amount0]]

conn = sqlite3.connect('resto.db')  # connection
c = conn.cursor()
c.execute('DROP TABLE IF EXISTS price')
c.execute('CREATE TABLE IF NOT EXISTS price(item TEXT, price FLOAT, quantity INTEGER)')
c.execute('INSERT INTO price VALUES(?,?,?)', priceAndQ)
conn.commit()
conn.close()

#WHERE NOT EXISTS (SELECT 1 FROM price WHERE item = \'steak\''
def tableFromDatabase(database, table):
    conn = sqlite3.connect(database)  # connection
    c = conn.cursor()  # get a cursor object, all SQL commands are processed by
    c.execute('SELECT * FROM %s' % table)
    tableRows = c.fetchall()
    conn.close()
    return tableRows

rows = tableFromDatabase('resto.db', 'price')

currentInfo = [list(row) for row in rows]
currentPrice=currentInfo[0][1]

amountSold = 10 # increment through get_posts
amount=amount0-amountSold
currentHour=datetime.datetime.now().hour
currentMinutes=datetime.datetime.now().minute
currentTime=currentHour+currentMinutes/60.0

currentData=[[currentTime,currentPrice]]
prediction=[[float(clf.predict(currentData))]]

changeInPrice=betaPrice*(prediction[0][0]-amount)

newPrice = currentPrice - changeInPrice

priceAndQ = [[item,newPrice,amount]]

conn = sqlite3.connect('resto.db')  # connection
c = conn.cursor()
c.execute('DROP TABLE IF EXISTS price')
c.execute('CREATE TABLE IF NOT EXISTS price(item TEXT, price FLOAT, quantity INTEGER)')
c.execute('INSERT INTO price VALUES(?,?,?)', priceAndQ)
conn.commit()
conn.close()



print('Update price to ', newPrice)

books=[['laetitia tam','hack'],['krista bennatti','python']]