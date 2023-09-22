from api.models import Organizer

class AdminService:
    def __init__(self):
        pass

    @staticmethod
    def update_organizer(organizer_uuid, status):
        try:
            Organizer.organiserManager.updateOrganization(organizer_uuid, status)
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def getAllOrganizers():
        try:
            return Organizer.organiserManager.getAll()
        except Exception as e:
            print(e)
            return False

