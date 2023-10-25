from django.contrib import admin
from api.models import Admin, Organizer,NormalUser,GenericUser,Event,EventOrganizerMapping,EventParticipant
from django.contrib.auth.models import Group
# Register your models here.
from django_otp.admin import OTPAdminSite
admin.site.__class__ = OTPAdminSite

@admin.register(Organizer)
class OrganizerAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False


@admin.register(GenericUser)
class GenericUserAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    exclude = ["password"]

@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    pass

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass

@admin.register(EventParticipant)
class EventParticipantAdmin(admin.ModelAdmin):
    pass
@admin.register(EventOrganizerMapping)
class EventOrganizerMappingAdmin(admin.ModelAdmin):
    pass
admin.site.unregister(Group)
