from api.models import EventOrganizerMapping, Organizer, Event, EventParticipant
from api.serializer import (
    EventOrganizerMappingSerializer,
    EventSerializer,
    EventOrganizerMappingCreate,
    EventParticipantSerializer,
    AllEventOrganizerMappingSerializer
)
import os
from datetime import datetime, timezone
import pytz
import django.utils as du

class EventService:
    def __init__(self):
        pass
    
    def updateEventStatus():
        events = Event.eventManager.getAllRecords().filter(endDate__lt=du.timezone.now())
        events.update(eventStatus='over')
    
    def checkFullEvent(eid):
        event = Event.eventManager.getByUUID(eid)
        if event is None:
            return True
        eventParticipants = EventParticipant.eventParticipantManager.getParticipantsByEventUUID(eid)
        if eventParticipants.count() >= event.noVol and event.eventStatus != "over":
            return False
        return True

    def updateParticipants(eid):
        event = Event.eventManager.getByUUID(eid)
        if event is None:
            return
        eventParticipants = EventParticipant.eventParticipantManager.getParticipantsByEventUUID(eid)
        if eventParticipants.count() >= event.noVol and event.eventStatus != "over":
            event.eventStatus='closed'
            event.save()
        else:
            event.eventStatus='open'
            event.save()

    def createEvent(data, organization_id):
        eventSerializer = EventSerializer(data=data)
        if eventSerializer.is_valid():
            newEvent = eventSerializer.save()
            organization = Organizer.organizerManager.getByUUID(organization_id)
            mapperSerializer = EventOrganizerMappingCreate(
                data={"event": newEvent.eid, "organizer": organization.user_id}
            )
            if mapperSerializer.is_valid():
                mapperSerializer.save()
                return True, None
            else:
                newEvent.delete()
                return False, mapperSerializer.errors
        return False, eventSerializer.errors

    def getEventByOrg(organizer_id):
        events = EventOrganizerMapping.eventMapperManager.getAllRecords().filter(organizer_id=organizer_id, event__endDate__gte=du.timezone.now()).exclude(event__eventStatus='over')
        serializer = EventOrganizerMappingSerializer(events, many=True)
        return serializer.data

    def checkValid(orgid, eid):
        eventMapInstance = (
            EventOrganizerMapping.eventMapperManager.getMapByOrgEventUUID(orgid, eid)
        )
        if eventMapInstance:
            return eventMapInstance
        else:
            return None

    def updateEvent(data, eid):
        eventInstance = Event.eventManager.getByUUID(eid)
        if 'startDate' in data:
            data['startDate'] = datetime.fromisoformat(data['startDate'])
            data['startDate'] = data['startDate'].astimezone(timezone.utc)
        if 'endDate' in data:
            data['endDate'] = datetime.fromisoformat(data['endDate'])
            data['endDate'] = data['endDate'].astimezone(timezone.utc)
        if 'startDate' not in data:
            data["startDate"] = eventInstance.startDate
        if 'endDate' not in data:
            data["endDate"] = eventInstance.endDate
        eventSerializer = EventSerializer(
            instance=eventInstance, data=data, partial=True
        )
        if eventSerializer.is_valid():
            eventSerializer.save()
            EventService.updateParticipants(eid)
            return True, None
        return False, eventSerializer.errors
    
    def checkPastEvent(self,eid):
        eventInstance = Event.eventManager.getByUUID(eid) 
        serializer = EventSerializer(eventInstance)
        timestamp = datetime.fromisoformat(serializer.data["startDate"])
        current_time = datetime.now(pytz.timezone('Asia/Singapore'))  # Use the appropriate timezone

        # Compare the timestamps
        if timestamp < current_time:
            return True
        return False
          

    def deleteEvent(eid):
        try:
            eventInstance = Event.eventManager.getByUUID(eid)
            if eventInstance.eventImage:
                if os.path.isfile(eventInstance.eventImage.path):
                    os.remove(eventInstance.eventImage.path)
            Event.eventManager.deleteByUUID(eid)
            return True
        except Exception:
            return False

    def getParticipantsByEvent(organizer_id, eid):
        eventInstance = EventOrganizerMapping.eventMapperManager.getMapByOrgEventUUID(
            organizer_id, eid
        )
        if eventInstance is None:
            return None
        particpants = (EventParticipant.eventParticipantManager.getParticipantsByEventUUID(eid))
        serializer = EventParticipantSerializer(particpants, many=True)
        return serializer.data

    def searchEvent(name):
        events = EventOrganizerMapping.eventMapperManager.getAllRecords().filter(approval='accepted',event__eventName__contains=name, event__endDate__gte=du.timezone.now()).exclude(event__eventStatus='over')
        serializer = EventOrganizerMappingSerializer(events, many=True)
        return serializer.data

    def getEventByID(organizer_id, eid):
        orgEventInstance = (
            EventOrganizerMapping.eventMapperManager.getMapByOrgEventUUID(
                organizer_id, eid
            )
        )
        eventInstance = Event.eventManager.getByUUID(orgEventInstance.event_id)
        serializer = EventSerializer(eventInstance)
        return serializer.data
    
    def userGetEventById(self,eid):
        eventInstance = Event.eventManager.getByUUID(uuid=eid)
        serializer = EventSerializer(eventInstance)
        return serializer.data
    
    def getAllEvent():
        events = EventOrganizerMapping.eventMapperManager.getAllRecords().filter(approval="accepted", event__endDate__gte=du.timezone.now()).exclude(event__eventStatus='over')
        # events = Event.eventManager.getAllRecords().filter(eventStatus= "open")
        serializer = AllEventOrganizerMappingSerializer(events,many=True)
        return serializer.data