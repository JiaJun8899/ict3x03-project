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

def csrf(request):
    return JsonResponse({'csrfToken': get_token(request)})

def ping(request):
    return JsonResponse({'result': 'OK'})

from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
class UpdateOrganizerStatus(APIView):
    def put(self, request):
        organizerAdminService = OrganizerAdminService()
        success = organizerAdminService .updateOrganizer(organizer_uuid = request.data["user"],status = request.data["validOrganisation"])
        if success:
            return Response({"message": "Organizer status updated successfully."})
        else:
            return Response({"message": "Failed to update organizer status."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
    parser_classes = (MultiPartParser,FormParser, JSONParser)

    def get(self, request, organization_id):
        eventsByOrg = EventService.getEventByOrg(organization_id)
        return Response(eventsByOrg, status=status.HTTP_200_OK)

    def post(self, request, organization_id):
        """Create Event"""
        print(request.data)
        data = {
            "eventName": request.data['eventName'],
            "startDate": request.data['startDate'],
            "endDate": request.data['endDate'],
            "noVol": request.data['noVol'],
            "eventDesc": request.data['eventDesc'],
            "eventImage": request.data['eventImage'],
        }
        success = EventService.createEvent(data, organization_id)
        if success:
            return Response({"status": status.HTTP_200_OK})
        else:
            return Response({"status": status.HTTP_400_BAD_REQUEST})

    def put(self, request, organization_id):
        """Update event"""
        print(request.data)
        checkValid = EventService.checkValid(organization_id,
            request.data["eid"]
        )  # Should be able to remove and just use under updateEvent
        if checkValid:
            data = {}

            for key, value in request.data.items():
                if key == 'eventImage' and not isinstance(value, InMemoryUploadedFile):
                    pass
                else:
                    data[key] = value
            data['eventStatus'] = 'open'
            print(data)
            success = EventService.updateEvent(data, request.data["eid"])
            if success:
                return Response({"status": status.HTTP_200_OK})
        return Response({"status": status.HTTP_400_BAD_REQUEST})

    def delete(self, request, organization_id):
        """Delete Event and Mapping"""
        # print(request.data)
        success = EventService.deleteEvent(request.data["eid"])
        success = True
        if success:
            return Response({"status": status.HTTP_200_OK})
        else:
            return Response({"status": status.HTTP_400_BAD_REQUEST})


class EventSingleByOrganizationAPI(APIView):
    def get(self, request, organization_id, event_id):
        eventsByOrg = EventService.getEventByID(organization_id, event_id)
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
class UpdateUserAPIView(APIView):
    def put(self, request):
        # ['first_name', 'last_name', 'email', 'phoneNum', 'username']
        # ["name", "relationship", "phoneNum"]
        valid = UserService.UserService.getUserById(request.data["id"]) 
        emergency = EmergencyContactService.EmergencyContactService.getContactById(request.data["id"])
        if emergency:    
            nokData = {
                "name" : request.data["name"], 
                "relationship" : request.data["relationship"],
                "phoneNum": request.data["phoneNum"]
            }
            nokUpdateSuccess = NokService.NokService.updateNok(nokData,emergency["nok"]) 
            print(nokUpdateSuccess)       
            # nok = NokService.NokService.getNokById(emergency["nok"])
        
        if valid != None:
            data ={
                "first_name": request.data["first_name"],
                "last_name": request.data["last_name"],
                "email": request.data["email"],
                "phoneNum": request.data["phoneNum"],
                "username": request.data["username"],
            }
            success = UserService.UserService.updateUserProfile(data,request.data["id"])
            if success:
                return Response({"status": status.HTTP_200_OK})
        return Response({"status": status.HTTP_400_BAD_REQUEST})
    
class GetProfileDetailsAPIView(APIView):
    def get(self,request,user_id):
        data = {}
        valid = UserService.UserService.getUserById(user_id)
        data["profile"] = valid
        emergency = EmergencyContactService.EmergencyContactService.getContactById(user_id)
        if emergency:            
            # data["emergency"] = emergency
            # print(emergency)
            nok = NokService.NokService.getNokById(emergency["nok"])
            data["nok"] = nok
        
        # print(valid)
        return Response(data, status=status.HTTP_200_OK)

    
class SignUpEventAPIView(APIView):
    def post(self,request):

        validUser = UserService.UserService.getUserById(request.data["id"])
        validEvent = EventCommonService.EventCommonService.getEventByID(request.data["eid"])
        if validUser != None and validEvent != None:
            data={               
                "event": request.data["eid"],     
                "participant":request.data["id"]          
            }
            success = UserService.UserService.signUpEvent(data=data)
            if success:
                return Response({"status": status.HTTP_200_OK})
        return Response({"status": status.HTTP_400_BAD_REQUEST})
    

class SearchEvents(APIView):
    def post(self,request):
        events = EventService.searchEvent(request.data["name"])
        if events != None:
            return Response(events, status=status.HTTP_200_OK)
        return Response({"status": status.HTTP_400_BAD_REQUEST})



class TestAPI(APIView):
    def get(self, request):
        return Response({'role': 'test'}, status=status.HTTP_200_OK)

class GetAllEvent(APIView):
    def get(self, request):
        eventService = EventService()
        events = eventService.getAllEvents()

        if  events != None:
            # Assuming that the returned organizers is a QuerySet or list of Organizer instances
            return Response({"data":events})
        else:
            return Response({"Failed to retrieve organizers."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class Login(APIView):
    def post(self,request):
        username = request.data.get("username")
        password = request.data.get("password")
        authenticated = AuthService.authenticateUser(request, username, password)
        if authenticated:
            return Response({"detail": "Logged in successfully."}, status=200)
        return Response({"detail": "Invalid credentials."}, status=401)



class GetAllEvent(APIView):
    def get(self, request):
        eventService = EventService()
        events = eventService.getAllEvents()

        if  events != None:
            # Assuming that the returned organizers is a QuerySet or list of Organizer instances
            return Response({"data":events})
        else:
            return Response({"Failed to retrieve organizers."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class Login(APIView):
    def post(self,request):
        username = request.data.get("username")
        password = request.data.get("password")
        authenticated = AuthService.authenticateUser(request, username, password)
        if authenticated:
            request.session["email"] = authenticated.email
            return Response({"detail": "Logged in successfully."}, status=200)
        return Response({"detail": "Invalid credentials."}, status=401)
