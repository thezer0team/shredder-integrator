#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
CLI Application to collect Google Calendars and calendar events
"""

import sys
from oauth2client import client
from googleapiclient import sample_tools
import datetime


def grab_calendars(argv):
    '''
    Grab calendarId values for Google Calendar user after instantiating
    the service object
    '''

    # Authenticate and construct service.
    service, flags = sample_tools.init(
        argv, 'calendar', 'v3', __doc__, __file__,
        scope='https://www.googleapis.com/auth/calendar.readonly')

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

    return calendars


def transform_events(*args):
    '''
    Function accepts dictionary with calendars and events and transforms the object into a normalized event mapping
    '''
    values_list = ['summary', 'description', 'start', 'end', 'status', 'attendees']
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
    return events

def grab_events(argv, calendars):
    '''
    Provide list of calendar IDs to func and this func collects events
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
    return mapping

if __name__ == '__main__':
    calendars = grab_calendars(sys.argv)
    events = grab_events(sys.argv, calendars)
    print(events)