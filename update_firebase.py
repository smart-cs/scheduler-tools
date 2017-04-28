"""
Loads UBC Courses data into Firebase.
"""

import json
import time

import requests

import util

def scrape_course_from(year, session):
    """ Scrape information from UBC Course Schedule Website and store it onto Firebase.

    Args:
        year (str): Academic year.
        session (str): Academic session - 'W' for Winter, 'S' for Summer.
    """

    base_url = 'https://ubc-coursedb.firebaseio.com/{0}{1}/'.format(year, session)
    rsession = requests.Session()
    scraper = util.CourseScraperUBC(year, session)

    for dept_link in scraper.dept_links():
        dept = {}

        for course_link in scraper.course_links_from_dept(dept_link, in_format='link'):
            name, info = scraper.extract_course_info(course_link, in_format='link')
            dept[name] = info

        json_encoded = json.JSONEncoder().encode(dept)

        dept_name = util.extract_field('department', dept_link)
        rsession.put(base_url + dept_name + '.json', data=json_encoded)

        # be nice to UBC server
        time.sleep(1)

if __name__ == '__main__':
    YEAR = '2017'
    SESSION = 'S'

    scrape_course_from(YEAR, SESSION)
