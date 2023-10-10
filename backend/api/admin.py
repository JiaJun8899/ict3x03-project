from django.contrib import admin
from api.models import Admin, Organizer,NormalUser,GenericUser
# Register your models here.

admin.site.register(Admin)
admin.site.register(Organizer)
admin.site.register(NormalUser)
admin.site.register(GenericUser)
