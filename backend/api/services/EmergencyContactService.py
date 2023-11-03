from api.models import EmergencyContacts
from api.serializer import EmergencyContactsSerializer

class EmergencyContactService:
    def __init__(self):
        pass
    
    @staticmethod
    def getContactById(id):
        try:
            contact =  EmergencyContacts.objects.get(normalUser=id)        
            serializer = EmergencyContactsSerializer(contact)  
            if serializer != None:
                return serializer.data
            else:
                return False
        except Exception as e:
            return False   
        
    def createNewContact(nok_id,user_id):
        try:
            contact = EmergencyContacts.objects.create(
                normalUser_id=user_id,
                nok_id= nok_id
            )
            serializer = EmergencyContactsSerializer(contact)
            return True, None
        except Exception as e:
            return False