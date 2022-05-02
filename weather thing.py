import requests
import json
import datetime

#response_API = requests.get("https://api.openweathermap.org/data/2.5/onecall?lat=31.063&lon=-102.388&units=metric&appid=" + apikey)
#data = response_API.text
with open('E:\projects\stuff and things\jsontest.json') as json_file:
    data = json.load(json_file)
parse_json = data

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
    gusts = "m/s, gusting to " + str(parse_json["current"]["wind_gust"]) + " m/s"
else:
    gusts = " m/s"

print("Currently the temperature is " + str(parse_json["current"]["temp"]) + " degrees Celsius - feeling like " + str(parse_json["current"]["feels_like"]) + "C - with " + str(parse_json["current"]["weather"][0]["description"]) + " under " + clouds + " (" + str(parse_json["current"]["clouds"]) +  "%) skies.")
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

if parse_json["daily"][int(1)]["clouds"] >= 85:
    clouds = "cloudy"
elif parse_json["daily"][int(1)]["clouds"] >= 50:
    clouds= "mostly cloudy"
elif parse_json["daily"][int(1)]["clouds"] >= 25:
    clouds= "partly cloudy"
elif parse_json["daily"][int(1)]["clouds"] >= 10:
    clouds = "clear"

print("\nTomorrows forecast:")
print("High: " + str(parse_json["daily"][int(1)]["temp"]["max"]) + "C - Low: " + str(parse_json["daily"][int(1)]["temp"]["min"]) + "C with " + str(parse_json["daily"][int(1)]["weather"][int(0)]["description"]) + " under " + clouds + " (" + str(parse_json["daily"][int(1)]["clouds"]) + "%) skies.")
print("Winds " +  wind_direction + " at " + str(parse_json["daily"][int(1)]["wind_speed"]) + gusts + ".")