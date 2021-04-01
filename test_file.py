from whoop_config import *
import requests
from datetime import datetime


# Set HEC header
auth_header = {'Authorization': 'Splunk ' + hec_hr_token}

# Set test data
values = [{'days': ['2021-04-01'], 'during': {'bounds': '[)', 'lower': '2021-04-01T04:09:39.807+00:00', 'upper': None}, 'id': 96247039, 'lastUpdatedAt': '2021-04-01T12:03:52.701315+00:00', 'predictedEnd': '2021-04-02T03:30:14.837+00:00', 'recovery': {'blackoutUntil': None, 'calibrating': False, 'heartRateVariabilityRmssd': 0.113683, 'id': 100131809, 'responded': False, 'restingHeartRate': 48, 'score': 84, 'state': 'complete', 'surveyResponseId': None, 'timestamp': '2021-04-01T11:18:23.349+00:00'}, 'sleep': {'id': 211355622, 'naps': [], 'needBreakdown': {'baseline': 27459936, 'debt': 1235697, 'naps': 0, 'strain': 111685, 'total': 28807318}, 'qualityDuration': 23827719, 'score': 83, 'sleeps': [{'cyclesCount': 3, 'disturbanceCount': 15, 'during': {'bounds': '[)', 'lower': '2021-04-01T04:09:39.807+00:00', 'upper': '2021-04-01T11:18:23.349+00:00'}, 'id': 211355622, 'inBedDuration': 25722580, 'isNap': False, 'latencyDuration': 0, 'lightSleepDuration': 13827860, 'noDataDuration': 0, 'qualityDuration': 23827719, 'remSleepDuration': 4593254, 'respiratoryRate': 13.7695, 'responded': False, 'score': 83, 'sleepConsistency': 85, 'sleepEfficiency': 0.926335, 'slowWaveSleepDuration': 5406605, 'source': 'auto', 'state': 'complete', 'surveyResponseId': None, 'timezoneOffset': '-0400', 'wakeDuration': 1923162}], 'state': 'complete'}, 'strain': {'averageHeartRate': 51, 'kilojoules': 4676.0596, 'maxHeartRate': 104, 'rawScore': 6.09453e-06, 'score': 0.8481839592059681, 'state': None, 'workouts': []}}]


splunk_payload = ""

# Stack events for Splunk HEC payload and adjust Splunk timezone issue
for x in values:
	event_time = x['during']['lower']
	event_time = datetime.strptime(event_time, "%Y-%m-%dT%H:%M:%S.%f%z")
	event_time = str(event_time.timestamp() * 1000)
	if len(x['strain']['workouts']) == 0:
		print("Empty list")
		splunk_payload = splunk_payload + '{"time": "' + str(
			event_time) + '", "host": "api-7.whoop.com", "index": "' + hec_index + '","source": "cycles_data", "sourcetype": "' + hec_cycles_sourcetype + '", "event": ' + str(
			x) + '}'
	else:
		print("Not empty list")
		splunk_payload = splunk_payload + '{"time": "' + str(event_time) + '", "host": "api-7.whoop.com", "index": "' + hec_index + '","source": "cycles_data", "sourcetype": "' + hec_cycles_sourcetype + '", "event": ' + str(x) + '}]}'


# Cheap way to fix single quotes
splunk_payload = splunk_payload.replace("'",'"')
splunk_payload = splunk_payload.replace('None','"None"')
splunk_payload = splunk_payload.replace('False','"False"')

print("Batched events: \n", splunk_payload)

# Send HEC event to Splunk
#r = requests.post(url=hec_endpoint, data=splunk_payload, headers=auth_header)
#print(r)
#print("Splunk HEC post status: \n", r.text)

