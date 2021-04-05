#!/usr/bin/env python3

# Author: Brian Cusick
# Pull heart rate data at a 60 second interval (instead of 6 or 600 second options)
# Whoop uploads to Cloud every 10 minutes if your app is always open
# Therefore, pulling earliest=-20m latest=-10m, every 10 minutes
# Should run every 10 minutes
# Assumes US/Eastern timezone (yes still needs work)
# Will eventually leverage a 'rising column'

from datetime import datetime, timedelta
import requests as requests
from whoop_config import *
import json

# Set variables
response_json = ""

# Pull stored access creds from disk
with open('file_token.txt', 'r') as file_token:
    response_json = file_token.read()

dict_response_json = json.loads(response_json)
token = dict_response_json['access_token']
userid = dict_response_json['user']['id']


# Set up request to HR endpoint
url = 'https://api-7.whoop.com/users/{}/metrics/heart_rate'.format(userid)


# Set five minute time range to pull data for
# Currently hardcoded for EDT
time_now = datetime.now()
ten_minutes = timedelta(minutes=10)
twenty_minutes = timedelta(minutes=20)
four_hours = timedelta(hours=4)
twenty_minutes_ago = time_now - twenty_minutes + four_hours
ten_minutes_ago = time_now - ten_minutes + four_hours
twenty_minutes_ago = twenty_minutes_ago.strftime("%Y-%m-%dT%H:%M:%S.000Z")
ten_minutes_ago = ten_minutes_ago.strftime("%Y-%m-%dT%H:%M:%S.000Z")

params = {
    'sort': 't',
    'step': '60',
    'start': twenty_minutes_ago,
    'end': ten_minutes_ago
}

headers = {
    'Authorization': 'bearer {}'.format(token)
}

r = requests.get(url, params=params, headers=headers)

# Check if creds are re-accepted
if r.status_code != 200:
    print(r, r.text)
    exit()
else:
    print(r)

# Put payload in object
values = r.json()['values']

# Begin formatting for Splunk HEC stacked events and
# fix Splunk timezone issue without using raw HEC endpoint
splunk_payload = ""

for x in values:
    event_time = x['time']
    splunk_payload = splunk_payload + '{"time": ' + str(event_time) + ', "host": "api-7.whoop.com", "index": "' + hec_index + '","source": "hr_data", "sourcetype": "' + hec_hr_sourcetype + '", "event": ' + json.dumps(x) + '}'


# Set HEC header
auth_header = {'Authorization': 'Splunk ' + hec_hr_token}

# Send HEC event to Splunk
r = requests.post(url=hec_endpoint, data=splunk_payload, headers=auth_header)
print("Splunk HEC post status: \n", r.text)
print("\nSplunk Payload:\t", splunk_payload)