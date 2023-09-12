from .user import GenericUser;
from django.db import models
class Admin(models.Model):
    user = models.OneToOneField( GenericUser, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return str(self.user.first_name)
    class Meta:
        app_label = 'api'
