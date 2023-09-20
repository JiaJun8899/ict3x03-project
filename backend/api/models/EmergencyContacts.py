from django.db import models
import uuid

class EmergencyContacts(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    normalUser = models.ForeignKey("NormalUser", on_delete=models.CASCADE)
    nok = models.ForeignKey("NOK", on_delete=models.CASCADE)
        
    class Meta:
        unique_together = (('normalUser'),)

    def __str__(self):
        return str(self.normalUser) + " : "  + str(self.nok)

    def save(self, *args, **kwargs):
        for field in self._meta.fields:
            if isinstance(field, (models.CharField, models.TextField)) and field.name != "password":
                value = getattr(self, field.name, None)
                if value != None and len(value) < 1: 
                    raise ValueError(f"{field.name} : {value} must have more than 5 characters")
        super().save(*args, **kwargs)


