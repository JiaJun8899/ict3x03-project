from django.db import models

class GenericInfoManager(models.Manager):
    def getAllRecords(self):
        return self.all()

    def getByUUID(self, uuid):
        return self.filter(pk=uuid).first()

    def deleteByUUID(self, uuid):
        return self.filter(pk=uuid).delete()
