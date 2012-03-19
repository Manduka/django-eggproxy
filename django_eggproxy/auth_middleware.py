import base64

from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login

# Provides the HttpBasicAuthenticator to perform HTTP basic authentication.

class HttpResponseUnauthorized(HttpResponse):
    status_code = 401

    def __init__(self):
        super(HttpResponseUnauthorized, self).__init__('Authorization Required')

# Uses the HttpBasicAuthenticator to enforce HTTP basic authentication for
# an entire application.

SAFE_URLS = (getattr(settings, 'LOGIN_URL', '/accounts/login/'), '/health-check/', '/500/', '/404/', '/packageindex/')

class HttpBasicMiddleware(object):
    def process_request(self, request):
        if request.user.is_authenticated():
            return
        auth = request.META.get('HTTP_AUTHORIZATION')
        if auth:
            auth = auth.split()
            if len(auth) == 2 and auth[0].lower() == 'basic':
                username, password = base64.b64decode(auth[1]).split(':')
                user = authenticate(username=username, password=password)
                if user is not None and user.is_active:
                    login(request, user)
                    return
        for url in SAFE_URLS:
            if request.path.startswith(url):
                return
        response = HttpResponseUnauthorized()
        realm = 'siteauth'
        response['WWW-Authenticate'] = 'Basic realm="%s"' % realm
        return response


class RequireLoginMiddleware(object):
    def __init__(self):
        self.require_login_path = getattr(settings, 'LOGIN_URL', '/accounts/login/')
    
    def process_request(self, request):
        for url in SAFE_URLS:
            if request.path.startswith(url):
                return
        if (request.user.is_anonymous()):
            return HttpResponseRedirect('%s?next=%s' % (self.require_login_path, request.path))
