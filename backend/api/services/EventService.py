from api.models import EventOrganizerMapping, Organizer, Event, EventParticipant
from api.serializer import EventOrganizerMappingSerializer, EventSerializer, EventOrganizerMappingCreate, EventParticipantSerializer

class EventService:
    def __init__(self):
        pass
    
    @staticmethod
    def getAllEvent():
        events = EventOrganizerMapping.eventMapperManager.getAllRecords()
        serializer = EventOrganizerMappingSerializer(events, many=True)
        return serializer.data
    
    def createEvent(data, organization_id):
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
    
    def getParticipantsByEvent(organizer_id, eid):
        # Check if org and event are linked
        # If have, query the participants
        eventInstance = EventOrganizerMapping.eventMapperManager.getMapByOrgEventUUID(organizer_id, eid)
        if eventInstance is None:
            return None
        particpants = EventParticipant.eventParticipantManager.getParticipantsByEventUUID(eid)
        serializer = EventParticipantSerializer(particpants, many=True)
        return serializer.data
        