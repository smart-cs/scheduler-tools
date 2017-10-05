"""Provides various functions for handling UBC course schedule HTML scraping"""
import re

import requests
import bs4

COURSE_RE = re.compile(r'course=(\d{2,3}\w?)')
COURSE_RE = re.compile(r'dept=(\w{3,4})')

def extract_field(field, url_endpoint, default=None):
    """Extrat a field from an URL endpoint.

    Args:
        field (str): Name of the field to extract. Supports 'course', 'department'.
        url_endpoint (str): URL endpoint.
    Returns:
        str: Value of the 'field' or default if not found.
    """

    if field is 'course':
        match = COURSE_RE.search(url_endpoint)
    elif field is 'department':
        match = COURSE_RE.search(url_endpoint)
    else:
        return default

    return match.group(1) if match else default


class CourseScraperUBC:
    """UBC Course Schedule Scrapping Session."""

    BASE_URL = 'https://courses.students.ubc.ca'
    REST_BASE_URL = BASE_URL + '/cs/main?'
    PNAME = 'subjarea'
    TNAME = 'subjareas'

    def __init__(self, sessyr, sesscd):
        """
        Args:
            sessyr (str): Academic year.
            sesscd (str): Academic session - 'W' for Winter, 'S' for Summer.
        """
        self.rsession = requests.Session()
        self.rsession.params = {
            'pname' : self.PNAME,
            'tname' : self.TNAME,
            'sessyr' : sessyr,
            'sesscd' : sesscd
        }


    def is_full(self, course):
        """Checks if a course with section is full or not.

        Args:
            course (str): In the form of <DEPARTMENT> <COURSE #> <SECTION #>.
                e.g. CPSC 221 101
        Returns:
            boolean: True if the course is full, False otherwise.
        Raises:
            ValueError: 'course' is in an invalid format.
            HttpError: Error on HTTP request.
        """

        parsed = course.split()

        # TODO: better error checking here
        if len(parsed) != 3:
            raise ValueError("String must be in the form of '<DEPARTMENT> <COURSE #> <SECTION #>'")

        url_params = {
            'req' : '5',
            'dept' : parsed[0],
            'course' : parsed[1],
            'section' : parsed[2]
        }

        response = self.rsession.get(self.REST_BASE_URL, params=url_params)
        response.raise_for_status()

        if 'Total Seats Remaining' not in response.text:
            raise Exception("URL doesn't contain seat information: {}".format(response.url))
        return 'Note: this section is full' in response.text


    def dept_links(self):
        """Get the deparments that are offering courses in this year and session.

        Returns:
            list: List of links to UBC departments.
        """

        url_params = {'req' : '0'}

        response = self.rsession.get(self.REST_BASE_URL, params=url_params)
        response.raise_for_status()

        soup = bs4.BeautifulSoup(response.text, "lxml")

        return [self.BASE_URL + a['href']
                for a in soup.find_all('a', href=True)
                if extract_field('department', a['href'])]


    def course_links_from_dept(self, department, in_format='name'):
        """See what courses a department offers.

        Args:
            department (str): Department name or link.
            in_format (str): Format of 'deparment' param. Supports 'name' or 'link'.
        Returns:
            tuple: (course_name, dict)
                inner dict of (section_name, dict of
                    status, activity, term, interval, days, start_time, end_time)
        Raises:
            ValueError: Invalid 'in_format'.
        """
        if in_format == 'name':
            url_params = {
                'req' : '1',
                'dept' : department
            }
            response = self.rsession.get(self.REST_BASE_URL, params=url_params)
        elif in_format == 'link':
            response = self.rsession.get(department)
        else:
            raise ValueError('in_format not implemented')

        soup = bs4.BeautifulSoup(response.text, "lxml")

        return [self.BASE_URL + a['href']
                for a in soup.find_all('a', href=True)
                if extract_field('course', a['href'])]


    def extract_course_info(self, course, in_format='name'):
        """Extracts information about a course such as CPSC 221.

        Args:
            course (str): Course name or link.
            in_format (str): Format of 'course' param. Supports 'name' or 'link'.
        Returns:
            tuple : (course_name, dict)
                inner dict of (section_name, dict of
                    status, activity, term, interval, days, start_time, end_time)
        Raises:
            ValueError: Invalid 'in_format'.
        """

        if in_format == 'name':
            course_name = course
            tmp = course.split()
            query_params = {
                'dept' : tmp[0],
                'course' : tmp[1]
            }
            response = self.rsession.get(self.REST_BASE_URL, params=query_params)
        elif in_format == 'link':
            course_name = '{0} {1}'.format(
                extract_field('department', course),
                extract_field('course', course)
            )
            response = self.rsession.get(course)
        else:
            raise ValueError('in_format not implemented')

        response.raise_for_status()
        soup = bs4.BeautifulSoup(response.text, "lxml")
        trs = soup.find_all('tr', attrs={"class" : ["'section1'", "section"]})

        # tuple: (status, section, activity, term, interval, days, start_time, end_time, comments)
        course_sections_info = [tuple(td.text.strip() for td in tr.find_all('td')) for tr in trs]
        return (course_name, self._parse_course_sections(course_sections_info))


    def _parse_course_sections(self, course_sections_info):
        """
        Args:
            course_sections_info (list): List of tuples of course section information.
        Returns:
            dict: dictionary of 'section name (str)' to data about the section.
        """
        course_info = {}

        for section_info in course_sections_info:
            (status, section, activity, term, interval, days, start_time, end_time, comments) = section_info

            # new section
            if section != '':
                last_section = section
                course_info[last_section] = {
                    'status': status,
                    'activity':[activity],
                    'term':[term],
                    'interval': interval,
                    'days':[days],
                    'start_time':[start_time],
                    'end_time':[end_time]
                }
            # attached to the last section
            else:
                section_info = course_info[last_section]
                section_info['activity'].append(activity)
                section_info['term'].append(term)
                section_info['days'].append(days)
                section_info['start_time'].append(start_time)
                section_info['end_time'].append(end_time)

        return course_info
