from google_calendar import transform_events


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
        "attendees": "test.user@gmail.com",
        "status": "Busy",
        "end": "2019-09-01",
        "start": "2019-08-23",
        "description": "Test Description",
        "summary": "Test Summary",
        }


def test_transform_events(events=test_dict):
    ''' Test data normalizer '''
    assert transform_events(test_dict) == normalized_result
