from pandas import DataFrame, read_csv
import matplotlib.pyplot as plt
import pandas as pd
import os

print 'Pandas version ' + pd.__version__

names = ['Bob','Jessica','Mary','John','Mel']
births = [968, 155, 77, 578, 973]

BabyDataSet = zip(names,births)
#print BabyDataSet

df = DataFrame(data = BabyDataSet, columns=['Names', 'Birth_Count'])
#print df

df.to_csv('births1980.csv',index=False,header=False)

Location = r'births1980.csv'

inp = read_csv(Location,header=None,names=['Names','Birth_Count'])

print inp
#print inp.dtypes

inp['Birth_Count'].plot()

mx_value = inp['Birth_Count'].max()
mx_name = inp['Names'][inp['Birth_Count'] == mx_value].values

Text = str(mx_value) + " - " + mx_name

# Add text to graph
plt.annotate(Text, xy=(1, mx_value), xytext=(8, 0), 
                 xycoords=('axes fraction', 'data'), textcoords='offset points')

print "The most popular name"
inp[inp['Birth_Count'] == inp['Birth_Count'].max()]

os.remove(Location)

plt.show()


