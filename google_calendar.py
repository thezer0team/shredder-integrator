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

#logger.warning('This is a warning')
#logger.error('This is an error')

def grab_calendars(argv):
    '''
    Grab calendarId values for Google Calendar user after instantiating
    the service object
    '''

    # Authenticate and construct service.
    service, flags = sample_tools.init(
        argv, 'calendar', 'v3', __doc__, __file__,
        scope='https://www.googleapis.com/auth/calendar.readonly')

    # Init our list to store calendars
    calendars = []

    try:
        page_token = None
        while True:
            calendar_list = service.calendarList().list(
                pageToken=page_token).execute()

            for calendar_list_entry in calendar_list['items']:

                if 'holiday' in calendar_list_entry['id']:
                    break
                else:
                    calendars.append(calendar_list_entry['id'])
            page_token = calendar_list.get('nextPageToken')
            if not page_token:
                break
    except client.AccessTokenRefreshError:
        print('The credentials have been revoked or expired, please re-run'
              'the application to re-authorize.')
        logger.error('The credentials have been revoked or expired')

    return calendars


def transform_events(*args):
    '''
    Function accepts dictionary with calendars and events and transforms the object into a normalized event mapping
    '''
    values_list = [
        'summary', 
        'description', 
        'start', 
        'end', 
        'status', 
        'attendees'
        ]

    events = []

    for event in args:
        for item in values_list:
            try:
                event.get(item)

                if event[item] is not None and event[item] is not "":
                    print(event[item])
                    events.append(event[item])

            except KeyError as keyerror:
                print('[!] KeyError: {}'.format(keyerror))
                logger.error('Key Error encountered', exc_info=True)
    return events

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
        try:
            page_token = None
            while True:
                calendar_events = service.events().list(
                    calendarId=calendar,
                    timeMin=current_date_TS,
                    pageToken=page_token).execute()

                mapping[calendar] = calendar_events
                     
                page_token = calendar_events.get('nextPageToken')
                if not page_token:
                    break

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
    try:
        post = requests.post('https://httpbin.org/post', data = args)

    except 



    pass

if __name__ == '__main__':
    calendars = grab_calendars(sys.argv)
    events = grab_events(sys.argv, calendars)
    print(events)