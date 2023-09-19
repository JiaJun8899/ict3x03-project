from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
import uuid

class GenericUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    USER_TYPE_CHOICES = (
        ('normal', 'Normal'),
        ('admin', 'Admin'),
        ('org', 'Organizer'),
    )
    phone_regex = RegexValidator(
    regex=r'^\d{8}$', 
    message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
)

    auth = models.CharField(choices=USER_TYPE_CHOICES, max_length=20,blank=False)
    phone = models.CharField(max_length=8, null=False,blank=False,validators=[phone_regex])
    nric = models.CharField(max_length=15, null=False, blank=False)

    class Meta:
        app_label = "api"

    def __str__(self):
        return (self.first_name) + str(self.last_name)
 
    def save(self, *args, **kwargs):
        for field in self._meta.fields:
            if isinstance(field, (models.CharField, models.TextField)) and field.name != "password":
                value = getattr(self, field.name, None)
                if value != None and len(value) < 1: 
                    return False
        super().save(*args, **kwargs)
        return True
