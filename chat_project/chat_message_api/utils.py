import json

import requests
from bs4 import BeautifulSoup

from utils import parse_json_config


def publish_message_to_websocket(messages, channel):
    command = {
        "method": "publish",
        "params": {
            "channel": channel,
            "data": messages
        }
    }

    parsed_config = parse_json_config('config.json')
    api_key = parsed_config['api_key']

    data = json.dumps(command)

    headers = {'Content-type': 'application/json', 'Authorization': 'apikey ' + api_key}
    requests.post("http://centrifugo:8000/api", data=data, headers=headers)


def clear_html_tags(user_input):
    soup = BeautifulSoup(user_input, "html.parser")
    text_input = soup.get_text()

    return text_input
