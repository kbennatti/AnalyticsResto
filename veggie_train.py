import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
import random as rand
import datetime
import sqlite3

item = 'veggie'

#train steak model
df=pd.DataFrame()

time = sorted([rand.uniform(10.0,24.0) for element in range(100)])
price = sorted([rand.uniform(5.0,30.0) for element in range(100)])
end_time=23.0
df['Time']=time
df['Time_to_close']=[end_time for row in range(len(time))]-df['Time']
i=1
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
#end training

print(betaPrice)

import pickle
f = open('veggie_clf.pickle', 'wb')
pickle.dump(clf, f)
f.close()
