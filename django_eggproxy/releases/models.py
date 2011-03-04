import os
import tempfile
import shutil

from django.db import models
from django.core.files import File

from packageindex.models import PackageIndex, Application, Package

REPOSITORY_TYPES = [
    ('git', 'Git'),
]

def run_cmd(cmd):
    print cmd
    return os.popen(cmd).read()

class ManagedApplication(models.Model):
    application = models.ForeignKey(Application)
    package_index = models.ForeignKey(PackageIndex)
    repository_type = models.CharField(max_length=10, choices=REPOSITORY_TYPES)
    repository_url = models.CharField(max_length=512)
    
    def __unicode__(self):
        return u'%s - %s' % (self.application, self.package_index)

class ReleaseManager(models.Manager):
    def pending_releases(self):
        return self.filter(package__isnull=True)
    
    def generate_releases(self):
        for release in self.pending_releases():
            release.build_package()

class Release(models.Model):
    title = models.CharField(max_length=100)
    version = models.CharField(max_length=20, blank=True)
    application = models.ForeignKey(ManagedApplication)
    repository_version = models.CharField(max_length=128)
    package = models.ForeignKey(Package, null=True, blank=True)
    
    objects = ReleaseManager()
    
    def __unicode__(self):
        return self.title
    
    def released(self):
        return bool(self.package)
    
    def build_package(self):
        package = Package(title=self.title,
                          version=self.version,
                          application=self.application.application,
                          package_index=self.application.package_index,
                          active=True,)
        repo_dir = self._checkout()
        package_path = self._build_dist(repo_dir)
        assert package_path
        package_file = File(open(package_path, 'rb'))
        package.download.save(os.path.split(package_path)[-1], package_file)
        shutil.rmtree(repo_dir, ignore_errors=True)
        self.package = package
        self.save()
    
    def _checkout(self):
        dest = tempfile.mkdtemp(prefix='tmprelease')
        run_cmd('git clone %s %s' % (self.application.repository_url, dest))
        run_cmd('cd %s && git checkout %s' % (dest, self.repository_version))
        return dest
    
    def _build_dist(self, dest):
        run_cmd('cd %s && python setup.py sdist --formats=gztar' % dest)
        dist_dir = os.path.join(dest, 'dist')
        for name in os.listdir(dist_dir):
            path = os.path.join(dist_dir, name)
            if os.path.isfile(path) and path.endswith('.tar.gz'):
                return path

