from django.db import models
import uuid


class EventOrganizerMapping(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey("Event", on_delete=models.CASCADE)
    organizer = models.ForeignKey("Organizer", on_delete=models.CASCADE)
    approval = models.BooleanField(default=False,blank=False)

    def __str__(self):
        return f"{str(self.organizer)} - {str(self.event)}"
    
    class Meta:
        unique_together = (('event', 'organizer'),)
        app_label = 'api'

