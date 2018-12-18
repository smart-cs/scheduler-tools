#!/usr/bin/env python
import datetime
import json

import click
import requests

import ubc


@click.group()
def cli():
    pass


@cli.command()
@click.option('--year', type=click.Choice(['2018', '2019']), default='2018')
@click.option('--session', type=click.Choice(['W', 'S']), default='W')
def scrape(year, session):
    """ Downlodas UBC Course Schedule data to local storage."""
    scrapper = ubc.CourseScrapper(year, session)
    data = {}
    for dept_link in scrapper.dept_links():
        dept_name = ubc.extract_field('department', dept_link)
        print('scraping {}...'.format(dept_name))
        dept = dict(
            scrapper.extract_course_info(cl, in_format='link')
            for cl in scrapper.course_links_from_dept(dept_name, in_format='name')
        )
        data[dept_name] = dept

    today = datetime.datetime.today().strftime('%Y-%m-%d')
    filename = '{}{}_{}.json'.format(year, session, today)
    with open(filename, 'w') as f:
        json.dump(data, f)
    click.echo('created: ' + filename)


@cli.command()
@click.argument('upload_file', type=click.File('r'))
def upload(upload_file):
    """ Uploads local data to Firebase."""
    URL = 'https://ubc-coursedb.firebaseio.com/{}'.format(upload_file.name)
    resp = requests.post(URL, json=json.load(upload_file))
    resp.raise_for_status()
    click.echo('uploaded: ' + upload_file.name)


if __name__ == '__main__':
    cli()