from django.db import models
import uuid

class NOK(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    relationship = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    age= models.CharField(max_length=15, blank=True, default="15")
    # One-to-One relationship with NormalUser

    def __str__(self):
        return self.fname

    class Meta:
        app_label = 'api'

