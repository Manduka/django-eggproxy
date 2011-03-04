from django.contrib import admin

from models import ManagedApplication, Release

class ManagedApplicationAdmin(admin.ModelAdmin):
    raw_id_fields = ['application']
admin.site.register(ManagedApplication, ManagedApplicationAdmin)

class ReleaseAdmin(admin.ModelAdmin):
    list_display = ['title', 'version', 'released']
    raw_id_fields = ['package', 'application']
    actions = ['build_package']
    
    def build_package(self, request, queryset):
        for release in queryset.filter(package__isnull=True):
            release.build_package()

admin.site.register(Release, ReleaseAdmin)


