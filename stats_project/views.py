from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from . import manage_flights

def index(request):
    return render(request, 'stats_project/index.html')

def flight_data(request, departure, arrival, amount_cap, distance_cap):
    data = manage_flights.get_final_data(departure, arrival, amount_cap, distance_cap)

    #print(data)

    return JsonResponse(data)
# Functions