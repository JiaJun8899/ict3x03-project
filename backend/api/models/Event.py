import uuid
from django.db import models

class Event(models.Model):
    eid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('over', 'Over'),
    )
    eventName = models.CharField(max_length=64, blank=False)
    startDate= models.DateTimeField(blank=False)
    endDate= models.DateTimeField(blank=False)
    eventImage = models.ImageField(upload_to='events/')
    eventStatus = models.CharField(choices=STATUS_CHOICES, max_length=10,blank=False)
    noVol = models.IntegerField(default=0, verbose_name="Number of Volunteers",blank=False)
    eventDesc = models.TextField(blank=False)
    
    class Meta:
        app_label = 'api'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        for field in self._meta.fields:
            if isinstance(field, (models.CharField, models.TextField)) and field.name != "password":
                value = getattr(self, field.name, None)
                if value != None and len(value) < 1: 
                    raise ValueError(f"{field.name} : {value} must have more than 5 characters")
        super().save(*args, **kwargs)


