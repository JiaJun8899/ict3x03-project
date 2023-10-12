from sre_compile import FAILURE
from sre_constants import SUCCESS
from api.models import GenericUser, EventParticipant, NormalUser
from api.serializer import NormalUserSerializer, GenericUserSerializer, EventParticipantSerializer,EventSignUpParticipantSerializer

class UserService:
    def __init__(self):
        pass
    
    @staticmethod
    def validUser(eid):
        user = GenericUser.genericUserManager.getByUUID(eid)
        return user
    
    @staticmethod
    def getUserById(eid):
        try:
            user =  NormalUser.normalUserManager.getByUUID(eid)
            serializer = NormalUserSerializer(user)            
            return serializer.data
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
            print(e)
            return False
        

    @staticmethod
    def signUpEvent(data):
        try:
            eventSerializer = EventParticipantSerializer(data=data)
            print(eventSerializer.is_valid())
            print(eventSerializer.errors)
            if eventSerializer.is_valid():
                eventSerializer.save()
                return True
        except Exception as e:
            print(e)
            return False


            


