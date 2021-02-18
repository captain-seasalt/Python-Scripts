# Imports
import time
import csv
import datetime
import pprint
import datadog_api_client.v1
from dateutil.parser import parse as dateutil_parser
from datadog_api_client.v1 import ApiClient, ApiException, Configuration
from datadog_api_client.v1.api import logs_api
from datadog_api_client.v1.models import *
from pprint import pprint
# Defining the host is optional and defaults to https://api.datadoghq.com
# See configuration.py for a list of all supported configuration parameters.
configuration = datadog_api_client.v1.Configuration(
    host="https://api.datadoghq.com"
)
# Configure API key authorization: apiKeyAuth, replace ******** with apikey
configuration.api_key['apiKeyAuth'] = '********'
# Configure API key authorization: appKeyAuth, replace ******** with appkey
configuration.api_key['appKeyAuth'] = '********'
# Vars here
has_additional_logs = True
log_start_at = ''
def create_api_client():
    print(
        'This is where you really should create a single API client for re-use if possible')
def write_log(host, message, service, tags, timestamp):
    with open('data-dog-logs.csv', mode='a') as log_file:
        log_it = csv.writer(log_file, delimiter=',', quotechar='"',
                            quoting=csv.QUOTE_MINIMAL)
        log_it.writerow([host, message, service, tags, timestamp])
def loop_data_dog():
    # Adding headers to the file (only do this once)
    write_log(
        'host',
        'message',
        'service',
        'tags',
        'timestamp'
    )
    # Reference global vars
    global has_additional_logs, log_start_at
    # Placeholder for doing a more proper API client to reference
    create_api_client()
    # If we still have more logs to process, keep looping.
    while has_additional_logs:
        # can remove this, isn't entirely necessary.
        time.sleep(1)
        # Enter a context with an instance of the API client
        with ApiClient(configuration) as api_client:
            # Create an instance of the API class
            api_instance = logs_api.LogsApi(api_client)
            request_dict = {
                # index name for historical view is generated
                # when rehydrating logs, it will be the query name
                'index': "january-15-2021",
                'limit': 1000,
                'query': "*",
                'sort': LogsSort("desc"),
                # Right here... this value is important to keep track
                # of with the iteration so we know where to jump back
                # in at and where to stop.
                #'start_at': log_start_at,
                'time': LogsListRequestTime(
                    _from=dateutil_parser('2021-01-15T07:00:00Z'),
                    timezone="timezone_example",
                    to=dateutil_parser('2021-01-15T21:00:00Z'),
                ),
            }
            if log_start_at != '':
                request_dict['start_at'] = log_start_at
            # Define the query constraints for the logs
            body = LogsListRequest(**request_dict)
            try:
                # Get a list of logs
                api_response = api_instance.list_logs(body)
                # This is the real special sauce here... keep looping
                # until you don't find any further log IDs.
                if 'next_log_id' in api_response:
                    has_additional_logs = True
                    log_start_at = api_response['next_log_id']
                else:
                    has_additional_logs = False
                # Show the log details.
                logs = api_response['logs']
                pprint(api_response)
                for log in logs:
                    write_log(
                        log['content']['host'],
                        log['content']['message'],
                        log['content']['service'],
                        log['content']['tags'],
                        log['content']['timestamp']
                    )
            except ApiException as e:
                print("Exception when calling LogsApi->list_logs: %s\n" % e)
    # Here we have completed all the looping
    # and can do any cleanup work.
    print('Done, any cleanup can go here.')
# This automatically enters the loop
# if you haven't passed any instructions to the .py file
if __name__ == '__main__':
    loop_data_dog()
