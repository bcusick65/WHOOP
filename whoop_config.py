# Whoop auth variables
username = "redacted@gmail.com"
password = "redacted"
save_directory = "~/"

# Global Splunk variables
endpoint = 'http://zeus.cusickbrian.com:8088'
hec_endpoint = endpoint + '/services/collector'
hec_raw_endpoint = endpoint + '/services/collector/raw'			# Leveraging raw endpoint for linebreaking
hec_index = 'whoop_test'											# Insert Splunk index for whoop data here

# Splunk HEC variables - daily cycles
hec_token = '-b784-4900-b11c-f66c8e82beaf'			# Insert Splunk HEC token here
hec_cycles_sourcetype = 'whoop:daily'								# May create this at API pull time later
metrics_endpoint = endpoint + '/services/collector'
metrics_token = '-8c00-435e-a56a-60e216ee9483'
channel_header = 'GSDG-SDG44W-Y5ERGYE'               # Additional request channel for raw endpoint

# Splunk HEC variables - heart rate data
hec_hr_token = '-d568-4a60-82fd-9af0cbdfb69d'
hec_hr_sourcetype = 'whoop:hr:data'
hec_hr_channel_header = 'hr_channel_header'
