

from django.contrib.auth import logout
from django.contrib import messages
import datetime

from django.conf import settings

from django.utils.deprecation import MiddlewareMixin

class SessionIdleTimeout(MiddlewareMixin):
    def __init__(self, get_response):
        super().__init__(get_response)
        
    def process_view(self, request, response, a, b):
        # if request.user.is_authenticated:
        #     current_datetime = datetime.datetime.now()
        #     # Timeout if idle time period is exceeded.
            
        #     if request.session.has_key('last_activity') and (current_datetime - datetime.datetime.fromtimestamp(request.session['last_activity'])).seconds > settings.SESSION_IDLE_TIMEOUT:
        #         logout(request)
        #         print(request.session['last_activity'])
        #         # logout(request)
        #         # messages.add_message(request, messages.ERROR, 'Your session has been timed out.')
        #     # Set last activity time in current session.
        #     else:
        #         print((current_datetime - datetime.datetime.fromtimestamp(request.session['last_activity'])).seconds)
        #         request.session['last_activity'] = current_datetime.timestamp()

        return None
