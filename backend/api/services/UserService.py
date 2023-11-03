from api.models import GenericUser, NormalUser,EventParticipant
from api.serializer import NormalUserSerializer, GenericUserSerializer,EventSignUpParticipantSerializer
from api.services import EventService
from django.utils import timezone

class UserService:
    def __init__(self):
        pass
    
    @staticmethod
    def validUser(eid):
        user = NormalUser.normalUserManager.getByUUID(eid)
        return user
    
    @staticmethod
    def getUserById(eid):
        try:
            user =  NormalUser.normalUserManager.getByUUID(eid)            
            serializerGeneric = NormalUserSerializer(user)      
            return serializerGeneric.data    
        except Exception as e:
            return False

    @staticmethod
    def updateUserProfile(data,eid):
        try:
            user = GenericUser.genericUserManager.getByUUID(eid)
            serializer = GenericUserSerializer(instance=user, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return True, None
            return False, serializer.errors
        except Exception as e:
            return False
        

    @staticmethod
    def signUpEvent(data):
        try:
            eventSerializer = EventSignUpParticipantSerializer(data=data)
            if eventSerializer.is_valid() and EventService.checkFullEvent(data["event"]):
                eventSerializer.save()
                EventService.updateParticipants(data["event"])
                return True
            else:
                return False
        except Exception as e:
            return False
        
    @staticmethod
    def cancelSignUpEvent(data):
        try:         
            signedup = EventParticipant.eventParticipantManager.deleteSingleUserEventmap(data["event"],data["participant"])
            if not signedup:
                return False
            else:
                EventService.updateParticipants(data["event"])
                return True
        except Exception as e:
            return False