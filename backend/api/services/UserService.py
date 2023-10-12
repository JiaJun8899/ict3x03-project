from sre_compile import FAILURE
from sre_constants import SUCCESS
from api.models import GenericUser
from api.serializer import GenericUserSerializer

class UserService:
    def __init__(self):
        pass
    
    @staticmethod
    def validUser(eid):
        user = GenericUser.genericUserManager.getByUUID(eid)
        return user

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


            


