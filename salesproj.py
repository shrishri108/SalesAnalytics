#!/usr/bin/env python
# coding: utf-8

###########################################################################################
#        CODE WILL PRODUCE THREE GRAPHS.
#        CLOSE THE FIRST GRAPH FOR THE SECOND GRAPH TO APPEAR AND SO ON...
###########################################################################################
import pandas as pd
import os

#import all files by month and merge them into one file
files=[file for file in os.listdir('Sales_Data')]

all_months_data=pd.DataFrame()
for file in files:
    df=pd.read_csv("Sales_Data\\"+file)
    all_months_data=pd.concat([all_months_data,df])
                   
all_months_data.to_csv("all_month_data.csv",index=False)


#read in updated dataframe

all_data=pd.read_csv('all_month_data.csv')
#all_data.head()

#Clean Data of NAN
#Print nans
# nan_df= all_data[all_data.isna().any(axis=1)]
#nan_df.head()
all_data=all_data.dropna(how='any')

#Remove OR element in dataset (anomaly)

all_data=all_data[all_data['Order Date'].str[0:2]!='Or']
#temp_df=all_data[all_data['Order Date'].str[0:2]=='Or']
#temp_df.head()

#Augment data with additional column

#Add month column

all_data['Month']=all_data['Order Date'].str[0:2]
all_data['Month']=all_data['Month'].astype('int32')
all_data.head()

#convert types
all_data['Quantity Ordered']=pd.to_numeric(all_data['Quantity Ordered'])#Make int
all_data['Price Each']=pd.to_numeric(all_data['Price Each'])#Make int

#Add a sales Column
all_data['Sales']=all_data['Quantity Ordered']*all_data['Price Each']

#Add City Column
#use .apply() to run functions on elements of dataset
def get_city(address):
    return address.split(',')[1]
def get_state(address):
    return address.split(',')[2]
all_data['City']=all_data['Purchase Address'].apply(lambda x: get_city(x)+' '+ get_state(x))
#remove redundant state column :   all_data=all_data.drop(columns='State')
#all_data['State']=all_data['Purchase Address'].apply(lambda x: get_state(x))
all_data.head()

#Best month for sales
results=all_data.groupby('Month').sum()

import matplotlib.pyplot as plt
months=range(1,13)
plt.bar(months,results['Sales'])
plt.xticks(months)
plt.ylabel("Sales in $")
plt.xlabel("Month")
plt.show()

#New Task [What City had the Highest number of Sales]
#all_data

result_by_city=all_data.groupby('City').sum()
#result_by_city
#cities=all_data['City'].unique()
cities=[city for city , df in all_data.groupby('City')]
plt.bar(cities,result_by_city['Sales'])
plt.xticks(cities,rotation='vertical')
plt.xlabel('CITIES')
plt.ylabel('Sales (in millions of $)')
plt.show()

#Get order time and distribute over 24 hours to check probability density of sales
all_data['Order Date']=pd.to_datetime(all_data['Order Date'])
all_data['Hour']=all_data['Order Date'].dt.hour
all_data['Minute']=all_data['Order Date'].dt.minute
all_data.head()

hours=[hour for hour, df in all_data.groupby('Hour')]  #Get data in proper order to stop mismatch in plotting

plt.plot(hours,all_data.groupby(['Hour']).count())
plt.xticks(hours)
plt.ylabel('Number of Sales')
plt.grid()
plt.show()