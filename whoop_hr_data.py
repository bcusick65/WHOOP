#!/usr/bin/env python3

# Author: Brian Cusick
# Pull heart rate data at a 60 second interval (instead of 6 or 600 second options)
# Pulls the last 5 minutes
# Should run every 5 minutes
# Assumes US/Eastern timezone (yes still needs work)

from datetime import datetime, timedelta
import requests as requests
from whoop_config import *


# Get access creds
r = requests.post('https://api-7.whoop.com/oauth/token', json={
     "username": username,
     "password": password,
     "grant_type": "password",
     "issueRefresh": False
  })


if r.status_code != 200:
    print("Invalid Creds")
    exit()
else:
    print("Credentials Accepted")

# Set user/token
userid = r.json()['user']['id']
token = r.json()['access_token']


# Set up request to HR endpoint
url = 'https://api-7.whoop.com/users/{}/metrics/heart_rate'.format(userid)

# Set five minute time range to pull data for
time_now = datetime.now()
five_minutes = timedelta(minutes=5)
five_minutes_ago = time_now - five_minutes
five_minutes_ago = five_minutes_ago.strftime("%Y-%m-%dT%H:%M:%S.000Z")
time_now = time_now.strftime("%Y-%m-%dT%H:%M:%S.000Z")

params = {
    'sort': 't',
    'step': '60',
    'start': five_minutes_ago,
    'end': time_now
}

headers = {
    'Authorization': 'bearer {}'.format(token)
}

r = requests.get(url, params=params, headers=headers)

# Check if creds are re-accepted
if r.status_code != 200:
    print("Bad request, see ya.")
    exit()
else:
    print("Whoop!")

# Put payload in object
data_raw = r.json()
values = r.json()['values']

# Begin formatting for Splunk HEC stacked events
# Also fix Splunk timezone issue without using /raw endpoint
splunk_payload = ""

for x in values:
	event_time = x['time']
	four_hours = 14400000
	zulu_time = event_time + four_hours
	splunk_payload = splunk_payload + '{"time": ' + str(zulu_time) + ', "host": "api-7.whoop.com", "index": "' + hec_index + '","source": "hr_data", "sourcetype": "' + hec_hr_sourcetype + '", "event": ' + str(x) + '}'

# Fix single quotes
splunk_payload = splunk_payload.replace("'",'"')
print("Batched events: \n", splunk_payload)

# Send HEC event to Splunk
r = requests.post('http://zeus.cusickbrian.com:8088/services/collector', data=splunk_payload, headers=auth_header)
print("Splunk HEC post status: \n", r.text)


