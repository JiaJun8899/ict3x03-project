from django.contrib import admin
from api.models import Admin, Organizer,NormalUser,GenericUser
from django.contrib.auth.models import Group
# Register your models here.


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

admin.site.unregister(Group)
