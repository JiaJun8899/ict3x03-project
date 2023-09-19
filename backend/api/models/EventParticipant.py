from django.db import models
import uuid
class EventParticipant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey("Event", on_delete=models.CASCADE)
    participant = models.ForeignKey("NormalUser", on_delete=models.CASCADE)
    
    class Meta:
        unique_together = (('event', 'participant'),)

    def __str__(self):
        return str(event) + str(participant)

    def save(self, *args, **kwargs):
        for field in self._meta.fields:
            if isinstance(field, (models.CharField, models.TextField)) and field.name != "password":
                value = getattr(self, field.name, None)
                if value != None and len(value) < 1: 
                    raise ValueError(f"{field.name} : {value} must have more than 5 characters")
        super().save(*args, **kwargs)


