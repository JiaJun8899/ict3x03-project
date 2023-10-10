from api.models import EventOrganizerMapping, Organizer, Event
from api.serializer import EventOrganizerMappingSerializer, EventSerializer, OrganizerSerializer

class EventService:
    def __init__(self):
        pass
    
    @staticmethod
    def getAllEvent():
        events = EventOrganizerMapping.eventManager.getAllRecords()
        serializer = EventOrganizerMappingSerializer(events, many=True)
        return serializer.data