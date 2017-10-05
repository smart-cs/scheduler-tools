"""Function for AWS Lambda."""
import json
import requests
import schedulecreator

KEY = '2017W'
BASE_URL = 'https://ubc-coursedb.firebaseio.com'
COURSEDB = requests.get('{:s}/{:s}.json'.format(BASE_URL, KEY)).json()

def wrap_body_for_awsgatewayapi(body):
    """Creates a valid response for AWS Gateway API given a response body."""
    return {
        'isBase64Encoded': False,
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(body)
    }


def lambda_handler(event, context):
    """Function runs when triggered by AWS Lambda."""
    print(event)

    input_courses = event['queryStringParameters']['courses'].split(',')
    print(input_courses)

    response = wrap_body_for_awsgatewayapi(
        schedulecreator.create_from_course_names(input_courses, COURSEDB))

    print(response)
    return response
