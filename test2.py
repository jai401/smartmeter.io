import matplotlib.pyplot as plt
import pandas as pd
import numpy as np



#graph1   
dd2=[14,50,34]

g1=100
ax=dd2
dd1=['2018','2019','2020']

doc = dd1 #list(data.keys())
values = dd2 #list(data.values())
  
fig = plt.figure(figsize = (10, 5))

c=['red','blue','green']
# creating the bar plot
plt.bar(doc, values, color =c,
        width = 0.4)

plt.ylim((1,g1))

plt.xlabel("Year")
plt.ylabel("Energy Consumption")
plt.title("")


fn="graph1.png"
plt.xticks(rotation=20)

plt.savefig('static/'+fn)

#plt.close()
plt.clf()
