from celery.task import task

from packageindex.models import PackageIndex, Package

@task
def refresh_package_indexes():
    PackageIndex.objects.refresh_stale_indexes()
    Package.objects.populate_pending_downloads()
