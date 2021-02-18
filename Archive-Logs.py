import os
from dateutil.parser import parse as dateutil_parser
from datadog_api_client.v2 import ApiClient, ApiException, Configuration
from datadog_api_client.v2.api import logs_archives_api
from datadog_api_client.v2.models import *
from pprint import pprint
# Defining the host is optional and defaults to https://api.datadoghq.com
# See configuration.py for a list of all supported configuration parameters.
configuration = Configuration(
    host="https://api.datadoghq.com"
)

# Configure API key authorization: apiKeyAuth
configuration.api_key['apiKeyAuth'] = '**************************'

# Configure API key authorization: appKeyAuth
configuration.api_key['appKeyAuth'] = '**************************'

# Enter a context with an instance of the API client
with ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = logs_archives_api.LogsArchivesApi(api_client)
    archive_id = "paxez2aSQs6IF7x8MjTF1A"  # str | The ID of the archive.
    body = LogsListRequest(
        index="*",
        limit=1000,
        query="*",
        sort=LogsSort("desc"),
        # Hash identifier of the first log to return in the list, available in a log id attribute. This would be the next log id to start with, enable by removing hashtag before start_at and replace *********** with the next log id. For example: start_at="AQAAAXcHof6osxEV8gAAAABBWGNIb2hmNkFBQ25SSXlpc1RLeTl3QU8"
        #start_at="***********",
        time=LogsListRequestTime(
            _from=dateutil_parser('2021-01-14T20:00:00Z'),
            timezone="timezone_example",
            to=dateutil_parser('2021-01-15T20:00:00Z'),
        ),
    )  # LogsListRequest | Logs filter

    # example passing only required values which don't have defaults set
    try:
        # Get an archive
        api_response = api_instance.get_logs_archive(archive_id), api_instance.list_logs(body)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling LogsArchivesApi->get_logs_archive: %s\n" % e)