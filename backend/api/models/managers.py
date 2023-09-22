from django.db import models

class GenericGetInformation(models.Manager):
    def getAll(self):
        return self.all()

    def getByUuid(self, uuid):
        return self.filter(pk=uuid).first()

    def deleteById(self, uuid):
        return self.filter(pk=uuid).delete()

class GenericUserManager(GenericGetInformation):
    pass

class NormalUserManager(GenericGetInformation):
    pass

class AdminManager(GenericGetInformation):
    pass

class EventManager(GenericGetInformation):
    def setApproval(self, uuid, status):
        try:
            event = self.getByUuid(uuid)
            event.approval = status
            event.save()
        except Exception as e:
            print(e)

class OrganiserManager(GenericUserManager):
    def updateOrganization(self, uuid, status):
        organization = self.getByUuid(uuid)
        organization.validOrganisation = status
        organization.save()
        return True

