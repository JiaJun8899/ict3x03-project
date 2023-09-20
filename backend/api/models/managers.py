# managers.py (can be in the same file as your models or a separate one)
from django.db import models

class GenericGetInformation(models.Manager):
    def get_all(self):
        return self.all()

    def get_by_uuid(self,uuid):
        return self.filter(id=uuid).first()


class GenericUserManager(models.Manager):
    def get_admin_users(self):
        return self.filter(auth='admin')

    def get_normal_users(self):
        return self.filter(auth='normal')

    def get_org_users(self):
        return self.filter(auth='org')

    def get_all_users(self):
        return self.all()
    
    def delete_by_id(self,uuid):
        return self.filter(id=uuid).delete()

class EventManager(GenericGetInformation):
    def setApproval(self,uuid,status):
        try:
            event = self.get_by_uuid(uuid)
            event.approval = status
            event.save()
        except Exception as e:
            print(e)

