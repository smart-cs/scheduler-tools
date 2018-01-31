#!/usr/bin/env python

"""Loads UBC Course data into Firebase."""
import json
import time

import requests

import util

FIREBASE_PROJECT = 'ubc-coursedb'
YEAR = '2017'
SESSION = 'W'


def scrape_from(year, session):
    """Scrape information from UBC Course Schedule Website and store it onto Firebase.

    Args:
        year (str): Academic year.
        session (str): Academic session - 'W' for Winter, 'S' for Summer.
    """

    base_url = f'https://{FIREBASE_PROJECT}.firebaseio.com/{year}{session}/'
    rsession = requests.Session()
    scrapper = util.CourseScraperUBC(year, session)

    for dept_link in scrapper.dept_links():
        dept_name = util.extract_field('department', dept_link)

        dept = {}
        for course_link in scrapper.course_links_from_dept(dept_link, in_format='link'):
            name, info = scrapper.extract_course_info(course_link, in_format='link')
            dept[name] = info

        json_encoded = json.JSONEncoder().encode(dept)

        url_endpoint = base_url + dept_name + '.json'
        r = rsession.patch(url_endpoint, data=json_encoded)
        if r.status_code != 200:
            print('FAILED:', r.url)

        # Be nice to the UBC server
        time.sleep(1)


def main():
    scrape_from(YEAR, SESSION)


if __name__ == '__main__':
    main()
