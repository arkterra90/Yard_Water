from flask import Flask, request
from geocodio import GeocodioClient
from functools import wraps
from datetime import date, timedelta, datetime
import requests
import math


from flask import redirect, render_template

# Function returns API call to look up coordinates for users given zipcode
def lookup(zipcode):
    """API zipcode lookup function for lat long"""
    try:
        client = GeocodioClient("bc568438569fdfd8a3466dc6c9418986f51c183")
        location = client.geocode(zipcode)
    except request.RequestException:
        return None

    data = location.coords

    return data

# Function returns API call to look up daily total rain falls for previous 14 days
# and returns a sum of those rainfalls.
def rain(location):
    """api call to get weather"""

    #data for weather api call
    date1 = date.today().isoformat()
    date2 = (date.today() - timedelta(days=14)).isoformat()

    # Rounds geocode to use for Meteo API call requirements
    lat = round(location[0], 2)
    lng = round(location[1], 2)

    # API call for weather/rain fall data
    try:
        url = f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lng}&start_date={date2}&end_date={date1}&daily=precipitation_sum&timezone=America%2FChicago&precipitation_unit=inch"
        response = requests.get(url)
        response.raise_for_status()

    except requests.RequestException:
        return None

    # Takes json file and returns a sum of rain totals
    rain = response.json()

    while(None in rain['daily']['precipitation_sum']):
        rain['daily']['precipitation_sum'].remove(None)

    rain_sum = math.fsum(rain['daily']['precipitation_sum'])

    return rain_sum