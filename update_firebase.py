"""Loads UBC Course data into Firebase."""

import json
import time

import requests

import util

def scrape_course_from(year, session):
    """Scrape information from UBC Course Schedule Website and store it onto Firebase.

    Args:
        year (str): Academic year.
        session (str): Academic session - 'W' for Winter, 'S' for Summer.
    """

    base_url = 'https://ubc-coursedb.firebaseio.com/{0}{1}/'.format(year, session)
    rsession = requests.Session()
    scraper = util.CourseScraperUBC(year, session)

    for dept_link in scraper.dept_links():
        dept_name = util.extract_field('department', dept_link)

        dept = {}
        for course_link in scraper.course_links_from_dept(dept_link, in_format='link'):
            name, info = scraper.extract_course_info(course_link, in_format='link')
            dept[name] = info

        json_encoded = json.JSONEncoder().encode(dept)

        url_endpoint = base_url + dept_name + '.json'
        r = rsession.patch(url_endpoint, data=json_encoded)
        if r.status_code != 200:
            print("FAILED:", r.url)

        # be nice to UBC server
        time.sleep(1)

def main():
    YEAR = '2017'
    SESSION = 'W'

    scrape_course_from(YEAR, SESSION)

if __name__ == '__main__':
    main()
