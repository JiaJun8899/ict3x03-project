from .GenericInfoManager import GenericInfoManager

class OrganizerManager(GenericInfoManager):
    def updateOrganization(self, uuid, status):
        organization = self.getByUUID(uuid)
        organization.validOrganisation = status
        organization.save()
        return True

