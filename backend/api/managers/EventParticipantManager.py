from .GenericInfoManager import GenericInfoManager

class EventParticipantManager(GenericInfoManager):
    def getParticipantsByEventUUID(self, eid):
        try:
            particpantsMap = self.getAllRecords().filter(event_id=eid)
            return particpantsMap
        except Exception:
            return None
    
    def deleteByUUID(self, uuid):
        return self.filter(participant_id=uuid).delete()
    
    def getSingleUserEventmap(self,eid,pid):
        try:
            userEventMap = self.getAllRecords().filter(event_id=eid, participant_id=pid)
            return userEventMap
        except Exception:
            return None
