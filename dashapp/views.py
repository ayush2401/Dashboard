from django.shortcuts import render , redirect
from .models import *
import pycountry_convert as pc
from django.http import HttpResponse , HttpResponseRedirect
from django.urls import reverse
from collections import OrderedDict
# Create your views here.

def country_to_continent(country_name):
    country_alpha2 = pc.country_name_to_country_alpha2(country_name)
    country_continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
    country_continent_name = pc.convert_continent_code_to_continent_name(country_continent_code)
    return country_continent_name


def index(request):


    d , l , urls = [] , [] , []
    continents = []
    total_con = {}
    relevance = {}
    likeli = {}
    rel_like = {}
    year = {}
    intensity = {}

    for i in database.find():
        if i["sector"] == "Energy" and i["topic"] != '':
            l.append(i["topic"])

        if i['country'] != "":
            continents.append(country_to_continent(i['country']))

        if i['relevance'] != '' and i['sector'] != '':
            if i['sector'] in relevance:
                value = relevance[i['sector']]
                value[0] += (int)(i['relevance'])
                value[1] += 1
                relevance[i['sector']] = value
            else:
                relevance[i['sector']] = [(int)(i['relevance']) , 1]
        
        if i['likelihood'] != '' and i['sector'] != '':
            if i['sector'] in likeli:
                value = likeli[i['sector']]
                value[0] += (int)(i['likelihood'])
                value[1] += 1
                likeli[i['sector']] = value
            else:
                likeli[i['sector']] = [(int)(i['likelihood']) , 1]
        
        if i['intensity'] != '' and i['sector'] != '':
            if i['sector'] in intensity:
                value = intensity[i['sector']]
                value[0] += (int)(i['intensity'])
                value[1] += 1
                intensity[i['sector']] = value
            else:
                intensity[i['sector']] = [(int)(i['intensity']) , 1]
        

        val = i['start_year']
        if val != '':
            val = int(val)
            if val not in year:
                year[val] = 1
            else:
                year[val] += 1


    for key , values in intensity.items():
        v1 , v2 = values
        avg = round(v1/v2 , 2)
        intensity[key] = avg


    intensity = OrderedDict(sorted(intensity.items() , key=lambda x:x[1]))
    year = OrderedDict(sorted(year.items()))


    most , mval = ['',''] , [0 , 0]
    cat1 , cat2 = [] , []
    sum , tot = 0 , len(relevance)

    for key , values in relevance.items():
        v1 , v2 = values
        avg1 = round(v1 / v2 , 2)
        if avg1 >  mval[0]:
            mval[0] = avg1
            most[0] = key
        
        v1 , v2 = likeli[key]
        avg2 = round(v1 / v2 , 2)
        if avg2 >  mval[1]:
            mval[1] = avg2
            most[1] = key

        sum += abs(avg1 - avg2)
        cat1.append(avg1)
        cat2.append(avg2)

        rel_like[key] = {avg1 , avg2}

    for i in continents:
        total_con[i] = continents.count(i)


    labels = set(l)
    labels = list(labels)
    for i in labels:
        d.append(l.count(i))
    
    # filters form  
    FILTERS = ["end_year" , "sector" , "topic" , "region" , "pestle" , "source" , "country"]

    idx = 0
    options = [[] for i in range(len(FILTERS))]

    for i in FILTERS:
        for j in database.find():
            if j[i] != "":
                options[idx].append(j[i])
        
        options[idx] = set(options[idx])
        options[idx] = list(options[idx])
        idx += 1

    index = [i for i in range(0 , len(total_con))]
   
    
    if request.method == "POST": 
        
        checks = []
        
        
        for i in FILTERS:
            val = request.POST.get(i)
            if val != "":
                checks.append(i)
        
        for i in database.find():
            ok = True
            for j in checks:
                if str(i[j]) != request.POST.get(j):
                    ok = False
                    break
            if ok == True and len(checks) != 0:
                urls.append(i['url'])


    context = {
        'labels':labels,
        'data': d,
        'url':urls,
        'choose':options,
        'index':index,
        'continent':list(total_con.keys()),
        'values':list(total_con.values()),
        'most' : most,
        'mval':mval,
        'year':list(year.keys()),
        'fyear':list(year.values()),
        'bflabel':(list(rel_like.keys()))[:5],
        'cat1':cat1[:5],
        'cat2':cat2[:5],
        'mean':round((sum/tot) , 2),
        'ikey': list(intensity.keys()),
        'ival':list(intensity.values()),
    }

    return render(request , 'index.html' , context=context)


def demo(request):
    return render(request , 'demo.html')


def visual(request):
    return render(request , 'visuals.html')