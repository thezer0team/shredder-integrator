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


def verify_events(*args):
    '''
    Function accepts an event 'dict' and 'value' and verifies the value exists and isn't None
    '''
    values_list = ['summary', 'description', 'start', 'end', 'status', 'attendees']

    for event in args:
        for item in values_list:
            try:
                event.get(item)

                if event[item] is not None and event[item] is not "":
                    print(event[item])

            except KeyError as keyerror:
                print('[!] KeyError: {}'.format(keyerror))


def grab_events(argv, calendars):
    '''
    Provide list of calendar IDs to func and this func collects events
    '''

    # Authenticate and construct service.
    service, flags = sample_tools.init(
        argv, 'calendar', 'v3', __doc__, __file__,
        scope='https://www.googleapis.com/auth/calendar.readonly')

    events = []
    current_date_TS = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()

    for calendar in calendars:
        try:
            page_token = None
            while True:
                calendar_events = service.events().list(
                    calendarId=calendar,
                    timeMin=current_date_TS,
                    pageToken=page_token).execute()

                # for calendar_events_entry in calendar_events['items']:
                #     verify_event_object(calendar_events_entry, 'summary')
                #     verify_event_object(calendar_events_entry, 'start')
                #     verify_event_object(calendar_events_entry, 'end')
                #     verify_event_object(calendar_events_entry, 'description')
                #     verify_event_object(calendar_events_entry, 'status')
                #     verify_event_object(calendar_events_entry, 'attendees')
                events = map(verify_events, calendar_events['items'])

                page_token = calendar_events.get('nextPageToken')
                if not page_token:
                    break
        except client.AccessTokenRefreshError:
            print('The credentials have been revoked or expired, please re-run'
                'the application to re-authorize.')


if __name__ == '__main__':
    calendars = grab_calendars(sys.argv)
    events = grab_events(sys.argv, calendars)