from django_otp.decorators import otp_required
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
from django.db import transaction

import logging

adminLogger = logging.getLogger("backend.api.views.admin")
generalLogger = logging.getLogger("backend.api.views.general")
authLogger = logging.getLogger("backend.api.views.auth")

load_dotenv()
RECAPTCHA_KEY = os.getenv("RECAPTCHA_KEY", os.environ.get("RECAPTCHA_KEY"))

def csrf(request):
    return JsonResponse({"csrfToken": get_token(request)})

def validEventOrg(request, eid):
    organization_id = request.session["_auth_user_id"]
    print(organization_id)
    checkValid = EventService.checkValid(organization_id, eid)
    if checkValid:
        return JsonResponse({"valid": True})
    else:
        return JsonResponse({"valid": False})

class TestAPI(APIView):
    def get(self, request):
        if "_auth_user_id" in request.session:
            return Response(
                {
                    "id": request.session["_auth_user_id"],
                    "role": request.session["role"],
                },
                status=status.HTTP_200_OK,
            )
        return Response({"role": None}, status=status.HTTP_401_UNAUTHORIZED)


class UpdateOrganizerStatus(APIView):
    def put(self, request):
        organizerAdminService = OrganizerAdminService()
        success = organizerAdminService.updateOrganizer(
            organizer_uuid=request.data["user"],
            status=request.data["validOrganisation"],
        )
        if success:
            adminLogger.warning("Organizer {organizer_uuid} updated ... okay try this one later")
            return Response(
                {"message": "Organizer status updated successfully."},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"message": "Failed to update organizer status."},
                status=status.HTTP_400_BAD_REQUEST,
            )


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

class EventParticipantAPI(APIView):
    def get(self, request, event_id):
        organization_id = request.session["_auth_user_id"]
        eventsByOrg = EventService.getParticipantsByEvent(organization_id, event_id)
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

        if request.data["organization"]:
            success, errors = AccountService.createOrganisation(data)
        else:
            birthday = datetime.strptime(
                request.data["birthday"], "%Y-%m-%d"
            ).date()
            success, errors = AccountService.createNormalUser(data, birthday)
        if success != False:
            recaptcha_response = request.data["recaptchaValue"]
            verification_data = {"secret": RECAPTCHA_KEY, "response": recaptcha_response}
            response = requests.post(
                "https://www.google.com/recaptcha/api/siteverify", data=verification_data
            )
            recaptcha_result = response.json()
            print(recaptcha_result)
            if not recaptcha_result["success"]:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(status=status.HTTP_200_OK)
        else:
            print(errors)
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateUserAPIView(APIView):
    def put(self, request):
        emergencySuccess=False
        success=False
        nokUpdateSuccess=False

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
        # print("this is emergency before ")
        emergency = EmergencyContactService.getContactById(id)
        if emergency:
            nokData = {
                "name": request.data["nokName"],
                "relationship": request.data["nokRelationship"],
                "phoneNum": request.data["nokPhone"],
            }
            nokUpdateSuccess = NokService.updateNok(nokData, emergency["nok"])
            success = UserService.updateUserProfile(data, id)
        else:
            # create a nok here pls
            with transaction.atomic():
                newNok = NokService.createNok(request.data["nokName"],request.data["nokRelationship"],request.data["nokPhone"])
                emergencySuccess = EmergencyContactService.createNewContact(newNok["id"],id)
                # print(newNok)
                # print(emergencySuccess)        
        if ((success and nokUpdateSuccess) or emergencySuccess):        
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class GetProfileDetailsAPIView(APIView):
    def get(self, request):
        data = {}
        id = UUID(request.session["_auth_user_id"]).hex
        # this part use the session to get id
        valid = UserService.getUserById(id)

        data["profile"] = valid
        emergency = EmergencyContactService.getContactById(id)
        if emergency:
            nok = NokService.getNokById(emergency["nok"])
            data["nok"] = nok
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
        print(request.__dict__)
        username = request.data.get("username")
        password = request.data.get("password")
        authService = AuthService()
        userWithCorrectCredential = authService.authenticateUser(
            request, username, password
        )
        if userWithCorrectCredential:
            request.session["temp_id"] = str(userWithCorrectCredential.id)
            authLogger.info(f"views.Login | insert_IP_here | {{'User' : '{username}', 'credentials' : 'VALID'}}") #relook message later
            return Response({"detail": "Credentials are correct"}, status=200)
        
        authLogger.info(f"views.Login | insert_IP_here | {{'User' : '{username}', 'credentials' : 'INVALID'}}") #relook message later
        return Response({"detail": "Invalid credentials."}, status=401)


class GetOTP(APIView):
    def post(self, request):
        self.authService = AuthService()
        id = request.session["temp_id"]
        isOtpSent = self.authService.generateOTP(id)
        if isOtpSent:
            return Response({"detail": "Credentials are correct"}, status=200)
        return Response({"detail": "Invalid credentials."}, status=401)


class VerifyOtp(APIView):
    def post(self, request):
        self.authService = AuthService()
        otp = request.data.get("OTP")
        uuid = request.session["temp_id"]
        isVerifiedUser = self.authService.verifyOTP(uuid = uuid ,otpToken = otp)
        if isVerifiedUser :
            loginUser = self.authService.LoginUser(request)
            if loginUser :
                request.session["role"] = AccountService.getUserRole(loginUser.id)
                return Response({"detail": "OTP is Correct"}, status=200)
        return Response({"detail": "Something went wrong"}, status=401)


class Logout(APIView):
        def post(self,request):
            AuthService.logout(request)
            return Response({"detail": "LOGOUT SUCCESS"}, status=200)


class ChangePassword(APIView):
    def post(self,request):
        auth = AuthService()
        user = auth.getUserBySessionRequest(request)
        if user:
            auth.generateOTP(user.id)
            return Response({"detail": "OTP HAS BEEN Sent"}, status=200)
        return Response({"detail": "Invalid Permission"}, status=401)

    def put(self, request):
        
        try:
            currentPassword = request.data.get("currentPassword")
            newPasswordConfirmation = request.data.get("newPasswordConfirmation")
            newPassword = request.data.get("newPassword")
            otp = request.data.get("OTP")
            if None in [currentPassword, newPasswordConfirmation, newPassword, otp]:
                return Response({"detail": "Missing fields"}, status=status.HTTP_400_BAD_REQUEST)

            authService = AuthService()
            currentUser = authService.getUserBySessionRequest(request)
            
            if newPassword != newPasswordConfirmation:
                return Response({"detail": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)
            if currentUser is None:
                return Response({"detail": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

            userWithCorrectCredential = authService.authenticateUser(request, currentUser.email, currentPassword)
            
            if userWithCorrectCredential and authService.verifyOTP(userWithCorrectCredential.id,otp):
                if authService.changePassword(userWithCorrectCredential, newPassword):
                    return Response({"detail": "Password changed successfully"}, status=status.HTTP_200_OK)
                
            return Response({"detail": "Invalid current password"}, status=status.HTTP_401_UNAUTHORIZED)
            
        except Exception as e:
            return Response({"detail": f"Something went wrong: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ResetPassword(APIView):
    def post(self,request):
        email = request.data.get("email")
        auth = AuthService()
        auth.requestOTPFroMEmail(email)
        return Response({"detail": "email should be sent"}, status=200)

    def put(self,request):
        otp= request.data.get("OTP")
        email = request.data.get("email")
        newPasswordConfirmation = request.data.get("newPasswordConfirmation")
        newPassword = request.data.get("newPassword")
        auth = AuthService()
        if newPassword != newPasswordConfirmation:
            return Response({"detail": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)
        user = auth.getUserByEmail(email)
        if user:
            isOTPCorrect = auth.verifyOTP(user.id,otp)
            if isOTPCorrect:
                if auth.changePassword(user, newPassword):
                    return Response({"detail": "Password changed successfully"}, status=status.HTTP_200_OK)
        return Response({"detail": "Something went wrong"}, status=status.HTTP_401_UNAUTHORIZED)
