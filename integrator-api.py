from eve import eve

class HealthStatus(self):
    self.name = 'HealthStatus'
    self.endpoint = '/status'
    self.settings = {'STATUS': 'Healthy',
        {'CURRENT_STATE': 'Running'}
    }
    # TODO: Is there a method to run self-checks within the application itself?

    def run(self):
        app = Eve(settings=settings)
        app.run()

class Metrics(self):
    self.name = 'Metrics'
    self.endpoint = '/metrics'
    self.settings = {'LAST_SUCCESSFUL': '2019-08-02T20:00:01Z'}
    # TODO: Add more metrics as needed

    def run(self):
        app = Eve(settings=settings)
        app.run()

if __name__ == '__main__':
    if route == 'Metrics':
        Metrics.run()
    if route == 'HealthStatus':
        HealthStatus.run()