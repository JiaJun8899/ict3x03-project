from django.db import models
import uuid
from django.core.validators import MinLengthValidator

class NOK(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100,blank=False,validators=[MinLengthValidator(2)])
    relationship = models.CharField(max_length=50,blank=False,validators=[MinLengthValidator(2)])
    phoneNum = models.CharField(max_length=8, null=False,blank=False,validators=[MinLengthValidator(8)])

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'api'

