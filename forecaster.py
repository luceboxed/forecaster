import requests
import json
import datetime
import pytz
import os

#this needs a total rewrite before it can be used
#response_API = requests.get("https://api.openweathermap.org/data/2.5/onecall?lat=31.063&lon=-102.388&units=metric&appid=" + apikey)
#geocode = requests.get("http://api.openweathermap.org/geo/1.0/reverse?lat=31.063&lon=-102.388&limit=1&appid=" + "bec3a5c0a0f97477df0bd71d095ac65d")
#location_data = geocode.json()
#data = response_API.text

#for testing purposes
DIR_ABS_PATH = os.path.dirname(__file__)
EXAMPLE_PATH = os.path.join(DIR_ABS_PATH, 'examplejson.json')
with open(EXAMPLE_PATH) as json_file:
    data = json.load(json_file)
parse_json = data

timezone = pytz.timezone(parse_json["timezone"])

#please uncomment this when ready
#print("Weather for " + location_data[int(0)]['name'].upper() + ".")


print("Current observations:")
print("Time is " + timezone.localize(datetime.datetime.fromtimestamp(parse_json["current"]["dt"])).strftime("%d/%m/%Y - %H:%M %p"))
#list alerts
if "alerts" in parse_json:
    alertslist = []
    for i in range(len(parse_json["alerts"])):
        alertslist.append(parse_json["alerts"][int(i)]["event"])
    alerts = ', '.join([str(x) for x in alertslist])
    print(alerts + " are in effect for this area.")

#cloud cover
def cloud_cover(percent):
    if percent >= 85:
        return "cloudy"
    elif percent >= 50:
        return "mostly cloudy"
    elif percent >= 25:
        return "partly cloudy"
    elif percent >= 10:
       return "clear"


#degrees to direction
def degrees_to_direction(degrees):
    if degrees > 326.25:
        return "NNW"
    elif degrees > 303.75:
        return "NW"
    elif degrees > 281.25:
        return "WNW"
    elif degrees > 258.75:
        return "W"
    elif degrees > 236.25:
        return "WSW"
    elif degrees > 213.75:
        return "SW"
    elif degrees > 191.25:
        return "SSW"
    elif degrees > 168.75:
        return "S"
    elif degrees > 146.25:
        return "SSE"
    elif degrees > 123.75:
        return "SE"
    elif degrees > 101.25:
        return "ESE"
    elif degrees > 78.75:
        return "E"
    elif degrees > 56.25:
        return "ENE"
    elif degrees > 33.75:
        return "NE"
    elif degrees > 11.25:
        return "NNE"
    else:
        return "N"

#check if gusts
if "wind_gust" in parse_json["current"]:
    gusts = " m/s, gusting to " + str(parse_json["current"]["wind_gust"]) + " m/s"
else:
    gusts = " m/s"

print("Currently the temperature is " + str(parse_json["current"]["temp"]) + "C - feeling like " + str(parse_json["current"]["feels_like"]) + "C - with " + str(parse_json["current"]["weather"][0]["description"]) + " under " + cloud_cover(parse_json["current"]["clouds"]) + " (" + str(parse_json["current"]["clouds"]) +  "%) skies.")
print("The next 2 hours will have the current " + str(parse_json["hourly"][int(0)]["weather"][int(0)]["description"]) + " changing to " + str(parse_json["hourly"][int(1)]["weather"][int(0)]["description"]) + " in an hour, finally changing to " + str(parse_json["hourly"][int(2)]["weather"][int(0)]["description"]) + " in 2 hours.")
if parse_json["current"]["uvi"] >= 6:
    if parse_json["current"]["uvi"] >= 11:
        print("The UV index is " + str(parse_json["current"]["uvi"]) + " - extremely high. Avoid the sun between 10am and 4pm. Find shade, cover up, wear a hat and sunglasses, and put on sunscreen.")
    elif parse_json["current"]["uvi"] >= 8:
        print("The UV index is " + str(parse_json["current"]["uvi"]) + " - very high. Avoid the sun between 10am and 4pm. If you cannot, cover up, wear a hat, put on sunglasses, and wear sunglasses.")
    elif parse_json["current"]["uvi"] >= 6:
        print("The UV index is " + str(parse_json["current"]["uvi"]) + " - high. Cover up, wear a hat and use sunscreen.")
print("Winds " +  degrees_to_direction(parse_json["current"]["wind_deg"]) + " at " + str(parse_json["current"]["wind_speed"]) + gusts + ".")
print("Humidity is " + str(parse_json["current"]["humidity"]) + "%.")
if "rain" in parse_json["current"]:
    print(str(parse_json["current"]["rain"]["1h"]) + " mm of rain has fallen in the past hour.")
if "snow" in parse_json["current"]:
    print(str(parse_json["current"]["snow"]["1h"]) + " mm of snow has fallen in the past hour.")

print("\nTomorrows forecast:")
print("High: " + str(parse_json["daily"][int(1)]["temp"]["max"]) + "C - Low: " + str(parse_json["daily"][int(1)]["temp"]["min"]) + "C with " + str(parse_json["daily"][int(1)]["weather"][int(0)]["description"]) + ".")
print("Morning: " + str(parse_json["daily"][int(1)]["temp"]["morn"]) + "C. Afternoon: " + str(parse_json["daily"][int(1)]["temp"]["day"]) +  "C. Evening: " + str(parse_json["daily"][int(1)]["temp"]["eve"]) + "C. Night: " + str(parse_json["daily"][int(1)]["temp"]["night"]) + "C.")
print("Winds " +  degrees_to_direction(parse_json["daily"][int(1)]["wind_deg"]) + " at " + str(parse_json["daily"][int(1)]["wind_speed"]) + " m/s.")
print("Humidity will be " + str(parse_json["daily"][int(1)]["humidity"]) + "%.")
if "pop" in parse_json["daily"][int(1)]:
    print(str(parse_json["daily"][int(1)]["pop"]) + "% chance of precipation.")
if "rain" in parse_json["daily"][int(1)]:
    print(str(parse_json["daily"][int(1)]["rain"]) + " mm of rain expected.")
if "snow" in parse_json["daily"][int(1)]:
    print(str(parse_json["daily"][int(1)]["snow"]) + " mm of snow expected.")
#epoch to datetime timezone
print("Sunrise at " + datetime.datetime.fromtimestamp(parse_json["daily"][int(1)]["sunrise"], tz=timezone).strftime('%H:%M') + " and sunset at " + datetime.datetime.fromtimestamp(parse_json["daily"][int(1)]["sunset"], tz=timezone).strftime('%H:%M') + ".")
#5 day forecast
print("\n7 day forecast:")
for i in range(1, 8):
    epochtime = parse_json["daily"][int(i)]["dt"]
    #epoch to datetime with timezone
    date = datetime.datetime.fromtimestamp(epochtime, tz=timezone).strftime('%d/%m/%Y')
    print(date)
    print("High: " + str(round(parse_json["daily"][int(i)]["temp"]["max"])) + "C - Low: " + str(round(parse_json["daily"][int(i)]["temp"]["min"])) + "C with " + str(parse_json["daily"][int(i)]["weather"][int(0)]["description"]) + ".")
    print("Winds " +  degrees_to_direction(parse_json["daily"][int(i)]["wind_deg"]) + " at " + str(parse_json["daily"][int(i)]["wind_speed"]) + " m/s.")
    print("Sunrise at " + datetime.datetime.fromtimestamp(parse_json["daily"][int(i)]["sunrise"], tz=timezone).strftime('%H:%M') + " and sunset at " + datetime.datetime.fromtimestamp(parse_json["daily"][int(i)]["sunset"], tz=timezone).strftime('%H:%M') + ".")
    if "pop" in parse_json["daily"][int(i)]:
        print(str(parse_json["daily"][int(i)]["pop"]) + "% chance of precipation.")
    print("\n")