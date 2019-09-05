#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
CLI Application to collect Google Calendars and calendar events
"""

import sys
from oauth2client import client
from googleapiclient import sample_tools
import datetime
import logging
from time import strftime,gmtime
import requests
import pytest
import pprint
import json

logger = logging.getLogger(__name__)

# Todays date
today = strftime("%Y-%m-%d", gmtime())

# Setup our handlers, one for console and one for file
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler('{}_{}.log'.format(today,__name__))

# Set Logging Levels per Handler
c_handler.setLevel(logging.WARNING)
f_handler.setLevel(logging.ERROR)

# Create our formatter object
c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Set our formatter on each handler
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

# Add the handlers for the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)

DEBUG_MODE = True

def grab_calendars(argv):
    '''
    Grab calendarId values for Google Calendar user after instantiating
    the service object
    '''

    # Authenticate and construct service.

    print(argv)

    try:
        service, flags = sample_tools.init(
            argv, 'calendar', 'v3', __doc__, __file__,
            scope='https://www.googleapis.com/auth/calendar.readonly')
        logger.debug("[+] Authenticated to Google API Endpoint")
    except Exception as e:
        logger.debug("[!] Unable to construct Google API Service object: {}".format(e))

    # Init our list to store calendars
    calendars = []

    try:
        page_token = None
        while True:
            calendar_list = service.calendarList().list(
                pageToken=page_token).execute()
            logger.debug("[^] Calendar list method executed: {}".format(calendar_list))

            for calendar_list_entry in calendar_list['items']:

                if 'holiday' in calendar_list_entry['id']:
                    break
                else:
                    calendars.append(calendar_list_entry['id'])
                    logger.debug("Added calendar {} to calendar list".format(calendar_list_entry))
            page_token = calendar_list.get('nextPageToken')
            if not page_token:
                break

    except client.AccessTokenRefreshError:
        print('The credentials have been revoked or expired, please re-run'
              'the application to re-authorize.')
        logger.error('The credentials have been revoked or expired')

    return calendars


def transform_events(events):
    '''
    Function accepts dictionary within a dictionary and transforms the object into a flattened data structure
    '''
    values_list = [
        'summary',
        'description',
        'start',
        'end',
        'status',
        'attendees'
        ]
    normalized_events = {}
    for i in events.items():
        if i in values_list:
            normalized_events.update(i)
            print(normalized_events)
    
    return normalized_events

def grab_events(argv, calendars):
    '''
    Provide list of calendar IDs to function and this function collects events
    '''

    # Authenticate and construct service.
    service, flags = sample_tools.init(
        argv, 'calendar', 'v3', __doc__, __file__,
        scope='https://www.googleapis.com/auth/calendar.readonly')

    # Init our data structure to store calendar and events
    mapping = {}

    # Get currnet timestamp in ISO format and with TZ info for Google API
    current_date_TS = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()

    for calendar in calendars:
        logger.debug("[^] Collecting events from calendar {}".format(calendar))
        try:
            page_token = None              
            while True:
                calendar_events = service.events().list(
                    calendarId=calendar,
                    timeMin=current_date_TS,
                    pageToken=page_token).execute()

                page_token = calendar_events.get('nextPageToken')
                if not page_token:
                    break

            mapping[calendar] = calendar_events

        except client.AccessTokenRefreshError:
            print('The credentials have been revoked or expired, please re-run'
                'the application to re-authorize.')
            logger.error('The credentials have been revoked or expired')
    return mapping

def verify_user_exists(username):
    ''' 
    Pseudo code to check if an API endpoint returns true
    '''
    pass

def request_new_userID(email):
    '''
    Function to request new User ID be created from user email
    '''
    pass

def verify_user_appcalID(userid):
    '''
    Function to verify if user has an existing AppCalID
    '''
    pass

def request_new_appcalID(userid):
    '''
    Function to request new AppCalID if a user does not have one
    '''
    pass

def verify_platform_calendar(userid, appCalID):
    '''
    Function to verify this calendar exists and is associated with the appCalID
    '''
    pass

def post_events(*args):
    '''
    Function to HTTP POST events to backend service API
    '''
    backend_api_url = 'https://httpbin.org/post'
    print(args)

    try:
        post = requests.post(backend_api_url, data = args)
        logger.info('HTTP POST with event payload sent to {}'.format(backend_api_url))

    except Exception as e:
        logger.error('Failed to POST to backend service API, exception is: {}'.format(e))

    if post.status_code == 200:
        logger.info('Info - Status Code is 200 for URL: {}'.format(backend_api_url))
        return True
    else:
        logger.error('Error - Status code for URL is {}'.format(post.status_code))
        return False

if __name__ == '__main__':
    calendars = grab_calendars(sys.argv)
    events = grab_events(sys.argv, calendars)
    normalized_events = transform_events(events)
    pprint.pprint(normalized_events)
    #pprint.pprint(events)
    #post_events(events)