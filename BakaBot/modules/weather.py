""" Weather Module"""

import asyncio
from datetime import datetime
import json
import os

import discord
from discord.ext import commands

import requests

class Current:
    """ Fetch the current weather from Dark Sky API based on Lat/Lng values """

    def __init__(self, lat, lng):
        # DELET THIS. Make it a dictionary instead. A lot better.
        with open('./json/setup.json') as data_file:
            settings = json.load(data_file)
        self.dsapikey = settings["DarkSkyAPIKey"]
        url = "https://api.darksky.net/forecast/" + self.dsapikey + \
            "/" + str(lat) + "," + str(lng) + "?exclude=minutely,hourly,daily,alerts,flags"
        req = requests.get(url)
        if req.status_code != 200:
            return
        a = json.loads(req.text)
        self.latitude = a["latitude"]
        self.longitude = a["longitude"]
        currently = a["currently"]
        self.summary = currently["summary"].lower()
        self.icon = currently["icon"]
        self.rainprobability = currently["precipProbability"] * 100
        if self.rainprobability != 0:
            self.preciptype = currently["precipType"]
        else:
            self.preciptype = 'rain'
        self.temp = currently["temperature"]
        self.feelslike = currently["apparentTemperature"]
        self.humidity = currently["humidity"] * 100
        self.time = datetime.fromtimestamp(currently["time"])

    def gettime(self):
        return (str(self.time.month) + "/" + str(self.time.day) + "/" +
                str(self.time.year) + " @ " + str(self.time.hour) + ":" +
                str(self.time.minute))

    def discordicon(self):
        """ Return the correlating Discord Emote"""
        if self.icon == "clear-day":
            return ":sunny:"
        elif self.icon == "clear-night":
            return ":crescent_moon:"
        elif self.icon == "rain":
            return ":cloud_rain:"
        elif self.icon == "snow":
            return ":cloud_snow:"
        elif self.icon == "sleet":
            return ":snowflake:"
        elif self.icon == "wind":
            return ":dash:"
        elif self.icon == "fog" or self.icon == "cloudy":
            return ":cloud:"
        elif self.icon == "partly-cloudy-day" or self.icon == "partly-cloudy-night":
            return ":partly_sunny:"
        else:
            print("No Icon Found For: " + self.icon)

    def msg(self, place):
        """ Return the message"""
        return ("Searched: [" + str(self.latitude) + ", " +
                str(self.longitude) + "]\t" + self.gettime() + "\n" +
                self.discordicon() + " It is " + self.summary +
                " in " + place + ". It is currently " + str(self.temp) +
                " F, but it feels like " + str(self.feelslike) +
                " F. There is a " + str(self.rainprobability) +
                "% chance of " + self.preciptype +
                ". Humidity: " + str(self.humidity)[:4] + "%\n" +

                "*Provided To You By Google's GeoCode and DarkSkyAPI*")


class Weather:
    def __init__(self, bot):
        self.bot = bot
        with open('./json/setup.json') as data_file:
            settings = json.load(data_file)
        self.geocodeapi = settings["GoogleAPIKey"]

    @commands.command(pass_context=True)
    async def weather(self, ctx, *, search: str):
        """ Grab the weather using GoogleGeoCodeAPI and DarkSkyAPI"""
        url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + \
            search.replace(" ", "+") + "&key=" + self.geocodeapi
        req = requests.get(url)
        if req.status_code != 200:
            await self.bot.say("Google GeoCode is currently down")
            return

        location = json.loads(req.text)
        if location["status"] == "OK":
            lat = location["results"][0]["geometry"]["location"]["lat"]
            lng = location["results"][0]["geometry"]["location"]["lng"]
            place = location["results"][0]["address_components"][0]["long_name"]
            current = Current(lat, lng)
            await self.bot.say(current.msg(place))
            self.bot.cogs['WordDB'].cmdcount('weather')
            return

        else:
            print("Status Error: " + location["status"])
            return

def setup(bot):
    bot.add_cog(Weather(bot))
