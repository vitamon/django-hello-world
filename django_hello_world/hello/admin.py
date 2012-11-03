from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from hello.models import UserProfile, CreationLog
from requests.models import RequestsLog, RequestsPriority

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'profiles'


class ProfileAdmin(UserAdmin):
    inlines = (UserProfileInline, )


class RequestsLogAdmin(ModelAdmin):
    list_display = ('url', 'time')


class RequestsPriorityAdmin(ModelAdmin):
    list_display = ('url', 'priority')
    verbose_name_plural = 'priorities'


class CreationLogAdmin(ModelAdmin):
    list_display = ('class_name', 'operation', 'time')

admin.site.unregister(User)
admin.site.register(User, ProfileAdmin)
admin.site.register(RequestsLog, RequestsLogAdmin)
admin.site.register(RequestsPriority, RequestsPriorityAdmin)
admin.site.register(CreationLog, CreationLogAdmin)
