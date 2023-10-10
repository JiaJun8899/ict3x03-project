from django.db import models
import uuid
from django.core.validators import MinLengthValidator
from api.managers import EventMapperManager

class EventOrganizerMapping(models.Model):
    eventMapperManager = EventMapperManager() 
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey("Event", on_delete=models.CASCADE)
    organizer = models.ForeignKey("Organizer", on_delete=models.CASCADE)
    ApprovalChoices= (
        ('pending', 'Pending'),
        ('reject', 'Rejected'),
        ('accepted', 'Accepted'),
    )
    approval = models.CharField(max_length=12, default='pending',choices=ApprovalChoices, validators=[MinLengthValidator(2)])

    def __str__(self):
        return f"{str(self.organizer)} - {str(self.event)}"
    
    class Meta:
        unique_together = (('event', 'organizer'))
        app_label = 'api'
