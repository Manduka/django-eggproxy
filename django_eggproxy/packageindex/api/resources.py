from tastypie import fields
from tastypie.resources import ModelResource, Resource
from tastypie.authorization import DjangoAuthorization, Authorization
from tastypie.constants import ALL, ALL_WITH_RELATIONS

from packageindex.models import PackageIndex, Package, Application

from authorization import Authentication

from django.core.files.storage import default_storage
from django.conf import settings

import boto
import urlparse

ACCESS_KEY_NAME     = getattr(settings, 'AWS_ACCESS_KEY_ID', None)
SECRET_KEY_NAME     = getattr(settings, 'AWS_SECRET_ACCESS_KEY', None)
STORAGE_BUCKET_NAME = getattr(settings, 'AWS_STORAGE_BUCKET_NAME', None)


class S3UploadResource(Resource):
    path = fields.CharField()
    expires_in = fields.IntegerField(default=60)
    public = fields.BooleanField(default=True)
    
    def get_object_list(self, request):
        return []
    
    def obj_get_list(self, request=None, **kwargs):
        return []
    
    def dehydrate(self, bundle):
        if bundle.obj:
            bundle.data.update(bundle.obj)
        return bundle
    
    def obj_create(self, bundle, request=None, **kwargs):
        connection = boto.connect_s3(ACCESS_KEY_NAME, SECRET_KEY_NAME)
        bucket = connection.get_bucket(STORAGE_BUCKET_NAME)
        key_name = bundle.data['path']
        #TODO rename path if the file already exists
        expires_in = bundle.data.get('expires_in', 60)
        key = bucket.new_key(key_name)
        if bundle.data.get('public'):
            key.set_acl('public-read')
        url = key.generate_url(expires_in, method='PUT', headers={'content-type':'multipart/form-data'})
        response = {'upload_url':url,
                    'expires_in':expires_in,
                    'url':url.split('?', 1)[0],}
        bundle.obj = response
        return bundle
    
    def get_resource_uri(self, bundle_or_obj):
        if isinstance(bundle_or_obj, dict):
            url = bundle_or_obj['url']
        else:
            url = bundle_or_obj.obj['url']
        result = urlparse.urlparse(url)
        return result.path
    
    class Meta:
        resource_name = 's3upload'
        authorization = Authorization()
        authentication = Authentication()
        object_class = dict
        always_return_data = True

class PackageIndexResource(ModelResource):
    class Meta:
        queryset = PackageIndex.objects.all()
        authorization = DjangoAuthorization()
        authentication = Authentication()
        filtering = {'name':ALL}

class ApplicationResource(ModelResource):
    class Meta:
        queryset = Application.objects.all()
        authorization = DjangoAuthorization()
        authentication = Authentication()
        filtering = {'name':ALL}

class PackageResource(ModelResource):
    application = fields.ForeignKey(ApplicationResource, 'application')
    package_index = fields.ForeignKey(PackageIndexResource, 'package_index')

    class Meta:
        queryset = Package.objects.all()
        authorization = DjangoAuthorization()
        authentication = Authentication()
        filtering = {'application':ALL_WITH_RELATIONS,
                     'package_index':ALL_WITH_RELATIONS,}

