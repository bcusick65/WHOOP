from whoop_config import *
import requests
from datetime import datetime


# Set HEC header
auth_header = {'Authorization': 'Splunk ' + hec_hr_token}

# Set test data
# Test without workout data
#values = [{'days': ['2021-04-01'], 'during': {'bounds': '[)', 'lower': '2021-04-01T04:09:39.807+00:00', 'upper': None}, 'id': 96247039, 'lastUpdatedAt': '2021-04-01T12:03:52.701315+00:00', 'predictedEnd': '2021-04-02T03:30:14.837+00:00', 'recovery': {'blackoutUntil': None, 'calibrating': False, 'heartRateVariabilityRmssd': 0.113683, 'id': 100131809, 'responded': False, 'restingHeartRate': 48, 'score': 84, 'state': 'complete', 'surveyResponseId': None, 'timestamp': '2021-04-01T11:18:23.349+00:00'}, 'sleep': {'id': 211355622, 'naps': [], 'needBreakdown': {'baseline': 27459936, 'debt': 1235697, 'naps': 0, 'strain': 111685, 'total': 28807318}, 'qualityDuration': 23827719, 'score': 83, 'sleeps': [{'cyclesCount': 3, 'disturbanceCount': 15, 'during': {'bounds': '[)', 'lower': '2021-04-01T04:09:39.807+00:00', 'upper': '2021-04-01T11:18:23.349+00:00'}, 'id': 211355622, 'inBedDuration': 25722580, 'isNap': False, 'latencyDuration': 0, 'lightSleepDuration': 13827860, 'noDataDuration': 0, 'qualityDuration': 23827719, 'remSleepDuration': 4593254, 'respiratoryRate': 13.7695, 'responded': False, 'score': 83, 'sleepConsistency': 85, 'sleepEfficiency': 0.926335, 'slowWaveSleepDuration': 5406605, 'source': 'auto', 'state': 'complete', 'surveyResponseId': None, 'timezoneOffset': '-0400', 'wakeDuration': 1923162}], 'state': 'complete'}, 'strain': {'averageHeartRate': 51, 'kilojoules': 4676.0596, 'maxHeartRate': 104, 'rawScore': 6.09453e-06, 'score': 0.8481839592059681, 'state': None, 'workouts': []}}]
# Test with workout data
values = [{'days': ['2021-03-29'], 'during': {'bounds': '[)', 'lower': '2021-03-29T02:17:19.717+00:00', 'upper': '2021-03-30T03:51:55.385+00:00'}, 'id': 95390882, 'lastUpdatedAt': '2021-03-30T11:47:31.912857+00:00', 'predictedEnd': '2021-03-30T02:17:19.717+00:00', 'recovery': {'blackoutUntil': None, 'calibrating': False, 'heartRateVariabilityRmssd': 0.107996, 'id': 99248344, 'responded': False, 'restingHeartRate': 50, 'score': 95, 'state': 'complete', 'surveyResponseId': None, 'timestamp': '2021-03-29T11:40:16.546+00:00'}, 'sleep': {'id': 209715843, 'naps': [], 'needBreakdown': {'baseline': 27460495, 'debt': 2746049, 'naps': 0, 'strain': 181427, 'total': 30387972}, 'qualityDuration': 31212351, 'score': 100, 'sleeps': [{'cyclesCount': 6, 'disturbanceCount': 13, 'during': {'bounds': '[)', 'lower': '2021-03-29T02:17:19.717+00:00', 'upper': '2021-03-29T11:40:16.546+00:00'}, 'id': 209715843, 'inBedDuration': 33579322, 'isNap': False, 'latencyDuration': 0, 'lightSleepDuration': 15233138, 'noDataDuration': 0, 'qualityDuration': 31212351, 'remSleepDuration': 8137348, 'respiratoryRate': 13.5352, 'responded': False, 'score': 100, 'sleepConsistency': 74, 'sleepEfficiency': 0.929511, 'slowWaveSleepDuration': 7841865, 'source': 'auto+user', 'state': 'complete', 'surveyResponseId': None, 'timezoneOffset': '-0400', 'wakeDuration': 2403484}], 'state': 'complete'}, 'strain': {'averageHeartRate': 68, 'kilojoules': 13117.9, 'maxHeartRate': 169, 'rawScore': 0.00558007624740515, 'score': 12.0653694759502, 'state': 'complete', 'workouts': [{'altitudeChange': 1.37012, 'altitudeGain': 144.851, 'averageHeartRate': 124, 'cumulativeWorkoutStrain': 8.4677, 'distance': 4015.28295521473, 'during': {'bounds': '[)', 'lower': '2021-03-29T17:41:56.841+00:00', 'upper': '2021-03-29T18:26:46.893+00:00'}, 'gpsEnabled': True, 'id': 209921265, 'kilojoules': 1565.48, 'maxHeartRate': 169, 'rawScore': 0.00260023247848361, 'responded': True, 'score': 8.46770783484894, 'source': 'user', 'sportId': 1, 'state': 'complete', 'surveyResponseId': 60647097, 'timezoneOffset': '-0400', 'zones': [57716, 240328, 1539048, 793073, 59600, 0]}]}}]


splunk_payload = ""

# Stack events for Splunk HEC payload and adjust Splunk timezone issue
for x in values:
	event_time = x['during']['lower']
	event_time = datetime.strptime(event_time, "%Y-%m-%dT%H:%M:%S.%f%z")
	event_time = str(event_time.timestamp() * 1000)
	if len(x['strain']['workouts']) == 0:
		print("Empty list")
		print(x)
		splunk_payload = splunk_payload + '{"time": "' + str(
			event_time) + '", "host": "api-7.whoop.com", "index": "' + hec_index + '","source": "cycles_data", "sourcetype": "' + hec_cycles_sourcetype + '", "event": ' + str(
			x) + '}'
	else:
		print("Not empty list")
		print(x)
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

