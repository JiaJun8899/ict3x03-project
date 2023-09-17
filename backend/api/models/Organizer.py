from django.contrib.auth.models import Permission
from django.db import models
from .GenericUser import GenericUser

class Organizer(models.Model):

    user = models.OneToOneField( GenericUser, on_delete=models.CASCADE, primary_key=True)
    isApproved = models.BooleanField(default=False)
    def __str__(self):
        return str(self.user)
    class Meta:
        app_label = 'api'
