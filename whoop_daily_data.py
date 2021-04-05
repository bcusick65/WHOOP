#!/usr/bin/env python3

# Author: Brian Cusick
# Pull daily cycle data at 24 hour interval
# Should run once every 24 hours, pulls YESTERDAY's data
# because recovery data isn't optimized until after sleep
# Assumes US/Eastern timezone (yes still needs work)
# Will eventually leverage a 'rising column'



from datetime import datetime, timedelta
import requests as requests
from whoop_config import *
import json

# Set variables
auth_header = {'Authorization': 'Splunk ' + hec_hr_token}
splunk_payload = ""
response_json = ""

# Get access creds
def get_oauth_creds():
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

    return r


# Write token to file
# This will create a temp file within the project
# dir that contains your repeatable access creds
response = get_oauth_creds()
with open('file_token.txt', 'w') as file:
    file = file.write(json.dumps(response.json()))

# Pull stored access creds from disk
with open('file_token.txt', 'r') as file_token:
    response_json = file_token.read()

dict_response_json = json.loads(response_json)
token = dict_response_json['access_token']
userid = dict_response_json['user']['id']


# Set up request
url = 'https://api-7.whoop.com/users/{}/cycles'.format(userid)

# Set yesterday as the time range
time_now = datetime.now()
one_day = timedelta(hours=24)
start = time_now - one_day
end = time_now - one_day
start = start.strftime("%Y-%m-%dT00:00:00.000Z")
end = end.strftime("%Y-%m-%dT23:59:59.000Z")

params = {
	'start': start,
	'end': end
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
	print("Whoop!")
	print(r)

# Parse data
values = r.json()

# Stack events for Splunk HEC payload and adjust Splunk timezone issue
for x in values:
	event_time = x['recovery']['timestamp']
	print(event_time)
	event_time = datetime.strptime(event_time, "%Y-%m-%dT%H:%M:%S.%f%z")
	event_time = str(event_time.timestamp() * 1000)
	event_time = str(round(float(event_time)))
	print(event_time)
	splunk_payload = splunk_payload + '{"time": "' + str(
		event_time) + '", "host": "api-7.whoop.com", "index": "' + hec_index + '","source": "cycles_data", "sourcetype": "' + hec_cycles_sourcetype + '", "event": ' + json.dumps(
		x) + '}'


# Send HEC event to Splunk
r = requests.post(url=hec_endpoint, data=splunk_payload, headers=auth_header)
print(r)
print("Splunk HEC post status: \n", r.text)


