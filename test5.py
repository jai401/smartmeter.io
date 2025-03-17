import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
#Importing data
df = pd.read_csv('dataset/C1.csv')
#Printing head
df.head()

#Subsetting the dataset
#Index 11856 marks the end of year 2013
df = pd.read_csv('dataset/C1.csv', nrows = 36)

#Creating train and test set 
#Index 10392 marks the end of October 2013 
train=df[0:36] 
test=df[12:]

#Aggregating the dataset at daily level
df.Timestamp = pd.to_datetime(df['year'],format='%Y') 
df.index = df.Timestamp 
df = df.resample('year').mean()
train.Timestamp = pd.to_datetime(train.Datetime,format='%Y') 
train.index = train.Timestamp 
train = train.resample('year').mean() 
test.Timestamp = pd.to_datetime(test.Datetime,format='%Y') 
test.index = test.Timestamp 
test = test.resample('year').mean()

#Plotting data
train.Count.plot(figsize=(15,8), title= 'Daily Ridership', fontsize=14)
test.Count.plot(figsize=(15,8), title= 'Daily Ridership', fontsize=14)
plt.show()
