from django.contrib.auth.admin import UserAdmin, User
from tastypie.admin import ApiKeyInline

from django.contrib import admin

UserAdmin.inlines += [ApiKeyInline]
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
