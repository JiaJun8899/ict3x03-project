from django.db import models
import uuid
from api.managers import EventParticipantManager
class EventParticipant(models.Model):
    eventParticipantManager = EventParticipantManager()
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey("Event", on_delete=models.CASCADE)
    participant = models.ForeignKey("NormalUser", on_delete=models.CASCADE)
    
    class Meta:
        unique_together = (('event', 'participant'),)

    def __str__(self):
        return str(self.event) + str(self.participant)



