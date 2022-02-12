"""
Post request dont work on Djano apps on A2 hosted servers. This replacement 'passenger_wsgi.py'
has fixed the issue for me. Works with python3 and Django 1.11, 2.0, 2.1 
"""

# Keep this empty
SCRIPT_NAME = ''

class PassengerPathInfoFix(object):
    """
    Sets PATH_INFO from REQUEST_URI since Passenger doesn't provide it.
    """
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        from urllib.parse import unquote
        environ['SCRIPT_NAME'] = SCRIPT_NAME

        request_uri = unquote(environ['REQUEST_URI'])
        script_name = unquote(environ.get('SCRIPT_NAME', ''))
        offset = request_uri.startswith(script_name) and len(environ['SCRIPT_NAME']) or 0
        environ['PATH_INFO'] = request_uri[offset:].split('?', 1)[0]
        return self.app(environ, start_response)

      
# projectname is the name of the main folder containing wsgi.py and setting.py
import buzzca.wsgi
application = buzzca.wsgi.application
application = PassengerPathInfoFix(application)
