from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.services import OrganizerAdminService, EventService


class UpdateOrganizerStatus(APIView):
    def put(self, request):
        success = OrganizerAdminService.updateOrganizer(request.data["user"],request.data["validOrganisation"])
        if success:
            return Response({"status": "success", "message": "Organizer status updated successfully."})
        else:
            return Response({"status": "error", "message": "Failed to update organizer status."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetAllOrganizers(APIView):
    def get(self, request):
        organizers = OrganizerAdminService.getAllOrganizers()

        if organizers != None:
            # Assuming that the returned organizers is a QuerySet or list of Organizer instances
            return Response({"status": status.HTTP_200_OK, "data": organizers})
        else:
            return Response({"status": "error", "message": "Failed to retrieve organizers."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class EventAPI(APIView):
    """ 1. Create Event
        2. Update Event
        3. Get all Event
        4. Get Event by Organiser
        5. Delete Event
        6. Change approval status"""
    def get(self, request):
        '''Gets all the events'''
        allEvents = EventService.getAllEvent()
        return Response(allEvents, status=status.HTTP_200_OK)
    def post(self, request):
        pass
