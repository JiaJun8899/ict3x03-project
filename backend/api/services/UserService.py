from sre_compile import FAILURE
from sre_constants import SUCCESS
from api.models import GenericUser, NOK, EmergencyContacts, NormalUser,EventParticipant
from api.serializer import NormalUserSerializer, GenericUserSerializer, EventParticipantSerializer,EventSignUpParticipantSerializer, NOKSerializer
from django.http import JsonResponse

class UserService:
    def __init__(self):
        pass
    
    @staticmethod
    def validUser(eid):
        user = NormalUser.normalUserManager.getByUUID(eid)
        return user
    
    @staticmethod
    def getUserById(eid):
        # data = {}
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
                return True
        except Exception as e:
            return False
        

    @staticmethod
    def signUpEvent(data):
        try:
            eventSerializer = EventSignUpParticipantSerializer(data=data)
            if eventSerializer.is_valid():
                eventSerializer.save()
                return True
        except Exception as e:
            return False
        
    @staticmethod
    def cancelSignUpEvent(data):
        try:         
            signedup = EventParticipant.eventParticipantManager.deleteSingleUserEventmap(data["event"],data["participant"])
            return True
        except Exception as e:
            return False