import math

from bs4 import BeautifulSoup as BSoup
from tabula import convert_into

import csv
import requests
from datetime import datetime, date

session = requests.session()

raw_data = []
#overall_mean_variances = [0.106802865, 0.191468296, 0.065944493, 0.142714838, 0.203228599, 0.06416601, -0.114002747, 0.071088255, 0.198161485, 0.480192837, 0.198254541, -0.236386928]
overall_mean_variances = [0.046935368, 0.349271934, 0.015730188, 0.104964831, 0.219331373, 0.066125376, -0.13580952, 0.040763284, 0.247060446, 0.298777508, 0.165885977, -0.293639191]
overall_stdev_variances = [0.48164962, 0.626318344, 0.511550704, 0.454368646, 0.393383854, 0.42043275, 0.244046188, 0.580217736, 0.654213661, 0.712783114, 0.459309131, 0.263116568]

months = {
        'Jan': 1,
        'Feb': 2,
        'Mar': 3,
        'Apr': 4,
        'May': 5,
        'Jun': 6,
        'Jul': 7,
        'Aug': 8,
        'Sep': 9,
        'Oct': 10,
        'Nov': 11,
        'Dec': 12,
    }

class Airport():
    name = ''
    iata_code = ''
    city = ''
    state = ''

def sort_distance(e):
    if 'distance' in e:
        return e['distance']

    return 10000

def get_airports_near(city, distance):
    url = "https://www.distance24.org/route.json?stops=" + city
    r = session.get(url)

    soup = BSoup(r.content, 'html5lib')

    json = r.json()

    cities = []

    nearby_cities = json['stops'][0]['nearByCities'] # Gets names of nearby cities
    nearby_cities.sort(key = sort_distance) # Sorts by distance from given city

    for city in nearby_cities:
        if 'distance' in city:
            if city['distance'] < distance: # Only adds cities below the threshold
                cities.append(city['city'])
        else:
            cities.append(city['city'])

    return cities

def get_flight_data(depart, arrival):
    url = "https://www.faredetective.com/faredetective/chart_data"
    r = session.post(url, data={'arrival': arrival, 'departure': depart})

    #print("Departure: " + depart)
    #print("Arrival: " + arrival)

    chart_data = r.json()['chart_data']

    temp_data = [depart, arrival, {}, {}] # Initializing data entry

    price = 0
    month_count = 0
    temp_month_count = 0
    month = ""

    for i in range(len(chart_data)): # For every month data
        item = chart_data[i] # All relevant info

        info = item['year'].split("\n")
        info.append(item['price'])

        if not month:  # First month data
            month = info[0]
            year = int(info[1])
        elif info[0] != month:  # When you get to the next month (some months have multiple data points)
            temp_data[2][months[month]] = price / temp_month_count # Sets months price to the average of each data point

            # Reset info for next month
            price = 0
            temp_month_count = 0
            month_count += 1
            month = info[0]

        temp_month_count += 1
        price += float(info[2])

        if i == len(chart_data) - 1: # Last month
            temp_data[2][months[month]] = price / temp_month_count # Sets months price to the average of each data point
            month_count += 1

    if month_count > 0: # If any data at all
        prices = temp_data[2]

        for key, price in prices.items(): # For every month's price
            key2 = key + 1 if key < 12 else 1  # Ensures that Dec to Jan gets calculated (wraps around to 1 if at the end of the list)

            if key2 in prices:  # If two consecutive months have data points
                price2 = prices[key2]

                difference = (price2 - price) / price

                #if difference > 10:
                    #difference -= difference - 10

                temp_data[3][key] = difference  # Calculates change in price

        return temp_data

    return False

codes_url = "https://www.nationsonline.org/oneworld/IATA_Codes/airport_code_list.htm"
codes_r = session.get(codes_url)
codes_soup = BSoup(codes_r.content, 'html5lib')

def get_all_codes(cities):
    total_codes = []

    for city in cities:
        total_codes += get_codes(city)

    return total_codes

# Parses a website for a list of IATA codes
def get_codes(city):
    divs = codes_soup.findAll('a', text = city)
    divs2 = codes_soup.findAll('td', attrs = {'class': 'border1'})

    codes = []

    # Removes duplicates
    for div in divs:
        codes.append(div.parent.parent.findAll('td')[2::3][0].text)
    for div in divs2:
        if city in div.text:
            code = div.parent.findAll('td')[2::3][0].text

            if code not in codes:
                codes.append(div.parent.findAll('td')[2::3][0].text)

    return codes

# Averages the prices and variances
def get_stats(data):
    mean_prices = {}
    mean_variances = {}
    prices_counts = {}
    variances_counts = {}
    stdev_variances = {}

    for route in data:
        for i, price in route[-2].items():
            if i in mean_prices:
                mean_prices[i] += price
                prices_counts[i] += 1
            else:
                mean_prices[i] = price
                prices_counts[i] = 1

        for i, variance in route[-1].items():
            if i in mean_variances:
                mean_variances[i] += variance
                variances_counts[i] += 1
            else:
                mean_variances[i] = variance
                variances_counts[i] = 1

    for i, variance in mean_variances.items():
        variance /= variances_counts[i]

    for i, price in mean_prices.items():
        price /= prices_counts[i]

    for x in range(len(overall_mean_variances)):
        if x + 1 not in mean_variances:
            mean_variances[x + 1] = overall_mean_variances[x] # Substitutes the overall variance if not is found

    stdev_totals = {}
    stdev_counts = {}

    for route in data:
        for i, variance in route[-1].items():
            if i in stdev_totals:
                stdev_totals[i] += math.pow(variance - mean_variances[i], 2)
                stdev_counts[i] += 1
            else:
                stdev_totals[i] = math.pow(variance - mean_variances[i], 2)
                stdev_counts[i] = 1

    for i, stdev_total in stdev_totals.items():
        if stdev_counts[i] > 1:
            stdev_variances[i] = math.sqrt(stdev_total / (stdev_counts[i] - 1))
        else:
            print("STDEV COUNT: " + str(stdev_counts[i]))

    for x in range(len(overall_stdev_variances)):
        if x + 1 not in stdev_variances:
            stdev_variances[x + 1] = overall_stdev_variances[x] # Substitutes the overall standard deviation if not is found

    return mean_prices, mean_variances, stdev_variances

def get_final_data(depart, arrival):
    cities1 = get_all_codes(get_airports_near(depart, 200))[:7] # Gets codes of nearby cities
    cities2 = get_all_codes(get_airports_near(arrival, 200))[:7]

    print("\n" + depart + ": " + str(cities1))
    print(arrival + ": " + str(cities2) + "\n")

    flight_data = []
    return_data = {}

    for city1 in cities1:
        for city2 in cities2:
            if city1 != city2:
                result = get_flight_data(city1, city2) # Gathers all flight data for nearby cities

                if result:
                    flight_data.append(result)

    mean_prices, mean_variances, stdev_variances = get_stats(flight_data)

    print("STDEVS: " + str(stdev_variances))

    today = datetime.today()
    month_index = datetime.today().month # An index of 3 means from March to April

    if today.day < 15: # Instead of a single trendline, this uses a linear trend from month to month (15th to 15th)
        month_index = month_index - 1 if month_index > 1 else 12

    predicted_variance = mean_variances[month_index]
    predicted_price = 0.0

    print("PREDICTED VARIANCE: " + str(predicted_variance))

    depart_codes = get_codes(depart)
    arrival_codes = get_codes(arrival)

    print(arrival_codes)

    if depart_codes != [] and arrival_codes != []:
        depart_code = get_codes(depart)[0]
        arrival_code = get_codes(arrival)[0]

        route_data = get_flight_data(depart_code, arrival_code) # Gets the user's requested flight data

        if not route_data: # If nothing is found by using the codes, use the cities names instead
            print("ERROR 1")

            route_data = get_flight_data(depart, arrival)
    else:
        route_data = get_flight_data(depart, arrival)

    if route_data:
        month_from = list(months.keys())[month_index - 1]
        month_to =  list(months.keys())[month_index]

        price_from = 0
        price_to = 0

        if (month_index in route_data[2]):
            price_from = route_data[2][month_index]
        else: # Uses average price from nearby cities if nothing is found
            print("===/// USING MEAN PRICE from ///===")
            price_from = mean_prices[month_index]

        if (month_index + 1 in route_data[2]):
            price_to = route_data[2][month_index + 1]
        else: # Uses average price from nearby cities if nothing is found
            print("===/// USING MEAN PRICE to ///===")
            price_to = mean_prices[month_index + 1]

        print(month_from + ": " + str(price_from))
        print(month_to + ": " + str(price_to))

        days_since_last = (today.date() - date(2020, month_index, 15)).days # How far along the month

        print("days since: " + str(days_since_last))

        predicted_price = price_from * (1 + (days_since_last * predicted_variance) / 30) # Calculates the predicted price
        lower_bound = price_from * (1 + (days_since_last * (predicted_variance - stdev_variances[month_index])) / 30)
        upper_bound = price_from * (1 + (days_since_last * (predicted_variance + stdev_variances[month_index])) / 30)

        print("PREDICTED PRICE: " + str(predicted_price))
    else:
        print("ERROR 2")
        print(route_data)

    print("")

    return_data['predicted_price'] = round(predicted_price, 2)
    return_data['lower_bound'] = round(lower_bound, 2)
    return_data['upper_bound'] = round(upper_bound, 2)

    return return_data

'''for data in raw_data:
    print(data[0] + " to " + data[1] + "\n========================================")

    for x in range(1, 12):
        if x in data[2]:
            print(list(months.keys())[x] + ": $" + str(round(data[2][x], 2)), end = '')

            if x in data[3]:
                print(" || Change to " + list(months.keys())[x + 1 if x < 11 else 0] + ": /" + str(round(data[3][x] * 100, 2)) + "%", end = '')

            print("")

    print("")'''