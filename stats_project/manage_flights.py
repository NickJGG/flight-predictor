from bs4 import BeautifulSoup as BSoup
from tabula import convert_into

import csv
import requests

session = requests.session()

raw_data = []

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

def get_airports_near(city, distance):
    url = "https://www.distance24.org/route.json?stops=" + city
    r = session.get(url)

    soup = BSoup(r.content, 'html5lib')

    json = r.json()

    cities = []

    for city in json['stops'][0]['nearByCities']:
        if city['distance'] < distance:
            cities.append(city['city'])

    return cities

def get_flight_data(depart, arrival):
    url = "https://www.faredetective.com/faredetective/chart_data"
    r = session.post(url, data={'arrival': arrival, 'departure': depart})

    #print("Departure: " + depart)
    #print("Arrival: " + arrival)

    chart_data = r.json()['chart_data']

    # Initializing data entry
    temp_data = [depart, arrival, {}, {}]

    price = 0
    month_count = 0
    temp_month_count = 0
    month = ""

    for i in range(len(chart_data)):
        item = chart_data[i]

        info = item['year'].split("\n")
        info.append(item['price'])

        if not month:  # First chart data
            month = info[0]
            year = int(info[1])
        elif info[0] != month:  # When you get to the next month (some months have multiple data points)
            temp_data[2][months[month]] = price / temp_month_count # Sets months price to the average of each data point

            # Reset info for next month
            price = 0
            temp_month_count = 0
            month_count += 1
            month = info[0]

            #print(temp_data[-1])

        temp_month_count += 1
        price += float(info[2])

        if i == len(chart_data) - 1:
            temp_data[2][months[month]] = price / temp_month_count # Sets months price to the average of each data point
            month_count += 1

            #print(temp_data[-1])

    #print(temp_data)

    if month_count > 0:
        prices = temp_data[2]

        for key, price in prices.items():
            key2 = key + 1 if key < 12 else 1  # Ensures that Dec to Jan gets calculated (wraps around to 1 if at the end of the list)

            if key2 in prices:  # If two consecutive months have data points
                price2 = prices[key2]

                difference = (price2 - price) / price

                #if difference > 10:
                    #difference -= difference - 10

                temp_data[3][key] = difference  # Calculates change in price

        raw_data.append(temp_data)  # Add to total data

codes_url = "https://www.nationsonline.org/oneworld/IATA_Codes/airport_code_list.htm"
codes_r = session.get(codes_url)
codes_soup = BSoup(codes_r.content, 'html5lib')

def get_all_codes(cities):
    total_codes = []

    for city in cities:
        total_codes += get_codes(city)

    return total_codes

def get_codes(city):
    divs = codes_soup.findAll('a', text = city)
    divs2 = codes_soup.findAll('td', attrs = {'class': 'border1'})

    codes = []

    for div in divs:
        codes.append(div.parent.parent.findAll('td')[2::3][0].text)
    for div in divs2:
        if city in div.text:
            code = div.parent.findAll('td')[2::3][0].text

            if code not in codes:
                codes.append(div.parent.findAll('td')[2::3][0].text)

    return codes

def get_final_data(depart, arrival):
    cities1 = get_all_codes(get_airports_near(depart, 200))[:7]
    cities2 = get_all_codes(get_airports_near(arrival, 200))[:7]

    print(depart + ": " + str(cities1))
    print(arrival + ": " + str(cities2))

    for city1 in cities1:
        for city2 in cities2:
            get_flight_data(city1, city2)

    return raw_data

'''for data in raw_data:
    print(data[0] + " to " + data[1] + "\n========================================")

    for x in range(1, 12):
        if x in data[2]:
            print(list(months.keys())[x] + ": $" + str(round(data[2][x], 2)), end = '')

            if x in data[3]:
                print(" || Change to " + list(months.keys())[x + 1 if x < 11 else 0] + ": /" + str(round(data[3][x] * 100, 2)) + "%", end = '')

            print("")

    print("")'''