from sre_compile import FAILURE
from sre_constants import SUCCESS
from api.models import  NOK 
from api.serializer import NOKSerializer
from django.http import JsonResponse

class NokService:
    def __init__(self):
        pass
    
    @staticmethod
    def getNokById(id):
        try:
            nok = NOK.objects.get(id=id)      
            serializer = NOKSerializer(nok)
            print(serializer)
            # if(serializer.is_valid()):
                # print(serializer.data)                    
            return serializer.data
        except Exception as e:
            print(e)
            return False   


            


