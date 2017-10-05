import unittest
import requests

import course

class TestCourseModule(unittest.TestCase):
    def test_append_perm(self):
        result = list(course.append_perm([], ['a', 'b', 'c']))
        expected = [['a'], ['b'], ['c']]
        self.assertCountEqual(expected, result)
        self.assertListEqual(expected, result)

        result = list(course.append_perm([['a'], ['b'], ['c']], ['1', '2', '3', '4']))
        expected = [['a', '1'], ['a', '2'], ['a', '3'], ['a', '4'],
                    ['b', '1'], ['b', '2'], ['b', '3'], ['b', '4'],
                    ['c', '1'], ['c', '2'], ['c', '3'], ['c', '4']]
        self.assertCountEqual(expected, result)
        self.assertListEqual(expected, result)

class TestScheduleCreator(unittest.TestCase):
    def setUp(self):
        self.db = requests.get('https://ubc-coursedb.firebaseio.com/2017W.json').json()

    def tearDown(self):
        pass

    def test_create_from_course_names(self):
        # result = course.ScheduleCreator.create_from_course_names(['MATH 100', 'GRSJ 230'], self.db)
        pass
         
if __name__ == '__main__':
    unittest.main()
