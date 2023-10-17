from api.models import Organizer
from api.serializer import OrganizerSerializer
class OrganizerAdminService:
    def __init__(self):
        pass

    def updateOrganizer(self,organizer_uuid, status):
        inputData={'user': organizer_uuid, 'validOrganisation': status}
        organizer = Organizer.organizerManager.getByUUID(organizer_uuid)
        organizerSerializer = OrganizerSerializer(instance=organizer, many=False, data=inputData)
        if organizerSerializer.is_valid():
            # Check if update passes
            if organizerSerializer.update(instance=organizer, validated_data = organizerSerializer.validated_data)   != None:
                return True
            else:
                return False
        else:
            return False

            
    def getAllOrganizers(self):
        try:
            organizers = Organizer.organizerManager.getAllRecords()
            serializer = OrganizerSerializer(organizers, many=True)
            return serializer.data
        except Exception as e:
            print(e)
            return None

