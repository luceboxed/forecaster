import requests
import json
import datetime
import pytz

#this needs a total rewrite before it can be used
#response_API = requests.get("https://api.openweathermap.org/data/2.5/onecall?lat=31.063&lon=-102.388&units=metric&appid=" + apikey)
#geocode = requests.get("http://api.openweathermap.org/geo/1.0/reverse?lat=31.063&lon=-102.388&limit=1&appid=" + "bec3a5c0a0f97477df0bd71d095ac65d")
#location_data = geocode.json()
#data = response_API.text

#for testing purposes
with open('E:/projects/forecaster/examplejson.json') as json_file:
    data = json.load(json_file)
parse_json = data

timezone = pytz.timezone(parse_json["timezone"])

#please uncomment this when ready
#print("Weather for " + location_data[int(0)]['name'].upper() + ".")


print("Current observations:")
#list alerts
if "alerts" in parse_json:
    alertslist = []
    for i in range(len(parse_json["alerts"])):
        alertslist.append(parse_json["alerts"][int(i)]["event"])
    alerts = ', '.join([str(x) for x in alertslist])
    print(alerts + " are in effect for this area.")

#cloud cover
if parse_json["current"]["clouds"] >= 85:
    clouds = "cloudy"
elif parse_json["current"]["clouds"] >= 50:
    clouds = "mostly cloudy"
elif parse_json["current"]["clouds"] >= 25:
    clouds = "partly cloudy"
elif parse_json["current"]["clouds"] >= 10:
    clouds = "clear"


#degrees to direction
if parse_json["current"]["wind_deg"] > 11.25:
    wind_direction = "NNE"
elif parse_json["current"]["wind_deg"] > 33.75:
    wind_direction = "NE"
elif parse_json["current"]["wind_deg"] > 56.25:
    wind_direction = "ENE"
elif parse_json["current"]["wind_deg"] > 78.75:
    wind_direction = "E"
elif parse_json["current"]["wind_deg"] > 101.25:
    wind_direction = "ESE"
elif parse_json["current"]["wind_deg"] > 123.75:
    wind_direction = "SE"
elif parse_json["current"]["wind_deg"] > 146.25:
    wind_direction = "SSE"
elif parse_json["current"]["wind_deg"] > 168.75:
    wind_direction = "S"
elif parse_json["current"]["wind_deg"] > 191.25:
    wind_direction = "SSW"
elif parse_json["current"]["wind_deg"] > 213.75:
    wind_direction = "SW"
elif parse_json["current"]["wind_deg"] > 236.25:
    wind_direction = "WSW"
elif parse_json["current"]["wind_deg"] > 258.75:
    wind_direction = "W"
elif parse_json["current"]["wind_deg"] > 281.25:
    wind_direction = "WNW"
elif parse_json["current"]["wind_deg"] > 303.75:
    wind_direction = "NW"
elif parse_json["current"]["wind_deg"] > 326.25:
    wind_direction = "NNW"
else:
    wind_direction = "N"

#check if gusts
if "wind_gust" in parse_json["current"]:
    gusts = " m/s, gusting to " + str(parse_json["current"]["wind_gust"]) + " m/s"
else:
    gusts = " m/s"

print("Currently the temperature is " + str(parse_json["current"]["temp"]) + "C - feeling like " + str(parse_json["current"]["feels_like"]) + "C - with " + str(parse_json["current"]["weather"][0]["description"]) + " under " + clouds + " (" + str(parse_json["current"]["clouds"]) +  "%) skies.")
if parse_json["current"]["uvi"] >= 6:
    if parse_json["current"]["uvi"] >= 11:
        print("The UV index is " + str(parse_json["current"]["uvi"]) + " - extremely high. Avoid the sun between 10am and 4pm. Find shade, cover up, wear a hat and sunglasses, and put on sunscreen.")
    elif parse_json["current"]["uvi"] >= 8:
        print("The UV index is " + str(parse_json["current"]["uvi"]) + " - very high. Avoid the sun between 10am and 4pm. If you cannot, cover up, wear a hat, put on sunglasses, and wear sunglasses.")
    elif parse_json["current"]["uvi"] >= 6:
        print("The UV index is " + str(parse_json["current"]["uvi"]) + " - high. Cover up, wear a hat and use sunscreen.")
print("Winds " +  wind_direction + " at " + str(parse_json["current"]["wind_speed"]) + gusts + ".")
if "rain" in parse_json["current"]:
    print(str(parse_json["current"]["rain"]["1h"]) + " mm of rain has fallen in the past hour.")
if "snow" in parse_json["current"]:
    print(str(parse_json["current"]["snow"]["1h"]) + " mm of snow has fallen in the past hour.")

print("\nTomorrows forecast:")
print("High: " + str(parse_json["daily"][int(1)]["temp"]["max"]) + "C - Low: " + str(parse_json["daily"][int(1)]["temp"]["min"]) + "C with " + str(parse_json["daily"][int(1)]["weather"][int(0)]["description"]) + ".")
print("Morning: " + str(parse_json["daily"][int(1)]["temp"]["morn"]) + "C. Afternoon: " + str(parse_json["daily"][int(1)]["temp"]["day"]) +  "C. Evening: " + str(parse_json["daily"][int(1)]["temp"]["eve"]) + "C. Night: " + str(parse_json["daily"][int(1)]["temp"]["night"]) + "C.")
print("Winds " +  wind_direction + " at " + str(parse_json["daily"][int(1)]["wind_speed"]) + " m/s.")
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
    print("Winds " +  wind_direction + " at " + str(parse_json["daily"][int(i)]["wind_speed"]) + " m/s.")
    if "pop" in parse_json["daily"][int(i)]:
        print(str(parse_json["daily"][int(i)]["pop"]) + "% chance of precipation.")
    print("\n")