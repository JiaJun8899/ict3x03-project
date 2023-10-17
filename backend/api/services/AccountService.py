from api.serializer import OrganizerSerializer, RegisterNormalUserSerializer, RegisterUserSerializer
class AccountService:
    def createOrganisation(data):
        genericUserSerializer = RegisterUserSerializer(data=data)
        if genericUserSerializer.is_valid():
            genericUserObj = genericUserSerializer.save()
            organizer = OrganizerSerializer(data={"user":genericUserObj.id})
            if organizer.is_valid():
                organizer.save()
                return True
            else:
                genericUserObj.delete()
                print(organizer.errors)
        return False
                
    def createNormalUser(data, birthday):
        genericUserSerializer = RegisterUserSerializer(data=data)
        if genericUserSerializer.is_valid():
            genericUserObj = genericUserSerializer.save()
            normalUser = RegisterNormalUserSerializer(data={"user":genericUserObj.id, 'birthday':birthday})
            if normalUser.is_valid():
                normalUser.save()
                return True
            else:
                genericUserObj.delete()
                print(normalUser.errors)
        return False