import json


def parse_json_config(json_file):
    with open(json_file) as json_data:
        data = json.load(json_data)

    return data
