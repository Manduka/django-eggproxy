
def register_api(api):
    from resources import PackageIndexResource, ApplicationResource, PackageResource, S3UploadResource
    api.register(PackageIndexResource(), canonical=True)
    api.register(ApplicationResource(), canonical=True)
    api.register(PackageResource(), canonical=True)
    api.register(S3UploadResource(), canonical=False)

