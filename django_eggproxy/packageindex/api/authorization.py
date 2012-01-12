from tastypie.authentication import ApiKeyAuthentication, BasicAuthentication
from tastypie.http import HttpUnauthorized

class Authentication(ApiKeyAuthentication):
    def __init__(self):
        self.api_key_auth = ApiKeyAuthentication()
        self.basic_auth = BasicAuthentication(backend=ApiKeyBackend())
    
    def is_authenticated(self, request, **kwargs):
        if request.user.is_authenticated():
            return True
        ret = self.basic_auth.is_authenticated(request, **kwargs)
        if isinstance(ret, HttpUnauthorized):
            ret2 = self.api_key_auth.is_authenticated(request, **kwargs)
            if not isinstance(ret2, HttpUnauthorized):
                return ret2
        return ret
    
    def get_identifier(self, request):
        if request.user.is_authenticated():
            return request.user.username
        ret = self.basic_auth.get_identifier(request)
        if isinstance(ret, HttpUnauthorized):
            ret2 = self.api_key_auth.get_identifier(request)
            if not isinstance(ret2, HttpUnauthorized):
                return ret2
        return ret

class ApiKeyBackend(object):
    def authenticate(self, username, password):
        from tastypie.models import ApiKey
        
        try:
            key = ApiKey.objects.get(user__username=username, key=password)
        except ApiKey.DoesNotExist:
            return None
        
        return key.user
