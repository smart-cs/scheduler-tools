"""Function for AWS Lambda."""
import course
import requests

COURSEDB = requests.get('https://ubc-coursedb.firebaseio.com/2017W.json').json()

def lambda_handler(event, context):
    """Function runs when triggered by AWS Lambda."""
    print(event)
    input_courses = event['queryStringParameters']['courses'].split(',')
    print(input_courses)
    response = course.ScheduleCreator.create_from_course_names(input_courses, COURSEDB)
    print(response)
    return response
