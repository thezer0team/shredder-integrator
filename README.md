## Shredder Integrator
Integration service for pulling from various API's and POST'ing to backend service to support calendar consolidation. 

## Purpose
One place for all your disparate calendar systems. Want to send an event to your friend? Know what platform? Who cares. 

Let us handle the process of making sure it ends up on whatever platform they use and focus on finding time and spending it with people you care about.

## Running via CLI
python google_calendar.py

## Development
1. git clone https://github.com/thezer0team/shredder-integrator.git
2. pipenv install
3. Ensure you have an OAuth approved application created and client_id and client_secret in a client_secrets.json file. Sample here: https://github.com/googleapis/google-api-python-client/blob/master/samples/calendar_api/client_secrets.json

### Minimum Python Version
3.7+

### Built With
- VSCode
- Pipenv