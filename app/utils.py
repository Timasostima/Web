import json


def load_json(filename):
    with open(filename, 'r') as file:
        return json.load(file)
