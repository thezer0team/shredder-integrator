from google_calendar import grab_calendars
from google_calendar import transform_events
from google_calendar import grab_events
from google_calendar import verify_platform_calendar
from google_calendar import verify_user_appcalID
from google_calendar import verify_user_exists
from google_calendar import request_new_appcalID
from google_calendar import request_new_userID
from google_calendar import post_events

def test_post_events():
    assert True

test_event = {
    'summary': 'This is a test summary of an event',
    'description': 'This is a test description of an event',
    'start': '10/01/2019 16:00',
    'end': '10/01/2019 18:00',
    'status': 'Busy',
    'attendees': 'test.user@gmail.com',
    'erroneous': 'This is useless for our transform needs'
    }

def test_tranform_events():
    ''' Test that our transform function does not return None '''
    result = transform_events(test_event)