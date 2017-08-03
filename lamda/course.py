"""Representation of UBC schedules and courses."""

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
        """Returns a list of ClassSessions given a section of a course.

        Args:
            section (dict): Requires the keys 'term', 'days', 'start_time', 'end_time'
                mapping to lists, lists must have the same length.
        Returns:
            list: List of ClassSession representing the course section.
        """
        terms = section['term']
        days_list = section['days']
        start_times = section['start_time']
        end_times = section['end_time']

        result = []
        for i, days in enumerate(days_list):
            for day in days.split(' '):
                result.append(ClassSession(terms[i], day, start_times[i], end_times[i]))
        return result


class Course(object):
    """Represents a UBC course.

    Attributes:
        name (str): Name of the course.
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
        """Creates a list of all sections of a course.

        Args:
            course_name (str): Name of the course.
            coursedb (dict): Database storing information about all courses.
        Returns:
            list: list of Course each representing a unique section of the course.
        """
        dept, cnum = course_name.split(' ')
        return [Course(sec, ClassSession.create_from_section(info))
                for sec, info in coursedb[dept][course_name].items()
                if info['activity'][0] == 'Lecture']


class ScheduleCreator:
    """Provides static methods to get Schedules."""
    @staticmethod
    def create_from_course_names(course_names, coursedb):
        """Returns a list of all non-conflicting schedules given a list of input course names."""
        schs = []
        for name in course_names:
            schs = append_perm(schs, Course.create_all(name, coursedb))
        return ScheduleCreator.wrap_body_for_awsgatewayapi(
            [ScheduleCreator.jsonify(sch) for sch in schs if ScheduleCreator.no_conflicts(sch)])

    @staticmethod
    def no_conflicts(potential_schedule):
        """Returns True if a schedule has no conflicts."""
        for course1 in potential_schedule:
            for course2 in potential_schedule:
                if course1.conflict(course2) and course1 is not course2:
                    return False
        return True

    @staticmethod
    def jsonify(sch):
        """Returns a list of JSON Serializable course data."""
        return [course.json() for course in sch]

    @staticmethod
    def wrap_body_for_awsgatewayapi(body):
        """Creates a valid response for AWS Gateway API given a response body."""
        return {
            'isBase64Encoded': False,
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': str(body)
        }

def append_perm(rlist, new_items):
    """Accumulates new permutations and returns it.

    Args:
        rlist (list): List to append to.
        new_items (list): Items to permutate into exisiting list.
    Returns
        list: Accumalted items.
    """
    if not rlist:
        return [[new_item] for new_item in new_items]

    result_rlist = []
    for r in rlist:
        for new_item in new_items:
            new_r = list(r)
            new_r.append(new_item)
            result_rlist.append(new_r)
    return result_rlist
