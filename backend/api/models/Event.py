import uuid
from django.db import models
from django.core.validators import MinLengthValidator
from api.managers import EventManager
from django.core.exceptions import ValidationError

class Event(models.Model):
    eventManager = EventManager() 
    eid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('over', 'Over'),
    )
    eventName = models.CharField(max_length=64, blank=False,validators=[MinLengthValidator(2)])
    startDate= models.DateTimeField(blank=False)
    endDate= models.DateTimeField(blank=False)
    eventImage = models.ImageField(blank = True, upload_to='events/')
    eventStatus = models.CharField(choices=STATUS_CHOICES, max_length=10,blank=False,validators=[MinLengthValidator(2)], default="open")
    noVol = models.IntegerField(default=0, verbose_name="Number of Volunteers",blank=False)
    eventDesc = models.TextField(blank=False,validators=[MinLengthValidator(2)], max_length=255)
    
    class Meta:
        app_label = 'api'

    def __str__(self):
        return self.eventName