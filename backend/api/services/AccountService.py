from api.serializer import (
    OrganizerSerializer,
    RegisterNormalUserSerializer,
    RegisterUserSerializer,
)
from api.models import NormalUser, Organizer


class AccountService:
    def createOrganisation(data):
        genericUserSerializer = RegisterUserSerializer(data=data)
        if genericUserSerializer.is_valid():
            genericUserObj = genericUserSerializer.save()
            genericUserObj.is_active = 0
            genericUserObj.save()
            organizer = OrganizerSerializer(data={"user": genericUserObj.id})
            if organizer.is_valid():
                organizer.save()
                return True, None, genericUserObj.id
            else:
                genericUserObj.delete()
        return False, genericUserSerializer.errors, None

    def createNormalUser(data, birthday):
        genericUserSerializer = RegisterUserSerializer(data=data)
        if genericUserSerializer.is_valid():
            genericUserObj = genericUserSerializer.save()
            normalUser = RegisterNormalUserSerializer(
                data={"user": genericUserObj.id, "birthday": birthday}
            )
            if normalUser.is_valid():
                normalUser.save()
                return True, None, genericUserObj.id
            else:
                genericUserObj.delete()
        return False, genericUserSerializer.errors, None


    def getUserRole(userId):
        if Organizer.organizerManager.getByUUID(userId):
            return "Organizer"
        if NormalUser.normalUserManager.getByUUID(userId):
            return "Normal"
        else:
            return None
