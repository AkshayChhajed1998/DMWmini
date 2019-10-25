from django.shortcuts import render,HttpResponse
import pandas as pd
import numpy as np
from mlxtend.preprocessing import TransactionEncoder
from django.views.decorators.csrf import csrf_exempt

def makeSelectiveSportDataset(fromData,sport,colList):
    toData = fromData[fromData['Sport'] == sport]
    toData =toData[colList]
    #to.head(5)
    med = ['Gold','Silver','Bronze']
    toData = toData[toData.Medal.isin(med)]
    return(toData)

def applyApriori(dataset,support):
    rec = dataset.values.tolist()
    # Finding Frequent Item Sets

    te = TransactionEncoder()
    te_ary = te.fit(rec).transform(rec)
    df = pd.DataFrame(te_ary, columns=te.columns_)
    
    # Applying Aprioi Algo
    from mlxtend.frequent_patterns import apriori
    
    freq_Itemsets =  apriori(df,min_support = support, use_colnames = True)
    freq_Itemsets['length'] = freq_Itemsets['itemsets'].apply(lambda x:len(x))
    return(freq_Itemsets[freq_Itemsets['length'] > 1])

# Create your views here.
def initialize(request):
  od = pd.read_csv('./assets/processed_dataset/processed_olympicdata.csv')
  index = od['Sport'].drop_duplicates().tolist()
  id_index = [x for x in range(0,len(index)) ]
  return render(request,'FDI_apriori/apriori.html',{'sports': index,
                                                      'id' : id_index})
@csrf_exempt
def perform(request):
  sport = request.POST['sport']
  od = pd.read_csv('./assets/processed_dataset/processed_olympicdata.csv')
  print(sport)
  sod = makeSelectiveSportDataset(od,sport,['Sex','Age', 'Height','Weight','Team','Medal'])
  fdi = applyApriori(sod,0.4)
  return HttpResponse(fdi.to_html(classes="ui celled striped selectable inverted purple table",table_id = "table"))
