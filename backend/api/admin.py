from django.contrib import admin
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

admin.site.__class__ = OTPAdminSite

#LYN CHANGE THIS
logger = logging.getLogger('django')

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
        if change:  # if object is being changed
            logger.info(f'LYNN LOGS -> User {request.user} changed object {obj}.')
        else:  # if object is being added
            logger.info(f'LYNN LOGS -> User {request.user} added object {obj}.')
        super().save_model(request, obj, form, change)

    #LYN DO HERE FIGURE OUT WHAT IS CHANGED
    def delete_model(self, request, obj):
        logger.info(f'LYNN LOGS -> User {request.user} deleted object {obj}.')
        logger.info(f'User {request.user} deleted object {obj}.')
        super().delete_model(request, obj)

@admin.register(Organizer)

class OrganizerAdmin(BaseAdmin):
    # Deny delete permission by default
    readonly_fields = ["user"]

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
