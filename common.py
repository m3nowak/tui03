import json

from contextlib import closing

def load_json(filename):
    with closing(open(filename, 'r')) as raw_json:
        loaded_json = json.load(raw_json)
    return loaded_json

def save_json(filename, object):
    with closing(open(filename, 'w')) as raw_json:
        json.dump(object, raw_json, indent=4, sort_keys=True)