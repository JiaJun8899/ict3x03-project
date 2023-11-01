from sre_compile import FAILURE
from sre_constants import SUCCESS
from api.models import Event
from api.serializer import EventSerializer

class EventCommonService:
    def __init__(self):
        pass

    @staticmethod
    def getAllEvents():
        try:
            events = Event.eventManager.getAllRecords()
            serializer = EventSerializer(events, many=True)
            return serializer.data
        except Exception as e:
            return None
        
    @staticmethod
    def getEventByID(eid):
        try:
            events = Event.eventManager.getByUUID(eid)
            serializer = EventSerializer(events)
            return serializer.data
        except Exception as e:
            return None