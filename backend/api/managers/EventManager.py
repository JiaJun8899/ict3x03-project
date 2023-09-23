from .GenericInfoManager import GenericInfoManager

class EventManager(GenericInfoManager):
    def setApproval(self, uuid, status):
        try:
            event = self.getByUUID(uuid)
            event.approval = status
            event.save()
        except Exception as e:
            print(e)

