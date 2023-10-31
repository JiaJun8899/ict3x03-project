from api.models import EventParticipant
from api.serializer import (
    EventParticipantSerializer,
)
import os

class EventParticipantService:
    def __init__(self):
        pass

    def getParticipatedEvents(self,user_id):
        events = EventParticipant.eventParticipantManager.getEventsByParticipant(user_id)
        serializer = EventParticipantSerializer(events,many=True)        
        return serializer.data