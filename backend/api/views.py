from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.services import *
from django.core.files.uploadedfile import InMemoryUploadedFile
from datetime import datetime
from uuid import UUID
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
import requests
from dotenv import load_dotenv
from django.db import transaction
import hashlib
from django.utils.html import escape
import re

import logging

adminLogger = logging.getLogger("backend.api.views.admin")
authLogger = logging.getLogger("backend.api.views.auth")
registerLogger = logging.getLogger("backend.api.views.register")
generalLogger = logging.getLogger("backend.api.views.general")

load_dotenv()

def get_client_ip_address(request):
    req_headers = request.META
    x_forwarded_for_value = req_headers.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for_value:
        ip_addr = x_forwarded_for_value.split(',')[-1].strip()
    else:
        ip_addr = req_headers.get('REMOTE_ADDR')
    return ip_addr

def sanitiseString(stringInput):
    return escape(stringInput.strip())

def checkDataValid(data):
    pattern = r"^[a-zA-Z0-9 ]*$"
    keysAlnum = ["first_name", "last_name", "nric"]
    for key, value in data.items():
        if key in keysAlnum:
            if not re.match(pattern, value.strip()):
                return False
    return True

def organiserCheck(role):
    if role == "Organizer":
        return True
    return False

class CheckValidEventOrg(APIView):
    def get(self, request, eid):
        organization_id = request.session["_auth_user_id"]
        checkValid = EventService.checkValid(organization_id, eid)
        if checkValid:
            return Response({"valid": True}, status=status.HTTP_200_OK)
        else:
            return Response({"valid": False}, status=status.HTTP_403_FORBIDDEN)

class CheckAuth(APIView):
    def get(self, request):
        if "_auth_user_id" and "role" in request.session:
            return Response(
                {
                    "id": request.session["_auth_user_id"],
                    "role": request.session["role"],
                },
                status=status.HTTP_200_OK,
            )
        return Response({"role": None}, status=status.HTTP_401_UNAUTHORIZED)


class EventAPI(APIView):
    def get(self, request):
        """Gets all the events"""
        EventService.updateEventStatus()
        allEvents = EventService.getAllEvent()
        return Response(allEvents, status=status.HTTP_200_OK)


class EventsByOrganizationAPI(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get(self, request):
        if not organiserCheck(request.session["role"]):
            return Response({"error": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        organization_id = request.session["_auth_user_id"]
        EventService.updateEventStatus()
        eventsByOrg = EventService.getEventByOrg(organization_id)
        return Response(eventsByOrg, status=status.HTTP_200_OK)

    def post(self, request):
        """Create Event"""
        organization_id = request.session["_auth_user_id"]
        clientIP = get_client_ip_address(request)
        if not organiserCheck(request.session["role"]):
            return Response({"error": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        try:
            if request.data["eventImage"].size > 2 * 1024 * 1024:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            data = {
                "eventName": sanitiseString(request.data["eventName"]),
                "startDate": request.data["startDate"],
                "endDate": request.data["endDate"],
                "noVol": request.data["noVol"],
                "eventDesc": sanitiseString(request.data["eventDesc"]),
                "eventImage": request.data["eventImage"],
            }
        except:
            return Response({'errors':"Some Fields are Missing"}, status=status.HTTP_400_BAD_REQUEST)
        success, errors = EventService.createEvent(data, organization_id)
        if success:
            eventName = sanitiseString(request.data["eventName"])
            generalLogger.info(f"views.EventsByOrganizationAPI.post {clientIP} {{'organizer' : '{organization_id}', 'event' : '{eventName}', 'message' : 'Created event.'}}")
            return Response(status=status.HTTP_200_OK)
        else:
            generalLogger.info(f"views.EventsByOrganizationAPI.post {clientIP} {{'organizer' : '{organization_id}', 'message' : 'Failed to create event'}}")
            print(errors)
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        """Update event"""
        organization_id = request.session["_auth_user_id"]
        checkValid = EventService.checkValid(
            organization_id, request.data["eid"]
        )  # Should be able to remove and just use under updateEvent
        eid = request.data["eid"]
        clientIP = get_client_ip_address(request)
        if checkValid:
            data = {}
            for key, value in request.data.items():
                if key == "eventImage" and not isinstance(value, InMemoryUploadedFile):
                    pass
                else:
                    if key == "eventName" or key == "eventDesc":
                        value = sanitiseString(value)
                    data[key] = value
            if "eventImage" in data:
                if data["eventImage"].size > 2 * 1024 * 1024:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            success, errors = EventService.updateEvent(data, request.data["eid"])
            if success:
                generalLogger.info(f"views.EventsByOrganizationAPI.put {clientIP} {{'organizer' : '{organization_id}', 'event' : '{eid}', 'message' : 'Updated event.'}}")
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        generalLogger.info(f"views.EventsByOrganizationAPI.put {clientIP} {{'organizer' : '{organization_id}', 'event' : '{eid}', 'message' : 'Failed to update event.'}}")
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request):
        """Delete Event and Mapping"""
        organization_id = request.session["_auth_user_id"]
        checkValid = EventService.checkValid(organization_id, request.data["eid"])
        eid = request.data["eid"]
        clientIP = get_client_ip_address(request)
        if checkValid:
            success = EventService.deleteEvent(request.data["eid"])
            success = True
            if success:
                generalLogger.info(f"views.EventsByOrganizationAPI.delete {clientIP} {{'organizer' : '{organization_id}', 'event' : '{eid}', 'message' : 'Deleted event.'}}")
                return Response(status=status.HTTP_200_OK)
        generalLogger.warning(f"views.EventsByOrganizationAPI.delete {clientIP} {{'organizer' : '{organization_id}', 'event' : '{eid}', 'message' : 'Failed to delete event.'}}")
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class EventSingleByOrganizationAPI(APIView):
    def get(self, request, event_id):
        organization_id = request.session["_auth_user_id"]
        if not organiserCheck(request.session["role"]):
            return Response({"error": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        EventService.updateParticipants(event_id)
        eventsByOrg = EventService.getEventByID(organization_id, event_id)
        return Response(eventsByOrg, status=status.HTTP_200_OK)

class EventParticipantAPI(APIView):
    def get(self, request, event_id):
        organization_id = request.session["_auth_user_id"]
        eventsByOrg = EventService.getParticipantsByEvent(organization_id, event_id)
        return Response(eventsByOrg, status=status.HTTP_200_OK)

class RegisterUserAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        if "SECRET_KEY" in request.data:
            inputKey = request.data["SECRET_KEY"]
            sha256 = hashlib.sha256()
            sha256.update(inputKey.encode('utf-8'))
            hashed_input_key = sha256.hexdigest()
            key = os.getenv("TEST_KEY", os.environ.get("TEST_KEY"))
            if hashed_input_key == key:
                RECAPTCHA_KEY = os.getenv("RECAPTCHA_KEY_TEST", os.environ.get("RECAPTCHA_KEY_TEST"))
        else:
            RECAPTCHA_KEY = os.getenv("RECAPTCHA_KEY", os.environ.get("RECAPTCHA_KEY"))
        try:
            recaptcha_response = request.data["recaptchaValue"]
            verification_data = {"secret": RECAPTCHA_KEY, "response": recaptcha_response}
            response = requests.post("https://www.google.com/recaptcha/api/siteverify", data=verification_data)
            recaptcha_result = response.json()
            clientIP = get_client_ip_address(request)
            if not recaptcha_result["success"]:
                registerLogger.warning(f"views.RegisterUserAPIView {clientIP} {{'message' : 'Invalid registration attempt.'}}")
                return Response(status=status.HTTP_400_BAD_REQUEST)
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
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if not checkDataValid(data):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if request.data["organization"]:
            success, errors, user_id = AccountService.createOrganisation(data)
        else:
            birthday = datetime.strptime(
                request.data["birthday"], "%Y-%m-%d"
            ).date()
            success, errors, user_id = AccountService.createNormalUser(data, birthday)
        if success:
            if request.data["organization"]:
                registerLogger.info(f"views.RegisterUserAPIView {clientIP} {{'user' : '{user_id}', 'accType' : 'Organizer', 'message' : 'Account created.'}}")
            else:
                registerLogger.info(f"views.RegisterUserAPIView {clientIP} {{'user' : '{user_id}', 'accType' : 'GenericUser', 'message' : 'Account created.'}}")
            return Response(status=status.HTTP_200_OK)
        else:
            registerLogger.warning(f"views.RegisterUserAPIView {clientIP} {{'message' : '{errors}'}}")
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateUserAPIView(APIView):
    def put(self, request):
        emergencySuccess=False
        success=False
        nokUpdateSuccess=False
        id = UUID(request.session["_auth_user_id"]).hex
        role = request.session["role"]
        if role == "Organizer":
            valid = OrganizerAdminService.getOrgById(id)
        else:
            valid = UserService.getUserById(id)
        if valid != None:
            data = {
                "first_name": request.data["first_name"],
                "last_name": request.data["last_name"],
                "email": request.data["email"],
                "phoneNum": request.data["phoneNum"]
            }
            if not checkDataValid(data):
                return Response(status=status.HTTP_400_BAD_REQUEST)
        success,userErrors = UserService.updateUserProfile(data, id)
        if not success:
            return Response(userErrors,status=status.HTTP_400_BAD_REQUEST)
        if role == "Organizer" and success:
            return Response(status=status.HTTP_200_OK)
        if success:
            emergency = EmergencyContactService.getContactById(id)
            if emergency:
                nokData = {
                "name": request.data["nokName"],
                "relationship": request.data["nokRelationship"],
                "phoneNum": request.data["nokPhone"],
                }
                if not checkDataValid(nokData):
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                nokUpdateSuccess, errors = NokService.updateNok(nokData, emergency["nok"])            
            else:
                with transaction.atomic():
                    newNok = NokService.createNok(request.data["nokName"],request.data["nokRelationship"],request.data["nokPhone"])
                    emergencySuccess, errors = EmergencyContactService.createNewContact(newNok["id"],id)     
            if ((success and nokUpdateSuccess) or emergencySuccess):        
                return Response(status=status.HTTP_200_OK)
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class GetProfileDetailsAPIView(APIView):
    def get(self, request):
        data = {}
        id = UUID(request.session["_auth_user_id"]).hex
        role = request.session["role"]
        if role == "Organizer":
            data["profile"] = OrganizerAdminService.getOrgById(id)
            return Response(data, status=status.HTTP_200_OK)
        if role =="Normal":
            data["profile"] = UserService.getUserById(id)
            emergency = EmergencyContactService.getContactById(id)
            if emergency:
                nok = NokService.getNokById(emergency["nok"])
                data["nok"] = nok
            return Response(data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


class SignUpEventAPIView(APIView):
    def post(self, request):
        id = UUID(request.session["_auth_user_id"]).hex
        eid = request.data['eid']
        validUser = UserService.getUserById(id)
        validEvent = EventCommonService.getEventByID(request.data["eid"])
        user_id = request.session["_auth_user_id"]
        clientIP = get_client_ip_address(request)
        if validUser != None and validEvent["eventStatus"] == "open" and validEvent != None:
            data = {"event": eid, "participant": id}
            success = UserService.signUpEvent(data=data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST) 
        if success:
            generalLogger.info(f"views.SignUpEventAPIView {clientIP} {{'user' : '{user_id}', 'event' : '{eid}', 'message' : 'Signed up for event.'}}")
            return Response(status=status.HTTP_200_OK)
        generalLogger.warning(f"views.SignUpEventAPIView {clientIP} {{'user' : '{user_id}', 'event' : '{eid}', 'message' : 'Failed to sign up for event.'}}")
        return Response(status=status.HTTP_400_BAD_REQUEST)


class CancelSignUpEventAPIView(APIView):
    def delete(self, request):
        id = UUID(request.session["_auth_user_id"]).hex
        validUser = UserService.getUserById(id)
        validEvent = EventCommonService.getEventByID(request.data["eid"])
        user_id = request.session["_auth_user_id"]
        eid = request.data['eid']
        clientIP = get_client_ip_address(request)
        if validUser != None and validEvent != None:
            data = {"event": request.data["eid"], "participant": id}
            success = UserService.cancelSignUpEvent(data=data)
            if success:
                generalLogger.info(f"views.CancelSignUpEventAPIView {clientIP} {{'user' : '{user_id}', 'event' : '{eid}', 'message' : 'Canceled event sign up.'}}")
                return Response(status=status.HTTP_200_OK)
        generalLogger.warning(f"views.CancelSignUpEventAPIView {clientIP} {{'user' : '{user_id}', 'event' : '{eid}', 'message' : 'Failed to canceled event sign up.'}}")
        return Response(status=status.HTTP_400_BAD_REQUEST)


class SearchEvents(APIView):
    def post(self, request):
        events = EventService.searchEvent(request.data["name"])
        if events != None:
            user_id = request.session["_auth_user_id"]
            search = request.data["name"]
            clientIP = get_client_ip_address(request)
            generalLogger.info(f"views.SearchEvents {clientIP} {{'user' : '{user_id}', 'message' : '{search}'}}")
            return Response(events, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class GetPastEventsByParticipant(APIView):
    def get(self, request):
        id = UUID(request.session["_auth_user_id"]).hex
        eventParticipantService = EventParticipantService()
        eventService = EventService()
        events = eventParticipantService.getParticipatedEvents(id)
        pastEvent = []
        if events != None:        
            # need to check if past current date
            for event in events:
                if(eventService.checkPastEvent(event["event"])):
                    pastEvent.append(eventService.userGetEventById(event["event"]))
            return Response(pastEvent, status=status.HTTP_200_OK)
        else:
            return Response({"Failed to participated events."}, status=status.HTTP_400_BAD_REQUEST,)

class GetUpcomingEventsByParticipant(APIView):
    def get(self, request):
        id = UUID(request.session["_auth_user_id"]).hex
        eventParticipantService = EventParticipantService()
        eventService = EventService()
        events = eventParticipantService.getParticipatedEvents(id)
        upcomingEvent = []
        if events != None:        
            for event in events:
                if(not eventService.checkPastEvent(event["event"])):
                    upcomingEvent.append(eventService.userGetEventById(event["event"]))
            return Response(upcomingEvent, status=status.HTTP_200_OK)
        else:
            return Response({"Failed to upcoming events."},status=status.HTTP_400_BAD_REQUEST,)


class GetEvent(APIView):
    def get(self, request, eid):
        eventService = EventService()
        events = eventService.userGetEventById(eid)
        if events != None:
            # Assuming that the returned organizers is a QuerySet or list of Organizer instances
            return Response({"data": events})
        else:
            return Response({"Failed to retrieve event."},status=status.HTTP_500_INTERNAL_SERVER_ERROR,)

class Login(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        authService = AuthService()
        userWithCorrectCredential = authService.authenticateUser(
            request, username, password
        )
        clientIP = get_client_ip_address(request)
        if userWithCorrectCredential and AccountService.getUserRole(userWithCorrectCredential.id):
            request.session["temp_id"] = str(userWithCorrectCredential.id)
            user_id = userWithCorrectCredential.id
            authLogger.info(f"views.Login {clientIP} {{'user' : '{user_id}', 'credentials' : 'VALID'}}") 
            return Response({"detail": "Credentials are correct"}, status=status.HTTP_200_OK)
        
        authLogger.info(f"views.Login {clientIP} {{'user' : '{None}', 'credentials' : 'INVALID'}}")
        return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)


class GetOTP(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        self.authService = AuthService()
        uuid = request.session.get("temp_id", None)
        if uuid != None:
            isOtpSent = self.authService.generateOTP(uuid)
            if isOtpSent:
                return Response({"detail": "Credentials are correct"}, status=status.HTTP_200_OK)
        return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)


class VerifyOtp(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        self.authService = AuthService()
        otp = request.data.get("OTP")
        uuid = request.session.get("temp_id", None)
        clientIP = get_client_ip_address(request)
        if uuid != None:
            isVerifiedUser = self.authService.verifyOTP(uuid = uuid ,otpToken = otp)
            if isVerifiedUser :
                del request.session['temp_id']
                loginUser = self.authService.LoginUser(request,uuid)
                if loginUser :
                    request.session["role"] = AccountService.getUserRole(loginUser.id)
                    authLogger.info(f"views.VerifyOtp {clientIP} {{'user' : '{uuid}', 'otp' : 'VALID'}}") 
                    return Response({"detail": "OTP is Correct"}, status=status.HTTP_200_OK)
        authLogger.info(f"views.VerifyOtp {clientIP} {{'user' : '{uuid}', 'otp' : 'INVALID'}}")
        return Response({"detail": "Something went wrong"}, status=status.HTTP_401_UNAUTHORIZED)


class Logout(APIView):
    def post(self,request):
        user_id = request.session["_auth_user_id"]
        clientIP = get_client_ip_address(request)
        AuthService.logout(request)
        authLogger.info(f"views.Logout {clientIP} {{'user' : '{user_id}', 'message' : 'Logged out.'}}")
        return Response({"detail": "LOGOUT SUCCESS"}, status=status.HTTP_200_OK)


class ChangePassword(APIView):
    def post(self,request):
        auth = AuthService()
        user = auth.getUserBySessionRequest(request)
        if user:
            if auth.generateOTP(user.id):
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
            user_id = request.session["_auth_user_id"]

            clientIP = get_client_ip_address(request)
            if currentUser is None:
                authLogger.warning(f"views.ChangePassword {clientIP} {{'user' : '{user_id}', 'message' : 'Unauthorized attempt to change password.'}}")
                return Response({"detail": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

            if newPassword != newPasswordConfirmation:
                return Response({"detail": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)

            userWithCorrectCredential = authService.authenticateUser(request, currentUser.email, currentPassword)
            if userWithCorrectCredential and authService.verifyOTP(userWithCorrectCredential.id,otp) and AccountService.getUserRole(userWithCorrectCredential.id):
                isSuccessful, errorMessages = authService.changePassword(userWithCorrectCredential, newPassword)
                if isSuccessful:
                    authLogger.warning(f"views.ChangePassword {clientIP} {{'user' : '{user_id}', 'message' : 'Password changed successfully.'}}")
                    return Response({"detail": "Password changed successfully"}, status=status.HTTP_200_OK)
                else:
                    error = str(errorMessages)
                    authLogger.warning(f"views.ChangePassword {clientIP} {{'user' : '{user_id}', 'message' : 'Password changed unsuccessful.', 'error' : '{error}' }}")
                    return Response({"detail": str(errorMessages)}, status=status.HTTP_400_BAD_REQUEST)
            authLogger.warning(f"views.ChangePassword {clientIP} {{'user' : '{user_id}', 'message' : 'Invalid current password.'}}")    
            return Response({"detail": "Invalid current password"}, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            return Response({"detail": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ResetPassword(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        email = request.data.get("email")
        auth = AuthService()
        user = auth.getUserByEmail(email)
        if user != None and AccountService.getUserRole(user.id):
            auth.requestOTPFroMEmail(email)
        clientIP = get_client_ip_address(request)
        authLogger.info(f"views.ResetPassword {clientIP} {{'user' : '{email}', 'message' : 'Password reset request has been sent.'}}")
        return Response({"detail": "email should be sent"}, status=status.HTTP_200_OK)

    def put(self,request):
        otp= request.data.get("OTP")
        email = request.data.get("email")
        newPasswordConfirmation = request.data.get("newPasswordConfirmation")
        newPassword = request.data.get("newPassword")
        auth = AuthService()
        if newPassword != newPasswordConfirmation:
            return Response({"detail": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)
        user = auth.getUserByEmail(email)
        clientIP = get_client_ip_address(request)
        if user != None and AccountService.getUserRole(user.id):
            isOTPCorrect = auth.verifyOTP(user.id,otp)
            if isOTPCorrect:
                if auth.changePassword(user, newPassword):
                    authLogger.warning(f"views.ResetPassword {clientIP} {{'user' : '{email}', 'message' : 'Password reset successfully.'}}")
                    return Response({"detail": "Password changed successfully"}, status=status.HTTP_200_OK)
        return Response({"detail": "Something went wrong"}, status=status.HTTP_401_UNAUTHORIZED)
