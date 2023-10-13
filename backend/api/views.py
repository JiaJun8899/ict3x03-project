from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.services import OrganizerAdminService, EventService, AccountService
from django.utils import timezone
from datetime import datetime
from rest_framework.parsers import MultiPartParser, FormParser
class UpdateOrganizerStatus(APIView):
    def put(self, request):
        success = OrganizerAdminService.updateOrganizer(
            request.data["user"], request.data["validOrganisation"]
        )
        if success:
            return Response(
                {
                    "status": "success",
                    "message": "Organizer status updated successfully.",
                }
            )
        else:
            return Response(
                {"status": "error", "message": "Failed to update organizer status."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class GetAllOrganizers(APIView):
    def get(self, request):
        organizers = OrganizerAdminService.getAllOrganizers()
        if organizers != None:
            # Assuming that the returned organizers is a QuerySet or list of Organizer instances
            return Response({"status": status.HTTP_200_OK, "data": organizers})
        else:
            return Response(
                {"status": "error", "message": "Failed to retrieve organizers."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class EventAPI(APIView):
    """1. Create Event
    2. Update Event
    3. Get all Event
    4. Get Event by Organiser
    5. Delete Event
    6. Change approval status"""

    def get(self, request):
        """Gets all the events"""
        allEvents = EventService.getAllEvent()
        return Response(allEvents, status=status.HTTP_200_OK)


class EventsByOrganizationAPI(APIView):
    parser_classes = (MultiPartParser,FormParser)

    def get(self, request, organization_id):
        eventsByOrg = EventService.getEventByOrg(organization_id)
        return Response(eventsByOrg, status=status.HTTP_200_OK)

    def post(self, request, organization_id):
        """Create Event"""
        data = {
            "eventName": request.data['data[eventName]'],
            "startDate": request.data['data[startDate]'],
            "endDate": request.data['data[endDate]'],
            "noVol": request.data['data[noVol]'],
            "eventDesc": request.data['data[eventDesc]'],
            "eventImage": request.data['data[eventImage]'],
        }
        success = EventService.createEvent(data, organization_id)
        if success:
            return Response({"status": status.HTTP_200_OK})
        else:
            return Response({"status": status.HTTP_400_BAD_REQUEST})

    def put(self, request, organization_id):
        """Update event"""
        checkValid = EventService.checkValid(
            request.data["eid"]
        )  # Should be able to remove and just use under updateEvent
        if checkValid:
            data = {
                "eventStatus": request.data["eventStatus"],
                "eventName": request.data["eventName"],
                "startDate": timezone.now(),
                "endDate": timezone.now(),
                "eventStatus": request.data["eventStatus"],
                "noVol": request.data["noVol"],
                "eventDesc": request.data["eventDesc"],
            }
            success = EventService.updateEvent(data, request.data["eid"])
            if success:
                return Response({"status": status.HTTP_200_OK})
        return Response({"status": status.HTTP_400_BAD_REQUEST})

    def delete(self, request, organization_id):
        """Delete Event and Mapping"""
        success = EventService.deleteEvent(request.data["eid"])
        if success:
            return Response({"status": status.HTTP_200_OK})
        else:
            return Response({"status": status.HTTP_400_BAD_REQUEST})


class EventSingleByOrganizationAPI(APIView):
    def get(self, request, organization_id, event_id):
        eventsByOrg = EventService.getParticipantsByEvent(organization_id, event_id)
        return Response(eventsByOrg, status=status.HTTP_200_OK)

class RegisterUserAPIView(APIView):
    def post(self, request):
        data = {
            "username": request.data["username"],
            "email": request.data["email"],
            "first_name": request.data["first_name"],
            "last_name": request.data["last_name"],
            "phoneNum": request.data["phoneNum"],
            "nric": request.data["nric"],
            "password": request.data["password"],
            "password2": request.data["password2"],
        }
        if request.data["organizer"]:
            AccountService.createOrganisation(data)
        else:
            birthday = datetime.strptime(request.data["birthday"], "%d%m%Y").date()
            AccountService.createNormalUser(data, birthday)
        return Response(status=status.HTTP_200_OK)


class TestAPI(APIView):
    def get(self, request):
        return Response({'role': 'test'}, status=status.HTTP_200_OK)