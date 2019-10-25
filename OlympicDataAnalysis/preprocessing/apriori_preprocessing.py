#Pre Processing for Apriori

import pandas as pd
import numpy as np

olympic_data = pd.read_csv('./raw_dataset/athlete_events.csv')
print(olympic_data.head(5))
print(olympic_data.shape)
print(olympic_data.columns)
print(olympic_data.isna().sum())

#Imputting Age with its Mode

AgeMode = int(olympic_data['Age'].mode()[0])
olympic_data['Age'] = olympic_data['Age'].fillna(AgeMode)
print(olympic_data['Age'].isna().sum())

#Imputting Height with its Mode

HeightMode = olympic_data['Height'].mode()[0]
olympic_data['Height'] = olympic_data['Height'].fillna(HeightMode)
print(olympic_data['Height'].isna().sum())

#Imputting Weight with its mode

WeightMode = olympic_data['Weight'].mode()[0]
olympic_data['Weight'] = olympic_data['Weight'].fillna(WeightMode)
print(olympic_data['Weight'].isna().sum())

#Imputting Medal by replacing it with None
olympic_data['Medal'] = olympic_data['Medal'].fillna("None")
print(olympic_data['Medal'].isna().sum())

#group
def group(data,col,span):
  data[col] = data[col].map(lambda value : '('+col+':'+str(int(value/span)*span)+'-'+str((int(value/span)+1)*span)+')')

group(olympic_data,'Age',10)
group(olympic_data,'Weight',10)
group(olympic_data,'Height',10)

print(olympic_data.head()['Weight'])

olympic_data.to_csv('./processed_dataset/processed_olympicdata.csv')