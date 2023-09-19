from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class GenericUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    USER_TYPE_CHOICES = (
        ('normal', 'Normal'),
        ('admin', 'Admin'),
        ('org', 'Organizer'),
    )
    auth = models.CharField(choices=USER_TYPE_CHOICES, max_length=20,blank=False)
    phone = models.CharField(max_length=8, null=False,blank=False)
    nric = models.CharField(max_length=15, null=False, blank=False)

    class Meta:
        app_label = "api"

    def __str__(self):
        return (self.first_name) + str(self.last_name)
