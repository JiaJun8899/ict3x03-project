from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.services import *
from django.core.files.uploadedfile import InMemoryUploadedFile
from datetime import datetime
from django.http import JsonResponse
from django.middleware.csrf import get_token
from uuid import UUID
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
import requests
from dotenv import load_dotenv

load_dotenv()
RECAPTCHA_KEY = os.getenv('RECAPTCHA_KEY',os.environ.get('RECAPTCHA_KEY'))
def csrf(request):
    return JsonResponse({"csrfToken": get_token(request)})

def ping(request):
    return JsonResponse({"result": "OK"})

class TestAPI(APIView):
    def get(self, request):
        # return Response({"role": "test"}, status=status.HTTP_200_OK)
        return Response({'id': request.session["_auth_user_id"], 'role' : request.session["role"]}, status=status.HTTP_200_OK)
        # Example of session being used

class UpdateOrganizerStatus(APIView):
    def put(self, request):
        organizerAdminService = OrganizerAdminService()
        success = organizerAdminService.updateOrganizer(
            organizer_uuid=request.data["user"],
            status=request.data["validOrganisation"],
        )
        if success:
            return Response({"message": "Organizer status updated successfully."})
        else:
            return Response({"message": "Failed to update organizer status."})

class GetAllOrganizers(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        organizerAdminService = OrganizerAdminService()
        organizers = organizerAdminService.getAllOrganizers()

        if organizers != None:
            # Assuming that the returned organizers is a QuerySet or list of Organizer instances
            return Response({"data": organizers})
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
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get(self, request):
        organization_id = request.session["_auth_user_id"]
        print(organization_id)
        eventsByOrg = EventService.getEventByOrg(organization_id)
        return Response(eventsByOrg, status=status.HTTP_200_OK)

    def post(self, request):
        """Create Event"""
        organization_id = request.session["_auth_user_id"]
        print(request.data)
        data = {
            "eventName": request.data["eventName"],
            "startDate": request.data["startDate"],
            "endDate": request.data["endDate"],
            "noVol": request.data["noVol"],
            "eventDesc": request.data["eventDesc"],
            "eventImage": request.data["eventImage"],
        }
        success = EventService.createEvent(data, organization_id)
        if success:
            return Response({"status": status.HTTP_200_OK})
        else:
            return Response({"status": status.HTTP_400_BAD_REQUEST})

    def put(self, request):
        """Update event"""
        print(request.data)
        organization_id = request.session["_auth_user_id"]
        checkValid = EventService.checkValid(
            organization_id, request.data["eid"]
        )  # Should be able to remove and just use under updateEvent
        if checkValid:
            data = {}
            for key, value in request.data.items():
                if key == "eventImage" and not isinstance(value, InMemoryUploadedFile):
                    pass
                else:
                    data[key] = value
            data["eventStatus"] = "open"
            print(data)
            success = EventService.updateEvent(data, request.data["eid"])
            if success:
                return Response({"status": status.HTTP_200_OK})
        return Response({"status": status.HTTP_400_BAD_REQUEST})

    def delete(self, request):
        """Delete Event and Mapping"""
        # print(request.data)
        organization_id = request.session["_auth_user_id"]
        success = EventService.deleteEvent(request.data["eid"])
        success = True
        if success:
            return Response({"status": status.HTTP_200_OK})
        else:
            return Response({"status": status.HTTP_400_BAD_REQUEST})


class EventSingleByOrganizationAPI(APIView):
    def get(self, request, event_id):
        organization_id = request.session["_auth_user_id"]
        eventsByOrg = EventService.getEventByID(organization_id, event_id)
        return Response(eventsByOrg, status=status.HTTP_200_OK)


class RegisterUserAPIView(APIView):
    def post(self, request):
        data = {
            "username": request.data["email"],
            "email": request.data["email"],
            "first_name": request.data["firstName"],
            "last_name": request.data["lastName"],
            "phoneNum": request.data["phoneNum"],
            "nric": request.data["NRIC"],
            "password": request.data["password"],
            "password2": request.data["password2"],
        }
        recaptcha_response = request.data["recaptchaValue"]
        verification_data = {
            "secret": RECAPTCHA_KEY,
            "response": recaptcha_response
        }
        response = requests.post("https://www.google.com/recaptcha/api/siteverify", data=verification_data)
        recaptcha_result = response.json()
        print(recaptcha_result)
        if not recaptcha_result["success"]:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            if request.data["organization"]:
                success = AccountService.createOrganisation(data)
            else:
                birthday = datetime.strptime(request.data["birthday"], "%Y-%m-%d").date()
                success = AccountService.createNormalUser(data, birthday)
            if success:
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)


class UpdateUserAPIView(APIView):
    def put(self, request):
        id = UUID(request.session["_auth_user_id"]).hex
        valid = UserService.getUserById(id)
        if valid != None:
            data = {
                "first_name": request.data["firstname"],
                "last_name": request.data["lastname"],
                "email": request.data["email"],
                "phoneNum": request.data["phoneNum"],
                "username": request.data["userName"],
            }
        emergency = EmergencyContactService.getContactById(id)
        if emergency:
            nokData = {
                "name": request.data["nokName"],
                "relationship": request.data["nokRelationship"],
                "phoneNum": request.data["nokPhone"],
            }
        nokUpdateSuccess = NokService.updateNok(nokData, emergency["nok"])

        success = UserService.updateUserProfile(data, id)
        if success and nokUpdateSuccess:
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class GetProfileDetailsAPIView(APIView):
    def get(self, request):
        data = {}
        id = UUID(request.session["_auth_user_id"]).hex
        # this part use the session to get id
        valid = UserService.getUserById(id)
        print(valid)
        # print(UUID(request.session["_auth_user_id"]).hex)

        data["profile"] = valid
        emergency = EmergencyContactService.getContactById(id)
        if emergency:
            # data["emergency"] = emergency
            # print(emergency)
            nok = NokService.getNokById(emergency["nok"])
            data["nok"] = nok

        # print(valid)
        return Response(data, status=status.HTTP_200_OK)


class SignUpEventAPIView(APIView):
    def post(self, request):
        id = UUID(request.session["_auth_user_id"]).hex
        validUser = UserService.getUserById(id)
        validEvent = EventCommonService.getEventByID(request.data["eid"])
        if validUser != None and validEvent != None:
            data = {"event": request.data["eid"], "participant": id}
            success = UserService.signUpEvent(data=data)
            print(success)
        if success:
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class CancelSignUpEventAPIView(APIView):
    def delete(self, request):
        # print(request.session.value())
        id = UUID(request.session["_auth_user_id"]).hex
        validUser = UserService.getUserById(id)
        validEvent = EventCommonService.getEventByID(request.data["eid"])
        if validUser != None and validEvent != None:
            data = {"event": request.data["eid"], "participant": id}
            success = UserService.cancelSignUpEvent(data=data)
            if success:
                return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class SearchEvents(APIView):
    def post(self, request):
        events = EventService.searchEvent(request.data["name"])
        if events != None:
            return Response(events, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class GetAllEvent(APIView):
    def get(self, request):
        eventService = EventService()
        events = eventService.getAllEvents()

        if events != None:
            # Assuming that the returned organizers is a QuerySet or list of Organizer instances
            return Response({"data": events})
        else:
            return Response(
                {"Failed to retrieve organizers."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

class GetEvent(APIView):
    def get(self, request, eid):
        eventService = EventService()
        events = eventService.userGetEventById(eid)

        if events != None:
            # Assuming that the returned organizers is a QuerySet or list of Organizer instances
            return Response({"data": events})
        else:
            return Response(
                {"Failed to retrieve event."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

class GetAllEvent(APIView):
    def get(self, request):
        eventService = EventService()
        events = eventService.getAllEvents()

        if events != None:
            # Assuming that the returned organizers is a QuerySet or list of Organizer instances
            return Response({"data": events})
        else:
            return Response(
                {"Failed to retrieve organizers."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

class Login(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        authenticated = AuthService.authenticateUser(request, username, password)
        if authenticated:
            request.session["email"] = authenticated.email
            request.session["role"] = AccountService.getUserRole(authenticated.id)
            return Response({"detail": "Logged in successfully."}, status=200)
        return Response({"detail": "Invalid credentials."}, status=401)