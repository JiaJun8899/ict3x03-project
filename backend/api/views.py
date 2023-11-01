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

class CheckValidEventOrg(APIView):
    def get(self, request, eid):
        organization_id = request.session["_auth_user_id"]
        print(organization_id)
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
        print(allEvents)
        return Response(allEvents, status=status.HTTP_200_OK)


class EventsByOrganizationAPI(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get(self, request):
        organization_id = request.session["_auth_user_id"]
        EventService.updateEventStatus()
        eventsByOrg = EventService.getEventByOrg(organization_id)
        return Response(eventsByOrg, status=status.HTTP_200_OK)

    def post(self, request):
        """Create Event"""
        organization_id = request.session["_auth_user_id"]
        data = {
            "eventName": sanitiseString(request.data["eventName"]),
            "startDate": request.data["startDate"],
            "endDate": request.data["endDate"],
            "noVol": request.data["noVol"],
            "eventDesc": sanitiseString(request.data["eventDesc"]),
            "eventImage": request.data["eventImage"],
        }
        success = EventService.createEvent(data, organization_id)
        if success:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        """Update event"""
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
                    if key == "eventName" or key == "eventDesc":
                        value = sanitiseString(value)
                    data[key] = value
            data["eventStatus"] = "open"
            print(data)
            success = EventService.updateEvent(data, request.data["eid"])
            if success:
                return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request):
        """Delete Event and Mapping"""
        # print(request.data)
        organization_id = request.session["_auth_user_id"]
        checkValid = EventService.checkValid(organization_id, request.data["eid"])
        if checkValid:
            success = EventService.deleteEvent(request.data["eid"])
            success = True
            if success:
                return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


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
        recaptcha_response = request.data["recaptchaValue"]
        verification_data = {"secret": RECAPTCHA_KEY, "response": recaptcha_response}
        response = requests.post("https://www.google.com/recaptcha/api/siteverify", data=verification_data)
        recaptcha_result = response.json()
        print(recaptcha_result)
        if not recaptcha_result["success"]:
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
        if not checkDataValid(data):
            registerLogger.info(f"views.RegisterUserAPIView insert_IP_here {{'message' : 'Invalid registration attempt.'}}")
            return Response(status=status.HTTP_400_BAD_REQUEST)
        print(data)
        if request.data["organization"]:
            success, errors = AccountService.createOrganisation(data)
        else:
            birthday = datetime.strptime(
                request.data["birthday"], "%Y-%m-%d"
            ).date()
            success, errors = AccountService.createNormalUser(data, birthday)
        if success:
            username = request.data["email"]
            if request.data["organization"]:
                registerLogger.info(f"views.RegisterUserAPIView insert_IP_here {{'user' : '{username}', 'accType' : 'Organizer', 'message' : 'Account created.'}}")
            else:
                registerLogger.info(f"views.RegisterUserAPIView insert_IP_here {{'user' : '{username}', 'accType' : 'GenericUser', 'message' : 'Account created.'}}")
            return Response(status=status.HTTP_200_OK)
        else:
            print(errors)
            registerLogger.info(f"views.RegisterUserAPIView insert_IP_here {{'message' : '{errors}'}}")
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
            if not checkDataValid(data):
                return Response(status=status.HTTP_400_BAD_REQUEST)
        # print("this is emergency before ")
        success = UserService.updateUserProfile(data, id)
        emergency = EmergencyContactService.getContactById(id)
        if emergency:
            nokData = {
                "name": request.data["nokName"],
                "relationship": request.data["nokRelationship"],
                "phoneNum": request.data["nokPhone"],
            }
            if not checkDataValid(nokData):
                return Response(status=status.HTTP_400_BAD_REQUEST)
            nokUpdateSuccess = NokService.updateNok(nokData, emergency["nok"])            
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
        eid = request.data['eid']
        validUser = UserService.getUserById(id)
        validEvent = EventCommonService.getEventByID(request.data["eid"])
        print(validEvent)
        if validUser != None and validEvent["eventStatus"] == "open" and validEvent != None:
            data = {"event": eid, "participant": id}
            success = UserService.signUpEvent(data=data)
            print(success)
        if success:
            username = request.user.get_username()
            generalLogger.info(f"views.SignUpEventAPIView insert_IP_here {{'user' : '{username}', 'event' : '{eid}', 'message' : 'Signed up for event.'}}")
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class CancelSignUpEventAPIView(APIView):
    def delete(self, request):
        id = UUID(request.session["_auth_user_id"]).hex
        validUser = UserService.getUserById(id)
        validEvent = EventCommonService.getEventByID(request.data["eid"])
        if validUser != None and validEvent != None:
            data = {"event": request.data["eid"], "participant": id}
            success = UserService.cancelSignUpEvent(data=data)
            if success:
                username = request.user.get_username()
                eid = request.data['eid']
                generalLogger.info(f"views.CancelSignUpEventAPIView insert_IP_here {{'user' : '{username}', 'event' : '{eid}', 'message' : 'Canceled event sign up.'}}")
                return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class SearchEvents(APIView):
    def post(self, request):
        events = EventService.searchEvent(request.data["name"])
        if events != None:
            username = request.user.get_username()
            search = request.data["name"]
            generalLogger.info(f"views.SearchEvents insert_IP_here {{'user' : '{username}', 'message' : '{search}'}}")
            return Response(events, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
class GetPastEvents(APIView):
    def post(self, request):
        events = EventService.searchEvent(request.data["name"])
        if events != None:
            return Response(events, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
        
class GetUpcomingEvents(APIView):
    def post(self, request):
        events = EventService.searchEvent(request.data["name"])
        if events != None:
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
        print(request.__dict__)
        username = request.data.get("username")
        password = request.data.get("password")
        authService = AuthService()
        userWithCorrectCredential = authService.authenticateUser(
            request, username, password
        )
        if userWithCorrectCredential:
            request.session["temp_id"] = str(userWithCorrectCredential.id)
            authLogger.info(f"views.Login insert_IP_here {{'user' : '{username}', 'credentials' : 'VALID'}}") 
            return Response({"detail": "Credentials are correct"}, status=status.HTTP_200_OK)
        
        authLogger.info(f"views.Login insert_IP_here {{'user' : '{username}', 'credentials' : 'INVALID'}}")
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
        username = request.user.get_username()
        self.authService = AuthService()
        otp = request.data.get("OTP")
        uuid = request.session.get("temp_id", None)
        if uuid != None:
            del request.session['temp_id']
            isVerifiedUser = self.authService.verifyOTP(uuid = uuid ,otpToken = otp)
            if isVerifiedUser :
                loginUser = self.authService.LoginUser(request,uuid)
                if loginUser :
                    request.session["role"] = AccountService.getUserRole(loginUser.id)
                    authLogger.info(f"views.VerifyOtp insert_IP_here {{'user' : '{username}', 'otp' : 'VALID'}}") 
                    return Response({"detail": "OTP is Correct"}, status=status.HTTP_200_OK)
        authLogger.info(f"views.VerifyOtp insert_IP_here {{'user' : '{username}', 'otp' : 'INVALID'}}")
        return Response({"detail": "Something went wrong"}, status=status.HTTP_401_UNAUTHORIZED)


class Logout(APIView):
    def post(self,request):
        username = request.user.get_username()
        AuthService.logout(request)
        authLogger.info(f"views.Logout insert_IP_here {{'user' : '{username}', 'message' : 'Logged out.'}}")
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
            if currentUser is None:
                return Response({"detail": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

            if newPassword != newPasswordConfirmation:
                return Response({"detail": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)

            userWithCorrectCredential = authService.authenticateUser(request, currentUser.email, currentPassword)
            if userWithCorrectCredential and authService.verifyOTP(userWithCorrectCredential.id,otp):
                if authService.changePassword(userWithCorrectCredential, newPassword):
                    username = request.user.get_username()
                    authLogger.info(f"views.ChangePassword insert_IP_here {{'user' : '{username}', 'message' : 'Password changed successfully.'}}")
                isSuccessful, errorMessages = authService.changePassword(userWithCorrectCredential, newPassword)
                if isSuccessful:
                    return Response({"detail": "Password changed successfully"}, status=status.HTTP_200_OK)
                else:
                    return Response({"detail": str(errorMessages)}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"detail": "Invalid current password"}, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            return Response({"detail": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ResetPassword(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        email = request.data.get("email")
        auth = AuthService()
        auth.requestOTPFroMEmail(email)
        authLogger.info(f"views.ResetPassword insert_IP_here {{'user' : '{email}', 'message' : 'Password reset request has been sent.'}}")
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
        if user:
            isOTPCorrect = auth.verifyOTP(user.id,otp)
            if isOTPCorrect:
                if auth.changePassword(user, newPassword):
                    authLogger.info(f"views.ResetPassword insert_IP_here {{'user' : '{email}', 'message' : 'Password reset successfully.'}}")
                    return Response({"detail": "Password changed successfully"}, status=status.HTTP_200_OK)
        return Response({"detail": "Something went wrong"}, status=status.HTTP_401_UNAUTHORIZED)
