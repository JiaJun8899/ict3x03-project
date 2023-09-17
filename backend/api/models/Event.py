import uuid
from django.db import models

class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('over', 'Over'),
    )
    name = models.CharField(max_length=64)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    image = models.ImageField(upload_to='events/')
    status = models.CharField(choices=STATUS_CHOICES, max_length=10)
    participant_limit = models.IntegerField()
    numberOfVolunteers = models.IntegerField(default=0, verbose_name="Number of Volunteers")
    approval = models.BooleanField(default=False)
    description = models.TextField()
    
    class Meta:
        app_label = 'api'

    def __str__(self):
        return self.name
