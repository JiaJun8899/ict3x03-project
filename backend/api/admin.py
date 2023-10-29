from django.contrib.admin.models import LogEntry
from django.contrib import admin
from api.models import Admin, Organizer,NormalUser,GenericUser,Event,EventOrganizerMapping,EventParticipant
from django.contrib.auth.models import Group
# Register your models here.
from django_otp.admin import OTPAdminSite
admin.site.__class__ = OTPAdminSite
from django.contrib import admin
from api.models import Admin, Organizer, NormalUser, GenericUser, Event, EventOrganizerMapping, EventParticipant
from django.contrib.auth.models import Group
from django_otp.admin import OTPAdminSite

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
        return False

@admin.register(Organizer)

class OrganizerAdmin(BaseAdmin):
    # Deny delete permission by default
    readonly_fields = ["user"]

    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

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
""" admin.site.unregister """
admin.site.unregister(Group)
admin.site.register(LogEntry)
