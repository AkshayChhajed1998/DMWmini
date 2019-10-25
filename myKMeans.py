# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 08:59:35 2019

@author: Akshay
                                    KMeans
"""
import math
import pandas as pd
import sys
import random
import plotly.offline as offline
import plotly.graph_objs as go
import numpy as np

def euclidianDistance(p,cp):
    return math.sqrt((p[0]-cp[0])**2+(p[1]-cp[1])**2)

def Classify(k,x,C):
    min_index = -1
    min_dist = sys.maxsize
    for i in range(0,k):
        dist = euclidianDistance(x,C[i].getCentroid())
        if  dist <= min_dist:
            min_index = i
            min_dist = dist
    C[min_index].addToCluster(x)

class Cluster():
    centroid = (0,0)
    cluster = []
    
    def  __init__(self,centroid):
        self.centroid = centroid
        self.cluster = []
        
    def calculateCentroid(self):
        s = [sum(x) for x in zip(*self.cluster)]
        c = [x/len(self.cluster) for x in s]
        if self.centroid == tuple(c):
            return True
        self.centroid = tuple(c)
        return False
    
    def getCluster(self):
        return self.cluster
    
    def getCentroid(self):
        return self.centroid
    
    def addToCluster(self,x):
        self.cluster.append(x)
        
    def removeFromCluster(self,x):
        self.cluster.remove(x)
    
    def clearCluster(self):
        self.cluster.clear()
    
def minMax(df,f):
    minv = sys.maxsize
    maxv = -1
    for x in df[f]:
        if x<minv:
            minv=x
        if x>maxv:
            maxv=x
    return {
            'min':minv,
            'max':maxv
        }
    
def KMeans(k,df,f1,f2):
    df = df[[f1,f2]]
    l = df.values.tolist()
    l = [tuple(x) for x in l]
    f1m = minMax(df,f1)
    f2m = minMax(df,f2)
    C = [Cluster((random.randint(f1m['min'],f1m['max']),random.randint(f2m['min'],f2m['max']))) for i in range(0,k)]
    cond = False
    while not cond:
        for x in l:
            Classify(k,x,C)
        con = [False for i in range(0,k)]
        for i in range(0,k):
            if con[i] == False:
                con[i]=C[i].calculateCentroid()
        cond = True
        for i in con:
            cond = cond and i
        if not cond:
            for i in range(0,k):
                C[i].clearCluster()
    return C


data = [np.random.randint(0,100,2) for i in range(0,200)]
df = pd.DataFrame(data,columns=['age','height'])
k=1
c = KMeans(k,df,'age','height')
labels=[]
x_v=[]
y_v=[]
for i in range(0,k):
    for j in c[i].getCluster():
        labels.append(i)
        x_v.append(j[0])
        y_v.append(j[1])
for i in range(0,k):
    labels.append(k)
    x_v.append(c[i].getCentroid()[0])
    y_v.append(c[i].getCentroid()[1])
fig2=offline.plot({"data":[go.Scatter(x=x_v,y=y_v,mode="markers",marker=dict(
              size=12,
              color=labels,#set color equal to a variable
              colorscale='Rainbow', # one of plotly colorscales
              showscale=True))]})