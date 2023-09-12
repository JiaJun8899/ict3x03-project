from django.db import models
import uuid

class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('closed', 'Closed'),
    )
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    organizer = models.ForeignKey("Organizer", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='events/')
    status = models.CharField(choices=STATUS_CHOICES, max_length=10)
    participant_limit = models.IntegerField()
    approval = models.BooleanField(default=False)
    description = models.TextField()
    
    class Meta:
        app_label = 'api'
