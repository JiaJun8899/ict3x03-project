from api.models import EventOrganizerMapping, Organizer, Event, EventParticipant, NormalUser
from api.serializer import (
    EventOrganizerMappingSerializer,
    EventSerializer,
    EventOrganizerMappingCreate,
    EventParticipantSerializer,
)
import os
from datetime import datetime
import pytz


class EventService:
    def __init__(self):
        pass

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
                return True
        return False

    def getEventByOrg(organizer_id):
        events = EventOrganizerMapping.eventMapperManager.getAllRecords().filter(
            organizer_id=organizer_id
        )
        serializer = EventOrganizerMappingSerializer(events, many=True)
        return serializer.data

    def checkValid(orgid, eid):
        eventMapInstance = (
            EventOrganizerMapping.eventMapperManager.getMapByOrgEventUUID(orgid, eid)
        )
        if eventMapInstance:
            print(eventMapInstance.id)
            return eventMapInstance
        else:
            return None

    def updateEvent(data, eid):
        eventInstance = Event.eventManager.getByUUID(eid)
        eventSerializer = EventSerializer(
            instance=eventInstance, data=data, partial=True
        )
        print(eventSerializer.is_valid())
        print(eventSerializer.errors)
        if eventSerializer.is_valid():
            eventSerializer.save()
            return True
        return False
    
    def checkPastEvent(self,eid):
        eventInstance = Event.eventManager.getByUUID(eid) 
        serializer = EventSerializer(eventInstance)
        # print(serializer.data["startDate"])  
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
                    # print("here")
                    os.remove(eventInstance.eventImage.path)
            Event.eventManager.deleteByUUID(eid)
            return True
        except Exception:
            return False

    def getParticipantsByEvent(organizer_id, eid):
        # Check if org and event are linked
        # If have, query the participants
        eventInstance = EventOrganizerMapping.eventMapperManager.getMapByOrgEventUUID(
            organizer_id, eid
        )
        if eventInstance is None:
            return None
        particpants = (EventParticipant.eventParticipantManager.getParticipantsByEventUUID(eid))
        serializer = EventParticipantSerializer(particpants, many=True)
        return serializer.data

    def searchEvent(name):
        events = Event.eventManager.searchEvent(name)
        print(events)
        serializer = EventSerializer(events, many=True)
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
        events = Event.eventManager.getAllRecords()
        serializer = EventSerializer(events,many=True)
        return serializer.data

