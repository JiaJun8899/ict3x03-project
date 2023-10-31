from django.contrib.auth.models import BaseUserManager
from .GenericInfoManager import GenericInfoManager

class GenericUserManager(BaseUserManager, GenericInfoManager):
    def getUserByEmail(self,email):
        try:
            obj =self.get(email=email)
        except self.model.DoesNotExist:
            obj = None
        return obj
