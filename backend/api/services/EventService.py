from api.models import EventOrganizerMapping, Organizer, Event
from api.serializer import EventOrganizerMappingSerializer, EventSerializer, OrganizerSerializer, EventOrganizerMappingCreate

class EventService:
    def __init__(self):
        pass
    
    @staticmethod
    def getAllEvent():
        events = EventOrganizerMapping.eventManager.getAllRecords()
        serializer = EventOrganizerMappingSerializer(events, many=True)
        return serializer.data
    
    def createEvent(data:dict, organization_id):
        eventSerializer = EventSerializer(data=data)
        print(eventSerializer)
        if eventSerializer.is_valid():
            obj = eventSerializer.save()
            organization = Organizer.organizerManager.getByUUID(organization_id)
            print(organization.user_id)
            mapperSerializer = EventOrganizerMappingCreate(data={'event':obj.eid, 'organizer':organization.user_id})
            print(mapperSerializer)
            if mapperSerializer.is_valid():
                mapperSerializer.save()
                return True
            else:
                print("nope")
                return False
        else:
            print("nope here")
            return False
    
    def getEventByOrg(organizer_id):
        events = EventOrganizerMapping.eventManager.getAllRecords().filter(organizer_id = organizer_id)
        serializer = EventOrganizerMappingSerializer(events, many=True)
        return serializer.data
            