# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 23:00:51 2019

@author: WorkStation
"""
import pandas as pd

df = pd.DataFrame([['Rainy','Hot','High',False,'No'],
['Rainy','Hot','High',True,'No'],
['Overcast','Hot','High',False,'Yes'],
['Sunny','Mild','High',False,'Yes'],
['Sunny','Cool','Normal',False,'May be'],
['Sunny','Cool','Normal',True,	'No'],
['Overcast','Cool','Normal',True,'Yes'],
['Rainy','Mild','High',False,'No'],
['Rainy','Cool','Normal',False,'Yes'],
['Sunny','Mild','Normal',False,'Yes'],
['Rainy','Mild','Normal',True,'May be'],
['Overcast','Mild','High',True,'May be'],
['Overcast','Hot','Normal',False,'May be'],
['Sunny','Mild','High',	True,'No']],columns=['OUTLOOK','TEMPERATURE','HUMIDITY','WINDY','PLAY'])

#print(df)


def pred_classes(df,f):
    classes = []
    for c in df[f]:
        if c not in classes:
            classes.append(c)
    return classes

def feature_classes(df,f):
    classes = []
    for c in df[f]:
        if c not in classes:
            classes.append(c)
    return classes

def probability(A,B):
    return float(A)/float(B)

def total_count(df,pcs,pf):
    count = [0]*len(pcs)
    for i in range(0,len(pcs)):
        for row in df[pf]:
            #print(row)
            if row == pcs[i]:
                count[i]=count[i]+1
    return count

def feature_predclass(df,f,pc):
    fc = feature_classes(df,f)
    pcs = pred_classes(df,pc)
    pcscount = total_count(df,pcs,pc)
    data = []
    for c in fc:
        r = []
        r.append(c)
        for i in range(1,len(pcs)+1):
            r.append(0)
        for row in df[[f,pc]].values:
            for i in range(0,len(pcs)):
                if row[0]==c and row[1]==pcs[i]:
                    r[i+1]=r[i+1]+1
                    break
        for i in range(1,len(pcs)+1):
            r.append(probability(r[i],pcscount[i-1]))
        data.append(r)
    return pd.DataFrame(data,columns=[f]+pcs+['P(feature|'+p+')' for p in pcs])

#print(df)       
#print(total_count(df,pred_classes(df,'PLAY'),'PLAY'))
#print(feature_predclass(df,'OUTLOOK','PLAY'))
#print(feature_predclass(df,'TEMPERATURE','PLAY'))
#print(feature_predclass(df,'HUMIDITY','PLAY'))
#print(feature_predclass(df,'WINDY','PLAY'))

def inde_p(dfa,fv,pc):
    p=1
    for key in fv.keys():
        d = dfa[key]
        p=p*(d.loc[d[key] == fv[key],'P(feature|'+pc+')'].values[0])
    return p

def NB(df,pf,fv):
    dfa = dict()
    for f in fv.keys():
        dfa[f]=feature_predclass(df,f,pf)
    pp = dict()
    pcs = pred_classes(df,pf)
    pcscount = total_count(df,pcs,pf)
    for i in range(0,len(pcs)):
        pp[pcs[i]] = pcscount[i]*inde_p(dfa,fv,pcs[i])/len(df)
    sum1 = 0
    for i in pp.keys():
        sum1 = sum1 + pp[i]
    for i in pp.keys():
        pp[i] = pp[i]/sum1
    clas = ''
    ma = 0
    for i in pp.keys():
       if ma < pp[i]:
           ma = pp[i]
           clas = i
    return clas

print(NB(df,'PLAY',{'OUTLOOK':'Rainy','TEMPERATURE':'Mild','HUMIDITY':'Normal','WINDY':True}))
        
        
    
