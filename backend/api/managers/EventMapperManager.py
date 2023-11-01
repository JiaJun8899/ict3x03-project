from .GenericInfoManager import GenericInfoManager

class EventMapperManager(GenericInfoManager):
    def setApproval(self, uuid, status):
        try:
            eventMap = self.getByUUID(uuid)
            eventMap.approval = status
            eventMap.save()
        except Exception as e:
            return None
    
    def getMapByEventUUID(self, eid):
        try:
            eventMap = self.get(event_id = eid)
            return eventMap
        except Exception:
            return None
    
    def getMapByOrganizationUUID(self, organizer_id):
        try:
            eventMap = self.get(organizer_id= organizer_id)
            return eventMap
        except Exception:
            return None
    
    def getMapByOrgEventUUID(self, organizer_id, eid):
        try:
            eventMap = self.get(organizer_id= organizer_id, event_id=eid)
            return eventMap
        except Exception:
            return None