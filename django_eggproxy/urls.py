# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
from django.views.generic.base import RedirectView

admin.autodiscover()

import patch_auth_admin

urlpatterns = patterns('',
    (r'^packageindex/', include('packageindex.urls')),
    url(r'', include("djangopypi.urls")),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    if '://' not in settings.STATIC_URL:
        from django.contrib.staticfiles.urls import staticfiles_urlpatterns
        urlpatterns += staticfiles_urlpatterns()

if hasattr(settings, 'AWS_STORAGE_BUCKET_NAME'):
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', RedirectView.as_view(url='http://%s.s3.amazonaws.com/' % settings.AWS_STORAGE_BUCKET_NAME + '%(paths)s')),
    )
else:
    urlpatterns += patterns('django.views',
        (r'^media/(?P<path>.*)$', 'static.serve', {'document_root': settings.MEDIA_ROOT}),
    )

