from .GenericUser import GenericUser;
from django.db import models 

class NormalUser(models.Model):
    user = models.OneToOneField( GenericUser, on_delete=models.CASCADE, primary_key=True,null = False)
    birthday = models.DateField(blank=False)
    def __str__(self):
        return str(self.user)
    class Meta:
        app_label = 'api'

    def save(self, *args, **kwargs):
        for field in self._meta.fields:
            if isinstance(field, (models.CharField, models.TextField)) and field.name != "password":
                value = getattr(self, field.name, None)
                if value != None and len(value) < 1: 
                    raise ValueError(f"{field.name} : {value} must have more than 5 characters")
        super().save(*args, **kwargs)


