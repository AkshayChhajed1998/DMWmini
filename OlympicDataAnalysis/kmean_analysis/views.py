from django.shortcuts import render,HttpResponse
import mpld3
from django.views.decorators.csrf import csrf_exempt
import pandas as pd 
import numpy as np
from copy import deepcopy
from matplotlib import pyplot as plt
import plotly.offline as offline
import plotly.graph_objs as go
import json
plt.style.use('ggplot')

# Create your views here.
def initialize(request):
  od = pd.read_csv('./assets/processed_dataset/processed_olympic_gdp_pop.csv')
  index = [int(x) for x in od['Year'].drop_duplicates().tolist() if int(x)>=1960]
  index.sort()
  print(index)
  return render(request,'kmean_analysis/kmeans.html',{'years':index})

@csrf_exempt
def perform(request):
  s=request.POST['type']
  year = int(request.POST['year'])
  return render(request,'kmean_analysis/kmeans.html',fig(s,year))

def fig(s,year=2016):
  olympics_complete = pd.read_csv('./assets/processed_dataset/processed_olympic_gdp_pop.csv')
  olympics_complete['Medal_Won'] = np.where(olympics_complete.loc[:,'Medal'] == 'None', 0, 1)
  medalC = olympics_complete.groupby(['Team'])['Medal_Won'].agg('sum').reset_index()
  medal_count_per_country = medalC.sort_values('Medal_Won',ascending = False)
  TYG = olympics_complete[olympics_complete['Year'] == year ][['Team','Year','GDP']]
  gdp = {}
  for index,row in TYG.iterrows():
      if TYG.loc[index,'Team'] not in gdp:
          gdp[TYG.loc[index,'Team']] = TYG.loc[index,'GDP']
  medal_count_per_country['GDP'] = medal_count_per_country['Team'].map(gdp)
  medal_count_per_country['GDP'] = medal_count_per_country['GDP'].fillna(1)
  
  TYP = olympics_complete[olympics_complete['Year'] == year][['Team','Year','Population']]
  popu = {}
  for index,row in TYP.iterrows():
      if TYP.loc[index,'Team'] not in popu:
          popu[TYP.loc[index,'Team']] = TYP.loc[index,'Population']
  medal_count_per_country['Population'] = medal_count_per_country['Team'].map(popu)
  medal_count_per_country['Population'] = medal_count_per_country['Population'].fillna(1)
  medal_count_per_country = medal_count_per_country[medal_count_per_country['Population']>10000]
  
  medal_count_per_country['Medal_WonNorm'] = (medal_count_per_country['Medal_Won']-medal_count_per_country['Medal_Won'].mean())/np.std(medal_count_per_country['Medal_Won'],axis = 0)
  medal_count_per_country['GDPNorm'] = (medal_count_per_country['GDP']-medal_count_per_country['GDP'].mean())/np.std(medal_count_per_country['GDP'],axis = 0)
  medal_count_per_country['PopulationNorm'] = (medal_count_per_country['Population']-medal_count_per_country['Population'].mean())/np.std(medal_count_per_country['Population'],axis = 0)
  topMedalHolders = medal_count_per_country
  from sklearn.cluster import KMeans
  wcss = []
  for i in range(1, 11):
      kmeans = KMeans(n_clusters = i, init = 'k-means++', random_state = 42)
      kmeans.fit(topMedalHolders.iloc[:, [4, 5]].values)
      wcss.append(kmeans.inertia_)
  if s=='GDPNorm':
    fig1_a='SUM of SQUARE of DISTANCE from RESPECTIVE CENTEROID'
    fig2_a='KMEAN for MEDAL WON VS GDP'
    ti='GDP'
  else:
    fig1_a='SUM of SQUARE of DISTANCE from RESPECTIVE CENTEROID'
    fig2_a='KMEAN for MEDAL WON VS POPULATION'
    ti='Population'
  fig1 = offline.plot({"data":[go.Scatter(x=[1,2,3,4,5,6,7,8,9,10],y=wcss,mode="lines",marker=dict(
    size=16,
    color= [0,1,2,3,4,5,6,7,8,9], #set color equal to a variable
    colorscale= 'Rainbow', # one of plotly colorscales
    showscale=True
  ))],"layout": go.Layout(title=fig1_a,xaxis={'title':'Number of Cluster'},yaxis={'title':'Sum of Square of each point from respective centroid'})},include_plotlyjs=False,output_type='div')
  print(wcss)
  print("Number of clusters:"+str(wcss.index(min(wcss))+1))
  kmeans = KMeans(n_clusters = 4, init = 'k-means++', random_state = 42)
  y_kmeans = kmeans.fit_predict(topMedalHolders[['Medal_WonNorm',s]])
  centroids = kmeans.cluster_centers_
  y_kmeans1=y_kmeans
  y_kmeans1=y_kmeans+1
  cluster = pd.DataFrame(y_kmeans1)
  topMedalHolders['cluster'] = cluster
  kmeans_mean_cluster = pd.DataFrame(round(topMedalHolders.groupby('cluster').mean(),1))
  fig2=offline.plot({"data":[go.Scatter(x=topMedalHolders['Medal_WonNorm'],y=topMedalHolders[s],mode="markers",marker=dict(
              size=16,
              color= kmeans.labels_.astype(float), #set color equal to a variable
              colorscale='Rainbow', # one of plotly colorscales
              showscale=True))],
            "layout": go.Layout(title=fig2_a,xaxis={'title':'Medal Won'},yaxis={'title':ti})}, include_plotlyjs=False, output_type='div')
  od = pd.read_csv('./assets/processed_dataset/processed_olympic_gdp_pop.csv')
  index = [int(x) for x in od['Year'].drop_duplicates().tolist() if int(x)>=1960]
  index.sort()
  return {
          'fig1':fig1,
          'fig2':fig2,
          'fig1_a':fig1_a,
          'fig2_a':fig2_a,
          'sel':s,
          'years':index,
          'Y':year,
         }