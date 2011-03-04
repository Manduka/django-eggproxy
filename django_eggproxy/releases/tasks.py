from celery.task import task

from releases.models import Release

@task
def generate_releases():
    Release.objects.generate_releases()
