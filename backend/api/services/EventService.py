from api.models import EventOrganizerMapping, Organizer, Event
from api.serializer import EventOrganizerMappingSerializer, EventSerializer, OrganizerSerializer, EventOrganizerMappingCreate

class EventService:
    def __init__(self):
        pass
    
    @staticmethod
    def getAllEvent():
        events = EventOrganizerMapping.eventMapperManager.getAllRecords()
        serializer = EventOrganizerMappingSerializer(events, many=True)
        return serializer.data
    
    def createEvent(data:dict, organization_id):
        eventSerializer = EventSerializer(data=data)
        if eventSerializer.is_valid():
            newEvent = eventSerializer.save()
            organization = Organizer.organizerManager.getByUUID(organization_id)
            mapperSerializer = EventOrganizerMappingCreate(data={'event':newEvent.eid, 'organizer':organization.user_id})
            if mapperSerializer.is_valid():
                mapperSerializer.save()
                return True
        return False
    
    def getEventByOrg(organizer_id):
        events = EventOrganizerMapping.eventMapperManager.getAllRecords().filter(organizer_id = organizer_id)
        serializer = EventOrganizerMappingSerializer(events, many=True)
        return serializer.data
    
    def checkValid(eid):
        eventMapInstance = EventOrganizerMapping.eventMapperManager.getMapByEventUUID(eid)
        return eventMapInstance
    
    def updateEvent(data, eid):
        eventInstance = Event.eventManager.getByUUID(eid)
        eventSerializer = EventSerializer(instance=eventInstance, data=data, partial = True)
        if eventSerializer.is_valid():
            eventSerializer.save()
            return True
        return False
    
    def deleteEvent(eid):
        try:
            Event.eventManager.deleteByUUID(eid)
            return True
        except Exception:
            return False
        