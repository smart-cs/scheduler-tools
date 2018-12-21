import ubc

class TestCourseScrapper:
    def test_extract_course_info(self):
        scrapper = ubc.CourseScrapper('2018', 'W')
        cname, cdata = scrapper.extract_course_info('CPSC 221')
        assert 'CPSC 221' == cname
        assert 'CPSC 221 101' in cdata
        assert cdata['title'] == 'CPSC 221 Basic Algorithms and Data Structures'
        assert cdata['pre_reqs'] == 'One of CPSC 210, EECE 210, CPEN 221 and one of CPSC 121, MATH 220.'
        assert cdata['credits'] == 4
        assert cdata['CPSC 221 101']['activity'] == ['Lecture']
        assert cdata['CPSC 221 101']['days'][0]
        assert cdata['CPSC 221 101']['start_time'][0]
        assert cdata['CPSC 221 101']['end_time'][0]
