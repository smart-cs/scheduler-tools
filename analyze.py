#!/usr/bin/env python
import json
from os.path import isfile

import requests

YEAR = '2017'
SESSION = 'W'
LOCAL_DB_PATH = f'{YEAR}{SESSION}-db.json'


def load_local_db():
    if not isfile(LOCAL_DB_PATH):
        download_db()

    with open(LOCAL_DB_PATH) as f:
        return json.load(f)


def download_db():
    YEAR = '2017'
    SESSION = 'W'
    FIREBASE_DB_URL = f'https://ubc-coursedb.firebaseio.com/{YEAR}{SESSION}.json'
    r = requests.get(FIREBASE_DB_URL)
    print(f'GET {r.url} => {r.status_code}')
    if r.status_code != 200:
        raise Exception('error downloading database')

    with open(LOCAL_DB_PATH, 'w') as f:
        f.write(r.text)


def get_activity_types(db):
    result = {
        info['activity'][0]
        for dept in db
        for course in db[dept]
        for section, info in db[dept][course].items()
        if len(info['activity']) > 0
    }
    return result


def main():
    db = load_local_db()
    for a in sorted(get_activity_types(db)):
        print(a)


if __name__ == '__main__':
    main()
