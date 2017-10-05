"""Representation of UBC schedules and courses."""
import json

class ClassSession(object):
    """Holds time information about about a single class.

    Attributes:
        term (str): Term '1' or '2' or '1-2'.
        day (str): Day of the week of class.
        start (str): start time of class (24 hour representation).
        end (str): start time of class (24 hour representation).
    """
    def __init__(self, term, day, start, end):
        self.term = term
        self.day = day
        self.start = start
        self.end = end

    def conflict(self, other):
        """Returns True if this ClassSession conflicts with another ClassSession.

        Condition for conflict:
            1. Same term and day.
            2. Same start time OR same end time OR other start/end is between ours.
        """
        return (self.day == other.day and self.term == other.term
                and ((self.start <= other.start and other.start < self.end)
                     or (self.start < other.end and other.end <= self.end)))

    def json(self):
        """Returns a dict (JSON serializable) representation."""
        return {'term' : self.term, 'day' : self.day, 'start' : self.start, 'end' : self.end}

    @staticmethod
    def create_from_section(section):
        """Returns a generator of ClassSessions given a section of a course.

        Args:
            section (dict): Requires the keys 'term', 'days', 'start_time', 'end_time'
                mapping to lists, lists must have the same length.
        Returns:
            generator: Generator of ClassSession representing the course section.
        """
        terms = section['term']
        days_list = section['days'] # e.g. Mon Wed Fri
        start_times = section['start_time']
        end_times = section['end_time']

        return (ClassSession(terms[i], day, start_times[i], end_times[i])
                for i, days in enumerate(days_list)
                for day in days.split(' '))


class Course(object):
    """Represents a UBC course.

    Attributes:
        name (str): Name of the course <DEPT> <LEVEL> <SECTION>.
        class_sessions (list): List of ClassSession.
    """
    def __init__(self, name, class_sessions):
        self.name = name
        self.class_sessions = class_sessions

    def json(self):
        """Returns a dict (JSON serializable) representation."""
        return {self.name : [session.json() for session in self.class_sessions]}

    def conflict(self, other_course):
        """Returns true if any of our ClassSession conflict with any of their ClassSession."""
        for our_session in self.class_sessions:
            for other_session in other_course.class_sessions:
                if our_session.conflict(other_session):
                    return True

        return False

    @staticmethod
    def create_all(course_name, coursedb):
        """Creates a generator of all sections of a course.

        Args:
            course_name (str): Name of the course in the form of <DEPT> <LEVEL>.
            coursedb (dict): Database storing information about all courses.
        Returns:
            generator: Generator of Course each representing a unique section of the course.
        """
        dept, cnum = course_name.split(' ')
        return (Course(sec, list(ClassSession.create_from_section(info)))
                for sec, info in coursedb[dept][course_name].items()
                if info['activity'][0] == 'Lecture')
