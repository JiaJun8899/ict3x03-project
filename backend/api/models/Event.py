import uuid
from django.db import models

class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('over', 'Over'),
    )
    name = models.CharField(max_length=64, blank=False)
    startDatetime = models.DateTimeField(blank=False)
    endDatetime = models.DateTimeField(blank=False)
    image = models.ImageField(upload_to='events/')
    status = models.CharField(choices=STATUS_CHOICES, max_length=10,blank=False)
    participant_limit = models.IntegerField(blank=False)
    numberOfVolunteers = models.IntegerField(default=0, verbose_name="Number of Volunteers",blank=False)
    approval = models.BooleanField(default=False,blank=False)
    description = models.TextField(blank=False)
    
    class Meta:
        app_label = 'api'

    def __str__(self):
        return self.name
