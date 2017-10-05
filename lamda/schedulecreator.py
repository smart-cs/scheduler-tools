"""Helpful functions to create schedules."""
import course

# TODO: this function can be moved to a 'util' module or something similar
def append_perm(iterable_lists, new_items):
    """Accumulates new permutations and returns it.

    Args:
        iterable (iterable): Iterable of lists to append to.
        new_items (list): Items to permutate into exisiting Iterable.
    Returns
        generator: Accumalted items.
    """
    if not iterable_lists:
        return ([new_item] for new_item in new_items)
    return (list(l) + [new_item] for l in iterable_lists for new_item in new_items)


def jsonify_schedule(sch):
    """Returns a list of JSON Serializable course data."""
    return [course.json() for course in sch]


def no_conflicts(potential_schedule):
    """Returns True if a schedule has no conflicts."""
    for course1 in potential_schedule:
        for course2 in potential_schedule:
            if course1.conflict(course2) and course1 is not course2:
                return False
    return True


def create_from_course_names(course_names, coursedb):
    """Returns a response where the body contains of all non-conflicting schedules (course_name is a list)."""
    schs = []
    for name in course_names:
        schs = append_perm(schs, course.Course.create_all(name, coursedb))
    return [jsonify_schedule(sch) for sch in schs if no_conflicts(sch)]
