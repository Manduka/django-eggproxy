from django.conf.urls.defaults import *

from tastypie.api import Api
from api import register_api

v1_api = Api(api_name='v1')
register_api(v1_api)

urlpatterns = patterns('packageindex.views',
    url(r'^api/', include(v1_api.urls)),
    url(r'^p/$', 'application_list', name='packageindex.application_list'),
    url(r'^p/(?P<name>[\.\w\d-]+)/$', 'application_detail', name='packageindex.application_detail'),
    url(r'^p/(?P<name>[\.\w\d-]+)/(?P<title>[\.\w\d-]+)', 'download_package', name='packageindex.download_package'),
    
    url(r'^(?P<access_key>[\w\d]+)/$', 'application_list', name='packageindex.keyed_application_list'),
    url(r'^(?P<access_key>[\w\d]+)/download/(?P<package_id>\d+)/$', 'direct_download_package', name='packageindex.direct_download_package'),
    url(r'^(?P<access_key>[\w\d]+)/(?P<name>[\.\w\d-]+)/$', 'application_detail', name='packageindex.keyed_application_detail'),
    url(r'^(?P<access_key>[\w\d]+)/(?P<name>[\.\w\d-]+)/(?P<title>[\.\w\d-]+)', 'download_package', name='packageindex.keyed_download_package'),
)

