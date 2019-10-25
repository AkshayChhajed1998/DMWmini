#Pre Processing for Kmeans

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

#Merging multiple datasets

noc_country = pd.read_csv('./raw_dataset/noc_regions.csv')
noc_country.drop('notes',axis=1,inplace=True)
noc_country.rename(columns = {'region':'Country'},inplace=True)

olympic_data_m = olympic_data.merge(noc_country,left_on='NOC',right_on='NOC',how='left')


#print(olympic_data_m.head(10))
#print(olympic_data_m.loc[olympic_data_m['Country'].isnull(),['NOC','Team']])
#print(olympic_data_m.loc[olympic_data_m['Country'].isnull(),['NOC','Team']].drop_duplicates().head(12))
#print(olympic_data_m.head(10))

w_gdp = pd.read_csv('./raw_dataset/world_gdp.csv',skiprows = 3)
w_gdp.drop(['Indicator Name', 'Indicator Code'],axis = 1,inplace = True)

w_gdp=pd.melt(w_gdp,id_vars=['Country Name','Country Code'], var_name='Year',value_name='GDP')
w_gdp['Year'] = pd.to_numeric(w_gdp['Year'])
w_gdp.head()

olympic_data_m.loc[olympic_data_m['Country'].isnull(), ['Country']] = olympic_data_m['Team']

olympic_data_m['Country'] = np.where(olympic_data_m['NOC']=='SGP', 'Singapore', olympic_data_m['Country'])
olympic_data_m['Country'] = np.where(olympic_data_m['NOC']=='ROT', 'Refugee Olympic Athletes', olympic_data_m['Country'])
olympic_data_m['Country'] = np.where(olympic_data_m['NOC']=='UNK', 'Unknown', olympic_data_m['Country'])
olympic_data_m['Country'] = np.where(olympic_data_m['NOC']=='TUV', 'Tuvalu', olympic_data_m['Country'])


# Put these values from Country into Team
olympic_data_m.drop('Team', axis = 1, inplace = True)
olympic_data_m.rename(columns = {'Country': 'Team'}, inplace = True)

# Merge to get country code
olympic_data_m_ccode = olympic_data_m.merge(w_gdp[['Country Name', 'Country Code']].drop_duplicates(),
                                            left_on = 'Team',
                                            right_on = 'Country Name',
                                            how = 'left')

olympic_data_m_ccode.drop('Country Name', axis = 1, inplace = True)

# Merge to get gdp too
olympic_data_m_gdp = olympic_data_m_ccode.merge(w_gdp,
                                                left_on = ['Country Code', 'Year'],
                                                right_on = ['Country Code', 'Year'],
                                                how = 'left')

olympic_data_m_gdp.drop('Country Name', axis = 1, inplace = True)

### Merge Population Data

# Read in the population data
w_pop = pd.read_csv('./raw_dataset/world_pop.csv')

w_pop.drop(['Indicator Name', 'Indicator Code'], axis = 1, inplace = True)

w_pop = pd.melt(w_pop, id_vars = ['Country', 'Country Code'], var_name = 'Year', value_name = 'Population')

# Change the Year to integer type
w_pop['Year'] = pd.to_numeric(w_pop['Year'])

w_pop.head()

olympics_complete = olympic_data_m_gdp.merge(w_pop,
                                            left_on = ['Country Code', 'Year'],
                                            right_on= ['Country Code', 'Year'],
                                            how = 'left')

olympics_complete.drop('Country', axis = 1, inplace = True)

olympics_complete.head()

olympics_complete.to_csv('./processed_dataset/processed_olympic_gdp_pop.csv')

