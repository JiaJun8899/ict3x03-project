from sre_compile import FAILURE
from sre_constants import SUCCESS
from api.models import GenericUser, NOK, EmergencyContacts
from api.serializer import EmergencyContactsSerializer
from django.http import JsonResponse

class EmergencyContactService:
    def __init__(self):
        pass
    
    
    @staticmethod
    def getContactById(id):
        try:
            contact =  EmergencyContacts.objects.get(normalUser_id=id)
            serializer = EmergencyContactsSerializer(contact)          
            return serializer.data
        except Exception as e:
            print(e)
            return False   


            


