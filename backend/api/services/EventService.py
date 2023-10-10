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
    
    def createEvent(data:dict):
        eventSerializer = EventSerializer(data=data)
        print(eventSerializer)
        if eventSerializer.is_valid():
            obj = eventSerializer.save()
            return True
        else:
            return False
            