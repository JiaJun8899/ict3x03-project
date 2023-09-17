from .user import GenericUser;
from django.db import models 

class NormalUser(models.Model):
    user = models.OneToOneField( GenericUser, on_delete=models.CASCADE)
    birthday = models.DateField(null=True)
    def __str__(self):
        return str(self.user.first_name)
    class Meta:
        app_label = 'api'
