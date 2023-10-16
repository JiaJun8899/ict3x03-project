from django.contrib import admin
from api.models import Admin, Organizer,NormalUser,GenericUser
from django.contrib.auth.models import Group
from django import forms
# Register your models here.
from django_otp.admin import OTPAdminSite, OTPAdminAuthenticationForm

class CustomOTPAdminAuthenticationForm(OTPAdminAuthenticationForm):
    DEVICE_CHOICES = [
        ('otp_email.emaildevice/43', 'otp_email.emaildevice/43'),
        # ... add other choices as needed
    ]

    otp_device = forms.ChoiceField(
        required=False, 
        choices=DEVICE_CHOICES, 
        widget=forms.Select(attrs={'class': 'hidden'})
    )

class CustomAdminSite(OTPAdminSite):
    name = 'Admin'
    login_form = CustomOTPAdminAuthenticationForm

admin.site.__class__ = CustomAdminSite
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
