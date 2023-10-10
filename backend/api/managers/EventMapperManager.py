from .GenericInfoManager import GenericInfoManager

class EventMapperManager(GenericInfoManager):
    def setApproval(self, uuid, status):
        try:
            eventMap = self.getByUUID(uuid)
            eventMap.approval = status
            eventMap.save()
        except Exception as e:
            print(e)
    
    def getMapByEventUUID(self, eid):
        try:
            eventMap = self.get(event_id = eid)
            return eventMap
        except Exception:
            return None