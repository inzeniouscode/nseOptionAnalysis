import requests
import json
import math

from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from collections import namedtuple

from nseOptionDataUpdate.models import nseOptionData

# Create your views here.

url_oc  = "https://www.nseindia.com/option-chain"
url_mq  = 'https://www.nseindia.com/api/master-quote'
url_stk =  'https://www.nseindia.com/api/option-chain-equities?symbol=RELIANCE'
url_nifty = 'https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY'


headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
            'accept-language': 'en,gu;q=0.9,hi;q=0.8',
            'accept-encoding': 'gzip, deflate, br'}

sess = requests.Session()
cookies = dict()


# Local methods
def set_cookie():
    request = sess.get(url_oc, headers=headers, timeout=5)
    cookies = dict(request.cookies)

def get_data(url):
    set_cookie()
    response = sess.get(url, headers=headers, timeout=5, cookies=cookies)
    if(response.status_code==401):
        set_cookie()
        #response = sess.get(url_nf, headers=headers, timeout=5, cookies=cookies)
    if(response.status_code==200):
        return response.json()
    return ""

def set_header(get_url):
    global bnf_ul
    global nf_ul
    global bnf_nearest
    global nf_nearest
    response_text = get_data(get_url)
    #data = response_text.json()
    return response_text


# Showing Header in structured format with Last Price and Nearest Strik

def nseOptionData_save(request):
    try:
        cursor = connection.cursor()
        cursor.execute("TRUNCATE TABLE `nseOptionData`")
        data = set_header(url_stk)
        if "records" in data:
            records = data['records']['data']
            for item in records:
                nseOCD = nseOptionData.objects.create(strikePrice = item['strikePrice'], expiryDate = datetime.strptime(item['expiryDate'],"%d-%b-%Y").date() )
                if "CE" in item:
                    nseOCD.underlying = item['CE']['underlying']
                    nseOCD.identifierCall = item['CE']['identifier']
                    nseOCD.underlyingValue = item['CE']['underlyingValue']
                    nseOCD.openInterestCall = item['CE']['openInterest']
                    nseOCD.changeinOpenInterestCall = item['CE']['changeinOpenInterest']
                    nseOCD.pchangeinOpenInterestCall = item['CE']['pchangeinOpenInterest']
                    nseOCD.totalTradedVolumeCall = item['CE']['totalTradedVolume']
                    nseOCD.impliedVolatilityCall = item['CE']['impliedVolatility']
                    nseOCD.lastPriceCall = item['CE']['lastPrice']
                    nseOCD.changeCall = item['CE']['change']
                    nseOCD.pChangeCall = item['CE']['pChange']
                    nseOCD.totalBuyQuantityCall = item['CE']['totalBuyQuantity']
                    nseOCD.totalSellQuantityCall = item['CE']['totalSellQuantity']
                    nseOCD.bidQtyCall = item['CE']['bidQty']
                    nseOCD.bidpriceCall = item['CE']['bidprice']
                    nseOCD.askQtyCall = item['CE']['askQty']
                    nseOCD.askPriceCall = item['CE']['askPrice']
                if "PE" in item:
                    nseOCD.underlying = item['PE']['underlying']
                    nseOCD.identifierPut = item['PE']['identifier']
                    nseOCD.underlyingValue = item['PE']['underlyingValue']
                    nseOCD.openInterestPut =  item['PE']['openInterest']
                    nseOCD.changeinOpenInterestPut =  item['PE']['changeinOpenInterest']
                    nseOCD.pchangeinOpenInterestPut =  item['PE']['pchangeinOpenInterest']
                    nseOCD.totalTradedVolumePut =  item['PE']['totalTradedVolume']
                    nseOCD.impliedVolatilityPut =  item['PE']['impliedVolatility']
                    nseOCD.lastPricePut =  item['PE']['lastPrice']
                    nseOCD.changePut =  item['PE']['change']
                    nseOCD.pChangePut =  item['PE']['pChange']
                    nseOCD.totalBuyQuantityPut =  item['PE']['totalBuyQuantity']
                    nseOCD.totalSellQuantityPut =  item['PE']['totalSellQuantity']
                    nseOCD.bidQtyPut =  item['PE']['bidQty']
                    nseOCD.bidpricePut =  item['PE']['bidprice']
                    nseOCD.askQtyPut =  item['PE']['askQty']
                    nseOCD.askPricePut =  item['PE']['askPrice']
                nseOCD.save()
                
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise
    #return render(request, 'optionAnalysis.html')

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]    

def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]    

def renderOptionAnalysis(request):
    #nseOptionData_save(request)
    cursor = connection.cursor()
    cursor.execute("SELECT `optionName`, `strikePrice`, DATE_FORMAT(`expiryDate`,'%Y-%b-%d') expiryDate, `currentValue`, `lastPriceCall`, `openInterestCall`, `callPremium`, `lastPricePut`, `openInterestPut`, `putPremium` FROM `nseoptiondataview`;")
    nseoptionview = dictfetchall(cursor)
    #nseoptionview = cursor.fetchall()
    return render(request, 'optionAnalysis.html',{'nseoptionview': nseoptionview})

