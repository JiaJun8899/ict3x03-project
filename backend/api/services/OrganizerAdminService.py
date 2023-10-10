from sre_compile import FAILURE
from sre_constants import SUCCESS
from api.models import Organizer
from api.serializer import OrganizerSerializer
class OrganizerAdminService:
    def __init__(self):
        pass

    @staticmethod
    def updateOrganizer(organizer_uuid, status):
        inputData={'user': organizer_uuid, 'validOrganisation': status}
        organizer = Organizer.organizerManager.getByUUID(organizer_uuid)
        organizerSerializer = OrganizerSerializer(instance=organizer, many=False, data=inputData)
        if organizerSerializer.is_valid():
            # Check if update passes
            if organizerSerializer.update(instance=organizer, validated_data = organizerSerializer.validated_data)   != None:
                return SUCCESS
            else:
                return FAILURE
        else:
            return FAILURE

            
    @staticmethod
    def getAllOrganizers():
        try:
            organizers = Organizer.organizerManager.getAllRecords()
            serializer = OrganizerSerializer(organizers, many=True)
            return serializer.data
        except Exception as e:
            print(e)
            return None

