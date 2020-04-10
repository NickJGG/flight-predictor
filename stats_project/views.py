from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from . import manage_flights

def index(request):
    return render(request, 'stats_project/index.html')

def flight_data(request, departure, arrival):
    data = manage_flights.get_final_data(departure, arrival)

    print(data)

    return JsonResponse({'data': data})

# Functions