import csv
import math
import urllib
from urllib.parse import urlencode

from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse

from app.settings import BUS_STATION_CSV


def index(request):
    return redirect(reverse(bus_stations))


def data_get(file):
    with open(file, encoding='cp1251') as csvfile:
        list_of_dict = list()
        for row in csv.DictReader(csvfile):
            list_of_dict.append({x: row[x] for x in ['Name', 'Street', 'District']})
    return list_of_dict


def bus_stations(request):
    list_of_dict = data_get(BUS_STATION_CSV)
    current_page = int(request.GET.get('page', 1))
    items_per_page = 10
    paginator = Paginator(list_of_dict, items_per_page)
    prev_page, next_page = None, None
    if current_page < 1 or current_page > math.ceil(len(list_of_dict) / items_per_page):
        current_page = 1
    if current_page > 1:
        prev_page = urlencode({'page': current_page - 1})
    if current_page * items_per_page < len(list_of_dict):
        next_page = urlencode({'page': current_page + 1})
    return render(request, 'index.html', context={
        'bus_stations': paginator.get_page(current_page).object_list,
        'current_page': current_page,
        'prev_page_url': f'{reverse(bus_stations)}?{prev_page}',
        'next_page_url': f'{reverse(bus_stations)}?{next_page}',
    })
