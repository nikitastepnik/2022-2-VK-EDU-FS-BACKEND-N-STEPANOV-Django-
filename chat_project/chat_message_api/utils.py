import json

import requests


def publish_message_to_websocket(text_msg, channel="chat"):
    command = {
        "method": "publish",
        "params": {
            "channel": channel,
            "data": text_msg
        }
    }

    parsed_config = parse_json_config('config.json')
    api_key = parsed_config['api_key']

    data = json.dumps(command)
    headers = {'Content-type': 'application/json', 'Authorization': 'apikey ' + api_key}
    requests.post("http://localhost:8000/api", data=data, headers=headers)


def parse_json_config(json_file):
    with open(json_file) as json_data:
        data = json.load(json_data)

    return data
