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

