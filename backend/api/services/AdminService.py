from api.models import Organizer

class AdminService:
    def __init__(self):
        pass

    @staticmethod
    def updateOrganizer(organizer_uuid, status):
        try:
            Organizer.organizerManager.updateOrganization(organizer_uuid, status)
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def getAllOrganizers():
        try:
            return Organizer.organizerManager.getAllRecords()
        except Exception as e:
            print(e)
            return False

