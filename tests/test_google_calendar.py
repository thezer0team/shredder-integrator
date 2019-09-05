<<<<<<< HEAD
from google_calendar import grab_calendars
from google_calendar import transform_events
from google_calendar import grab_events
from google_calendar import verify_platform_calendar
from google_calendar import verify_user_appcalID
from google_calendar import verify_user_exists
from google_calendar import request_new_appcalID
from google_calendar import request_new_userID
from google_calendar import post_events


test_dict = {
        "summary": "Test Summary",
        "description": "Test Description",
        "start": "2019-08-23",
        "end": "2019-09-01",
        "status": "Busy",
        "attendees": "test.user@gmail.com",
        "additional": {
            "random": "more random",
            "random2": "more more random",
        }
}
normalized_result = {
        "summary": "Test Summary",
        "description": "Test Description",
        "start": "2019-08-23",
        "end": "2019-09-01",
        "status": "Busy",
        "attendees": "test.user@gmail.com",
}


def test_transform_events():
    ''' Test data normalizer '''
    result = transform_events(test_dict)
    assert result == normalized_result


def test_transform_event_has_summary():
    ''' Test that transform function has summary '''
    result = transform_events(test_dict)
    summary = result.get('summary')
    assert summary