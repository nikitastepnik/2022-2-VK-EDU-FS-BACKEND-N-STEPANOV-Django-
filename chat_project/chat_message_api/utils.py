import json

import requests
from bs4 import BeautifulSoup


def publish_message_to_websocket(messages, channel):
    command = {
        "method": "publish",
        "params": {
            "channel": channel,
            "data": messages
        }
    }

    parsed_config = parse_json_config(
        '/Users/ni-n-stepanov/PycharmProjects/2022-2-VK-EDU-FS-BACKEND-N-STEPANOV/config.json')
    api_key = parsed_config['api_key']

    data = json.dumps(command)

    headers = {'Content-type': 'application/json', 'Authorization': 'apikey ' + api_key}
    requests.post("http://localhost:8000/api", data=data, headers=headers)


def parse_json_config(json_file):
    with open(json_file) as json_data:
        data = json.load(json_data)

    return data


def clear_html_tags(user_input):
    soup = BeautifulSoup(user_input, "html.parser")
    text_input = soup.get_text()

    return text_input
