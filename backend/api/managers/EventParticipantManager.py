from .GenericInfoManager import GenericInfoManager

class EventParticipantManager(GenericInfoManager):
    def getParticipantsByEventUUID(self, eid):
        try:
            particpantsMap = self.getAllRecords().filter(event_id=eid)
            return particpantsMap
        except Exception:
            return None