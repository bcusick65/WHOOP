# Whoop auth variables
username = "yourwhoopemail@domain.com"
password = "your_password"
save_directory = "~/"

# Global Splunk variables
endpoint = 'http://your.splunkHECendpoint.com:8088'
hec_endpoint = endpoint + '/services/collector'
hec_raw_endpoint = endpoint + '/services/collector/raw'			# Leveraging raw endpoint for linebreaking
hec_index = 'whoop_test'										# Insert Splunk index for whoop data here

# Splunk HEC variables - daily cycles
hec_token = 'your_daily_data_hec_token'			                # Insert Splunk HEC token here
hec_cycles_sourcetype = 'whoop:daily'							# May create this at API pull time later
metrics_endpoint = endpoint + '/services/collector'
channel_header = 'random_string'                                # Additional request channel for raw endpoint

# Splunk HEC variables - heart rate data
hec_hr_token = 'your_heartrate_hec_token'                       # Insert Splunk HEC token here
hec_hr_sourcetype = 'whoop:hr:data'
