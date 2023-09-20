from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
import uuid
""" from .managers import GenericUserManager """


class GenericUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nricRegex =RegexValidator(
        regex=r'^[A-Za-z]\d{8}[A-Za-z]$',
        message="NRIC must start with an alphabet character, followed by 8 digits, and ending with an alphabet character."
    ) 

    phone = models.IntegerField(max_length=8, null=False,blank=False,validators=[nricRegex])
    nric = models.CharField(max_length=9, null=False, blank=False)
    """ userManager = GenericUserManager() """
    class Meta:
        app_label = "api"

    def __str__(self):
        return (self.first_name) + str(self.last_name)
 
    def save(self, *args, **kwargs):
        for field in self._meta.fields:
            if isinstance(field, (models.CharField, models.TextField)) and field.name != "password":
                value = getattr(self, field.name, None)
                if value != None and len(value) < 1: 
                    raise ValueError(f"{field.name} : {value} must have more than 5 characters")
        super().save(*args, **kwargs)

