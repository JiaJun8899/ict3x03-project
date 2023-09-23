from .GenericUser import GenericUser;
from django.db import models
from api.managers import AdminManager

class Admin(models.Model):
    user = models.OneToOneField( GenericUser, on_delete=models.CASCADE, primary_key=True)
    adminManager = AdminManager()

    def __str__(self):
        return str(self.user.first_name + self.user.last_name)

    class Meta:
        app_label = 'api'

