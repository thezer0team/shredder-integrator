## Shredder Integrator

Integration service for pulling from various API's and POST'ing to backend service to support calendar consolidation. 

## Purpose

One place for all your disparate calendar systems. Want to send an event to your friend? Know what platform? Who cares. 

Let us handle the process of making sure it ends up on whatever platform they use and focus on finding time and spending it with people you care about.

## Running via CLI

`python google_calendar.py`

## Development

1. `git clone https://github.com/thezer0team/shredder-integrator.git`
2. `pipenv install --dev`
3. Ensure you have an OAuth approved application created and client_id and client_secret in a `client_secrets.json` file. Sample here: https://github.com/googleapis/google-api-python-client/blob/master/samples/calendar_api/client_secrets.json

### Minimum Python Version

3.7+

### Built With

- VSCode
- Pipenv

## Testing

```
D:\Documents\Python\shredder-integrator [master ≡]> python -m pytest -v --cov tests 
============================================ test session starts ============================================= 
platform win32 -- Python 3.7.2, pytest-5.1.2, py-1.8.0, pluggy-0.12.0 -- C:\Users\axi0m\.virtualenvs\shredder-integrator-zMysVctz\Scripts\python.exe
cachedir: .pytest_cache
rootdir: D:\Documents\Python\shredder-integrator
plugins: cov-2.7.1, icdiff-0.2
collected 1 item                                                                                               

tests/test_google_calendar.py::test_transform_events PASSED                                             [100%] 

----------- coverage: platform win32, python 3.7.2-final-0 -----------
Name                            Stmts   Miss  Cover
---------------------------------------------------
tests\test_google_calendar.py       5      0   100%


============================================= 1 passed in 0.83s ============================================== 
```
