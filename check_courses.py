#!/bin/env python
import json

import twilio.rest

import ubc


def main():
    with open('secret.json', 'r') as f:
        SECRET = json.load(f)

    TWILLIO_ACCOUNT_SID = SECRET['TWILLIO_ACCOUNT_SID']
    TWILIO_AUTH_TOKEN = SECRET['TWILIO_AUTH_TOKEN']
    TWILIO_NUMBER = SECRET['TWILIO_NUMBER']
    MY_NUMBER = SECRET['MY_NUMBER']

    if not (TWILLIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN):
        raise AssertionError("Provide Twilio API sid and token")

    TWILIO_CLIENT = twilio.rest.Client(TWILLIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    WANTED_COURSES = ('STAT 251 L1B', 'STAT 251 L1D', 'CPSC 320 921')
    scrapper = ubc.CourseScrapper('2017', 'S')

    for course in WANTED_COURSES:
        if scrapper.is_full(course):
            print(course + ' is FULL :(')
            return

        print(course + ' has a free spot!')
        TWILIO_CLIENT.messages.create(
            to=MY_NUMBER,
            from_=TWILIO_NUMBER,
            body="{} a free spot!".format(course)
        )


if __name__ == '__main__':
    main()
