import pandas as pd 
df = pd.read_csv("dataset/C1.csv")

print(df.head())

print(df.tail())

df.index = df['month']
del df['month']
print(df.head())

import matplotlib.pyplot as plt
import seaborn as sns


df['year'] = df.index
train = df['year'] < 2022
train['train'] = train['#Passengers']
del train['Date']
del train['#Passengers']
test = df['year'] >= 2019
del test['year']
test['test'] = test['#Passengers']
del test['#Passengers']
plt.plot(train, color = "black")
plt.plot(test, color = "red")
plt.title("Train/Test split for Passenger Data")
plt.ylabel("Passenger Number")
plt.xlabel('Year-Month')
sns.set()
plt.show()
