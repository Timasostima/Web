import json


def load_json(filename):
    with open(filename, 'r') as file:
        return json.load(file)


def calc_distance(destinations):
    return len(destinations) * 200


def calc_price(destinations, plan_price):
    return len(destinations) * plan_price * 8
