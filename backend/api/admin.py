from django.contrib import admin
from django_otp.plugins.otp_email.models import EmailDevice
from requests.api import delete
from api.models import Admin, Organizer,NormalUser,GenericUser,Event,EventOrganizerMapping,EventParticipant
from django.contrib.auth.models import Group
# Register your models here.
from django_otp.admin import OTPAdminSite
admin.site.__class__ = OTPAdminSite
from django.contrib import admin
from api.models import Admin, Organizer, NormalUser, GenericUser, Event, EventOrganizerMapping, EventParticipant
from django.contrib.auth.models import Group
from django_otp.admin import OTPAdminSite
import logging
from api.views import get_client_ip_address
from django.contrib.admin.models import LogEntry

admin.site.__class__ = OTPAdminSite

class BaseAdmin(admin.ModelAdmin):
    # Deny add permission by default
    def has_add_permission(self, request, obj=None):
        return False
    # Deny change permission by default
    def has_change_permission(self, request, obj=None):
        return False
    # Deny delete permission by default
    def has_delete_permission(self, request, obj=None):
        return True

    #LYN DO HERE
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

    #LYN DO HERE FIGURE OUT WHAT IS CHANGED
    def delete_model(self, request, obj):
        super().delete_model(request, obj)

@admin.register(Organizer)

class OrganizerAdmin(BaseAdmin):
    # Deny delete permission by default
    readonly_fields = ["user"]

    def has_change_permission(self, request, obj=None):
        return True

    def save_model(self, request, obj, form, change):
        if hasattr(obj, 'user') and isinstance(obj.user, GenericUser):
            obj.user.is_active = obj.validOrganisation 
            obj.user.save()
        super().save_model(request, obj, form, change)

@admin.register(NormalUser)
class GenericUserAdmin(BaseAdmin):
    exclude = ["password"]

@admin.register(Admin)
class AdminAdmin(BaseAdmin):
    pass

@admin.register(Event)
class EventAdmin(BaseAdmin):
    pass

@admin.register(EventParticipant)
class EventParticipantAdmin(BaseAdmin):
    pass

@admin.register(EventOrganizerMapping)
class EventOrganizerMappingAdmin(BaseAdmin):
    readonly_fields = ["event", "organizer"]

    def has_change_permission(self, request, obj=None):
        return True
admin.site.unregister(EmailDevice)
admin.site.unregister(Group)

@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'action_time'

    list_filter = [
        'user',
        'content_type',
        'action_flag'
    ]

    search_fields = [
        'object_repr',
        'change_message'
    ]

    list_display = [
        'action_time',
        'user',
        'content_type',
        'action_flag',
    ]

    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser
