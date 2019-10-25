# -*- coding: utf-8 -*-
"""
Created on Sun Oct 20 22:56:43 2019

@author: WorkStation
"""

def Itemset(T):
    itemset = []
    for t in T:
        for i in t:
            if [i] not in itemset:
                itemset.append([i])
    return itemset

def calculateSupport(li,T):
    count = 0;
    for t in T:
        if set(li).issubset(set(t)):
            count=count+1
    return float(count)/float(len(T))

def genL1(itemset,support,T):
    C1=[]
    for i in itemset:
        C1.append([i,calculateSupport(i,T)])
    return genL(C1,support)

def genNewLI(s1,s2):
    if len(list(set(s1)-set(s2)))==1 and len(list(set(s2)-set(s1)))==1:
        return list(set(s1).union(set(s2)))
    return None

def genC(preL,T):
    C = []
    for i in range(0,len(preL)):
        for j in range(i+1,len(preL)):
            n = genNewLI(preL[i][0],preL[j][0])
            if n is not None:
                y = [n,calculateSupport(n,T)]
                if y not in C:
                    C.append(y)
    return C
        

def genL(C,support):
    L = []
    for li in C:
        if li[1] >= support:
          L.append(li)
    return L

def Apriori(T,support):
    itemset = Itemset(T)
    L = []
    C = []
    C.append([])
    L.append(genL1(itemset,support,T))
    k = 1
    while len(L[k-1]) != 0:
        C.append(genC(L[k-1],T))
        L.append(genL(C[k],support))
        k = k+1
    return L

T = [
     ['milk','bread','toast','onion','jam','potato','burger','sauce','ginger'],
     ['milk','bread'],
     ['milk','bread','toast'],
     ['milk','bread','toast','burger'],
     ['milk','bread','toast','potato'],
     ['onion','jam','potato','burger','sauce','ginger'],
     ['onion','jam','potato','burger','sauce','ginger','milk'],
     ['onion','jam','potato','burger','sauce','bread'],
     ['onion','jam','potato','burger','sauce'],
     ['onion','jam','potato','burger'],
     ['onion','jam','potato','burger','milk'],
     ]

print(Apriori(T,0.6))