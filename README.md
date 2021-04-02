# WHOOP

**Description**

This repository will pull data from your WHOOP account and send to Splunk over HTTP, using the Splunk HTTP Event Collector (HEC).

<b>Requirements</b>
- Active WHOOP account (tested with Strap 3.0)
- Tested on Splunk 8.1.1

<b>Usage:</b>
1. Copy whoop_config_example.py to whoop_config.py
2. Update your creds within whoop_config.py
3. You must run whoop_daily_data.py prior to whoop_hr_data to obtain your access token
