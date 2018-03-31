#!/usr/bin/env python

"""Loads UBC Course data into Firebase."""
from json import JSONEncoder
from time import sleep

import requests

import util

FIREBASE_PROJECT = 'ubc-coursedb'
YEAR = '2017'
SESSION = 'W'
BASE_URL = f'https://{FIREBASE_PROJECT}.firebaseio.com/{YEAR}{SESSION}'

RSESSION = requests.Session()
SCRAPPER = util.CourseScrapperUBC(YEAR, SESSION)
JSON_ENCODER = JSONEncoder()


def scrape_all():
    """Scrape information from UBC Course Schedule Website and store it onto Firebase.

    Args:
        year (str): Academic year.
        session (str): Academic session - 'W' for Winter, 'S' for Summer.
    """
    for dept_link in SCRAPPER.dept_links():
        dept_name = util.extract_field('department', dept_link)
        dept = get_dept(dept_name)
        print(JSON_ENCODER.encode(dept))
        upload(dept_name, JSON_ENCODER.encode(dept))
        # Be nice to the UBC server
        sleep(1)


def get_dept(department_name):
    """Returns a dict of courses and their correpsponding information.

    Args:
        department_name (str): Name of the department.
    Returns:
        dict: course_name (str) to dict of course_section (str) to section information.
    """
    dept = {}
    for course_link in SCRAPPER.course_links_from_dept(department_name, in_format='name'):
        name, info = SCRAPPER.extract_course_info(course_link, in_format='link')
        dept[name] = info
    return dept


def upload(key, data):
    """Uploads JSON encoded data to Firebase Database.

    Args:
        key (str): Location to store the data
        data (str): JSON encoded string of data
    """
    response = RSESSION.patch(f'{BASE_URL}/{key}.json', data=data)
    if response.status_code != 200:
        print('FAILED:', response.url)


def main():
    scrape_all()


if __name__ == '__main__':
    main()
