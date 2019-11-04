import requests
import logging as log
from datetime import datetime, timedelta
import copy
import json
import argparse

log.getLogger().setLevel(log.INFO)


def format_timestamp(timestamp):
    return datetime.fromtimestamp(timestamp).strftime("%d-%m-%Y %H:%M:%S")


if __name__ == '__main__':
    """Extract an expression from Thanos in fixed {MAX_QUERY_RANGE_HOURS} batches from a starting time to now,
       storing the output in a JSON file
    """


    parser = argparse.ArgumentParser()
    parser.add_argument("query", help="The PromQL query", type=str)
    parser.add_argument("dest_file", help="The filepath where to store the JSON fetched", type=str)
    parser.add_argument("start_time", help="Start of the query range, e.g. 2019-09-01 00:00:00",
                        type=lambda d: datetime.strptime(d, '%Y-%m-%d %H:%M:%S'))

    args = parser.parse_args()

    MIN_INTERVAL_MINUTES = 5
    MAX_QUERY_RANGE_HOURS = 12
    BASE_URL = 'https://thanos-internal.tw.ee/api/v1/query_range'

    base_params = {
        'query': args.query,
        'partial_response': False,
        'dedup': True,
        'step': MIN_INTERVAL_MINUTES * 60 # hardcoded to 5m, it should match the one of the query !!
    }

    date_start_time = args.start_time
    date_end_time = date_start_time + timedelta(hours=MAX_QUERY_RANGE_HOURS)
    first_run = True

    dest_file_path = args.dest_file

    while date_start_time.timestamp() < datetime.now().timestamp():
        # generate dynamic query params
        params = copy.deepcopy(base_params)
        params["start"] = date_start_time.timestamp()
        params["end"] = date_end_time.timestamp()

        log.info("Querying Thanos with start [%s] and end [%s]",
                 format_timestamp(params['start']),
                 format_timestamp(params['end'])
        )

        with requests.get(BASE_URL, params=params, stream=True, verify=False) as r:
            json_response = r.json()
            if first_run:
                with open(dest_file_path, "w+") as file:
                    json.dump(json_response['data']['result'], file)
            else:
                with open(dest_file_path, "r+") as file2:
                    json_file = json.load(file2)
                    json_file[0]['values'].extend(json_response['data']['result'][0]['values'])

                    log.info("The query returned %s data points", len(json_response['data']['result'][0]['values']))
                    log.info("First timestamp added from the query: %s",
                             format_timestamp(json_response['data']['result'][0]['values'][0][0]))

                    log.info("Last timestamp added from the query: %s",
                             format_timestamp(json_response['data']['result'][0]['values'][-1][0]))

                    # point to the beginning to overwrite
                    file2.seek(0)
                    json.dump(json_file, file2)

        date_start_time = date_start_time + timedelta(hours=2, minutes=5)
        date_end_time = date_start_time + timedelta(hours=2)
        first_run = False
