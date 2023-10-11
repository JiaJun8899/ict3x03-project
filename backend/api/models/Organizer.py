from django.db import models
from .GenericUser import GenericUser
from api.managers import OrganizerManager

class Organizer(models.Model):
    user = models.OneToOneField(GenericUser, on_delete=models.CASCADE, primary_key=True,null = False)
    validOrganisation = models.BooleanField(default=False)
    organizerManager = OrganizerManager()

    def __str__(self):
        return str(self.user)
    class Meta:
        app_label = 'api'
