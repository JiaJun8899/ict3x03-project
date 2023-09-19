from django.db import models
import uuid

class NOK(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fname = models.CharField(max_length=100,blank=False)
    lname = models.CharField(max_length=100,blank=False)
    relationship = models.CharField(max_length=50,blank=False)
    phone = models.CharField(max_length=15,blank=False)
    email = models.EmailField(blank=False)
    age= models.CharField(max_length=15, blank=False, default="15")
    # One-to-One relationship with NormalUser

    def __str__(self):
        return self.fname

    class Meta:
        app_label = 'api'

    def save(self, *args, **kwargs):
        for field in self._meta.fields:
            if isinstance(field, (models.CharField, models.TextField)) and field.name != "password":
                value = getattr(self, field.name, None)
                if value != None and len(value) < 1: 
                    raise ValueError(f"{field.name} : {value} must have more than 5 characters")
        super().save(*args, **kwargs)


