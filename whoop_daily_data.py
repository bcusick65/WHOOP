#!/usr/bin/env python3

from datetime import datetime
import pytz
import requests as requests
from whoop_config import *
import json
import os



# Get access creds
#Create this as a 'def' (function) right here. Call this function inside this file
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

    # Set user/token
    #userid = r.json()['user']['id']
    #token = r.json()['access_token']
    return r


# Write token to file
# This will create a temp file within the project
# dir that contains your repeatable acccess creds
response = get_oauth_creds()
print(os.getcwd())
with open('file_token.txt', 'w') as file:
    file = file.write(json.dumps(response.json()))


# Set up request
url = 'https://api-7.whoop.com/users/{}/cycles'.format(userid)

# Set today as the time range
x = datetime.now()
start = '2021-03-24T00:00:00.000Z'
end = '2021-03-31T00:00:00.000Z'
#start = x.strftime("%Y-%m-%dT00:00:00.000Z")
#end = x.strftime("%Y-%m-%dT%H:%M:%S.000Z")

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
	print("No good at auth, see ya.")
	exit()
else:
	print("Whoop!")

# Parse data
values = r.json()


# Fix timezone junk
def time_parse(time_string, offset_string):
	# Switch sign on offset
	offset_string = offset_string.replace(
		'-', '+') if offset_string.count('-') else offset_string.replace('+', '-')
	# Remove tz from time and add offset, get to 19 characters
	time_string = time_string[:-(len(time_string) - 19)] + offset_string
	# Parse and format
	oldformat = '%Y-%m-%dT%H:%M:%S%z'
	newformat = '%Y-%m-%d %H:%M:%S'
	return datetime.strptime(time_string, oldformat).astimezone(pytz.utc).strftime(newformat)


# Make data object
#data_summary = []
# Iterate through data
#for d in values:

	# Make default record object
#	record = {
#		'timestamp_measurement': None,
#		'HR': None,
#		'AVNN': None,
#		'SDNN': None,
#		'rMSSD': None,
#		'pNN50': None,
#		'LF': None,
#		'HF': None,
#		'HRV4T_Recovery_Points': None
#	}

	# Recovery
#	if (d['recovery'] and
#			'timestamp' in d['recovery'] and
#			'heartRateVariabilityRmssd' in d['recovery'] and
#			isinstance(d['recovery']['heartRateVariabilityRmssd'], (int, float)) and
#			d['sleep'] and
#			d['sleep']['sleeps'] and
#			d['sleep']['sleeps'][0]['timezoneOffset']):
#
#		# This is the timestamp when Whoop processed sleep -
#		# not the time of measurement
#		record['timestamp_measurement'] = time_parse(
#			d['recovery']['timestamp'],
#			d['sleep']['sleeps'][0]['timezoneOffset'])
#		record['rMSSD'] = d['recovery']['heartRateVariabilityRmssd'] * 1000.0
#
#		if ('restingHeartRate' in d['recovery'] and
#				isinstance(d['recovery']['restingHeartRate'], (int, float))):
#			record['HR'] = d['recovery']['restingHeartRate']
#
#		# Recovery score
#		if ('score' in d['recovery'] and
#				isinstance(d['recovery']['score'], (int, float))):
#			record['HRV4T_Recovery_Points'] = d['recovery']['score'] / 10.0
#
#		# Append record to data dictionary
#		data_summary.append(record)

print("Values: ", values)

splunk_payload = ""

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


# Cheap way to fix single quotes
splunk_payload = splunk_payload.replace("'",'"')
splunk_payload = splunk_payload.replace('None','"None"')
splunk_payload = splunk_payload.replace('False','"False"')
splunk_payload = splunk_payload.replace('True','"True"')
#splunk_payload = splunk_payload.replace(']}]}}',']}]}]}}')

print("Batched events: \n", splunk_payload)


# Set HEC header
auth_header = {'Authorization': 'Splunk ' + hec_hr_token}

# Send HEC event to Splunk
r = requests.post(url=hec_endpoint, data=splunk_payload, headers=auth_header)
print(r)
print("Splunk HEC post status: \n", r.text)


