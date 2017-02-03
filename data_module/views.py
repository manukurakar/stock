"""
This view uploads data from csv to database for processing.

"""

from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import csv
import json
from datetime import datetime
from django.core import serializers
import decimal
from data_module.models import historical_date as hd

# Create your views here.

def data_upload(request):
    """ This method uploads csv data file to database """
    # TODO need to check whether the file already uploaded

    original = file('aapl.csv', 'rU')
    reader = csv.reader(original, delimiter=",")
    for row in reader:
        Date,Open,high,low,close,volume,type = row[0],row[1],row[2],row[3],row[4],row[5],row[6]
        data = hd(date=Date,open=Open,high=high,low=low,close=close,vol=volume,type=type)
        data.save()
    return HttpResponse("Data uploaded Successfully")





def process_data(request):
    """ This method process the request passes the data to template.

    """
    if request.method=="POST":
        data_rcvd = request.POST
        stock = data_rcvd.get('stock')
        frm_date  =data_rcvd.get('frm_date')
        to_date = data_rcvd.get('to_date')

        historical_data = hd.objects.filter(type=stock,date__range=(frm_date,to_date)).order_by('date')
        stock_data1 = []
        stock_data2 = []
        stock_data3 = []
        temp_data1,temp_data2,temp_data3 = {},{},{}
        for items in historical_data:
            t = items.date
            # t.strftime('YYYY-mm-dd')
            # date = str(t)
            date = t.strftime('%Y-%m-%d %H:%M:%S')
            temp_data1['date'] = date
            temp_data1['high'] = float(items.high)
            temp_data1['vol'] = items.vol
            stock_data1.append(temp_data1)

            temp_data2['date'] = date
            temp_data2['low'] = float(items.low)
            temp_data2['vol'] = items.vol
            # stock_data2.append(json.dumps(temp_data2, default=decimal_default))
            stock_data2.append(temp_data2)

            temp_data3['date'] = date
            temp_data3['close'] = float(items.close)
            temp_data3['vol'] = items.vol
            stock_data3.append(temp_data3)

        context = {
            'dataset': historical_data,
            'stock_name':stock,
            'from':frm_date,
            'to':to_date
        }
        return render(request,'_JSON_stockMultipleDataSets.html',context)
    else:
        return render(request,'item_selector.html')