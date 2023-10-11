from django.contrib.auth.models import BaseUserManager
from .GenericInfoManager import GenericInfoManager

class GenericUserManager(BaseUserManager, GenericInfoManager):
        pass
