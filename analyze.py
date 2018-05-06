#!/usr/bin/env python3
import json
from os.path import isfile

import requests


def get_db(year, session):
    db_path = f'{year}{session}-db.json'
    if not isfile(db_path):
        _download_db(year, session, db_path)

    with open(db_path) as f:
        return json.load(f)


def _download_db(year, session, destination):
    FIREBASE_DB_URL = f'https://ubc-coursedb.firebaseio.com/{year}{session}.json'

    resp = requests.get(FIREBASE_DB_URL)

    print(f'GET {resp.url} => {resp.status_code}')

    if resp.status_code != 200:
        raise Exception('error downloading database')

    with open(destination, 'w') as f:
        f.write(resp.text)


def unique_activity_types(db):
    return {
        info['activity'][0]
        for dept in db
        for course in db[dept]
        for section, info in db[dept][course].items()
        if info['activity']
    }


def unique_days_types(db):
    return {
        info['days'][0]
        for dept in db
        for course in db[dept]
        for section, info in db[dept][course].items()
        if info['days']
    }


def sections_without_start_time(db):
    return {
        section: info
        for dept in db
        for course in db[dept]
        for section, info in db[dept][course].items()
        if not info['start_time'] or not info['start_time'][0]
    }


def sections_with_more_than_one_activity_type(db):
    return {
        section: info
        for dept in db
        for course in db[dept]
        for section, info in db[dept][course].items()
        if len(info['activity']) > 1
    }


def main():
    YEAR = '2017'
    SESSION = 'W'
    db = get_db(YEAR, SESSION)
    for days in unique_days_types(db):
        print(days)
    # for activity in unique_activity_types(db):
    #     print(activity)
    # data = sections_with_more_than_one_activity_type(db)
    # print(json.dumps(data))


if __name__ == '__main__':
    main()
