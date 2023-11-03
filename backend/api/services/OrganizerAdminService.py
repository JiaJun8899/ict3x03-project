from api.models import Organizer
from api.serializer import OrganizerProfileSerializer
class OrganizerAdminService:
    def __init__(self):
        pass

    @staticmethod
    def getOrgById(eid):
        try:
            user =  Organizer.organizerManager.getByUUID(eid)            
            serializerGeneric = OrganizerProfileSerializer(user)      
            return serializerGeneric.data    
        except Exception as e:
            return False