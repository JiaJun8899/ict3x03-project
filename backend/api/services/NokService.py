from sre_compile import FAILURE
from sre_constants import SUCCESS
from api.models import  NOK 
from api.serializer import NOKSerializer
from django.http import JsonResponse
from django.db import transaction

class NokService:
    def __init__(self):
        pass
    
    @staticmethod
    def getNokById(id):
        try:
            nok = NOK.objects.get(id=id)      
            serializer = NOKSerializer(nok)                 
            return serializer.data
        except Exception as e:
            return False   
        
    @staticmethod
    def createNok(name,relationship,phoneNum):
        try:
            newNok = NOK.objects.create(
                name=name,
                relationship=relationship,
                phoneNum=phoneNum,
            )
            newNok.save()
            serializer  = NOKSerializer(newNok)
            return serializer.data
        except Exception as e:
            return False

        
    @staticmethod
    def updateNok(data,id):
        try:
            user = NOK.objects.get(id=id) 
            serializer = NOKSerializer(instance=user, data=data)
            if serializer.is_valid():
                serializer.save()
                return True, None
            return False, serializer.errors
        except Exception as e:
            return False