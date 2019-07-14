import sqlite3
from units import unit
import units.predefined
from stravalib import unithelper as uh

import requests
import json
import brotli

def format_data(athlete_info, race_data):
    race_distances = { "5k" : uh.meter(5000), "8k" : uh.meter(8000), "10k" : uh.meter(10000), "12k" : uh.meter(12000), "15k" : uh.meter(15000), "1/2 Mar" : uh.meter(21097.5), "Marathon" : uh.meter(42195)}

    formatted_race_data = [] 
    
    #Sorts races into chronological order
    race_data.sort(key = lambda x : x.start_date)

    for race in race_data:
        for distance in race_distances:
            #Maybe do with lambda later?
            if (abs(race_distances[distance] - race.distance) < 0.1 * race.distance):   
                race.distance = race_distances[distance]

        formatted_race_data.append(race)

                #Need to add way to deal with custom length race later
    return formatted_race_data
                

def calculate_vdot(race_data):
    headers = {
        'cookie': '__cfduid=d0b9f95405c5e2d2099437f23da0da88f1561088759; __utmc=140335664; _ga=GA1.2.1431627166.1561088760; __utmz=140335664.1561089351.2.2.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); _gid=GA1.2.1220013293.1562985965; _gat=1; __utma=140335664.1431627166.1561088760.1561089351.1562985974.3; __utmt=1; __utmb=140335664.3.9.1562985987153',
        'origin': 'https://runsmartproject.com',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9,de;q=0.8',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'referer': 'https://runsmartproject.com/calculator/',
        'authority': 'runsmartproject.com',
        'x-requested-with': 'XMLHttpRequest',
    }

    vdot_data = []

    for race in race_data:
        data = {
          'distance': race.distance,
          'unit': 'm',
          # Zfill adds leading 0 if string is less than 8 characters (needed formatting for post request)
          'time': str(race.moving_time).zfill(8),
          'pace': 'empty',
          'punit': 'mi',
          'temp': '',
          'tunit': 'F',
          'alt': '',
          'aunit': 'ft',
          'advtype': 'temperature',
          'predict': 'true'
        }

        response = requests.post('https://runsmartproject.com/vdot/app/api/find_paces', headers=headers, data=data)
        
        json_response = json.loads(brotli.decompress(response.content).decode("ascii"))
        #print (json_response['entered']['distance'])
        #print (json_response['entered']['time'])

        vdot_data.append((race.upload_id, [race, json_response]))

    formatted_vdot_data = dict(vdot_data)
    return (formatted_vdot_data)

