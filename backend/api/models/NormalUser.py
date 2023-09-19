from .GenericUser import GenericUser;
from django.db import models 

class NormalUser(models.Model):
    user = models.OneToOneField( GenericUser, on_delete=models.CASCADE, primary_key=True,null = False)
    birthday = models.DateField(blank=False)
    def __str__(self):
        return str(self.user)
    class Meta:
        app_label = 'api'
