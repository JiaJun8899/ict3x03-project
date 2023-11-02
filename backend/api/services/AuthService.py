from django.contrib.auth import authenticate, login
from api.serializer import GenericUserPasswordSerializer
from django_otp.plugins.otp_email.models import  EmailDevice
from api.models.GenericUser import GenericUser
from django.contrib.auth import logout

class AuthService:

    def __init__(self):
        self.user = None
        self.emailDevice = EmailDevice()
    

    def authenticateUser(self, request, username, password):
        self.user = authenticate(request = request, username=username, password=password)
        return self.user

    def generateChallenge(self):
        self.setEmailDevice()
        self.emailDevice.generate_challenge()

    def setEmailDevice(self):
        if self.user:
            self.emailDevice = EmailDevice.objects.get_or_create(user=self.user, email=self.user.email,name="EMAIL")[0]


    def generateOTP(self, uuid=None):
        self.user = self.getUserByUUID(uuid)
        if self.user:
            self.generateChallenge()
            return True
        return False

    def verifyOTP(self,uuid,otpToken):
        self.user = self.getUserByUUID(uuid)
        isVerified = False
        if self.user:
            self.setEmailDevice()
            if self.emailDevice and self.emailDevice.verify_is_allowed()[0]:
                isVerified = self.emailDevice.verify_token(otpToken)
        return isVerified

    def LoginUser(self, request,uuid):
        self.getUserByUUID(uuid)
        login(request, self.user)  # This will create a session
        return self.user

    def getUserByUUID(self, uuid):
        self.user = GenericUser.genericUserManager.getByUUID(uuid)
        return self.user

    @staticmethod
    def logout(request):
        return logout(request)


    def sendOTPForUpdatePassword(self,email):
        user = GenericUser.genericUserManager.get(email=email)
        if user:
            return self.generateOTP(user.id)
        return False

    def getUserBySessionRequest(self, request):
        user_id = request.session.get('_auth_user_id', None)
        if user_id is not None:
            return self.getUserByUUID(user_id)
        return None

    def changePassword(self,user,password):
        data = {"password": password}
        serializer = GenericUserPasswordSerializer(instance=user, data=data)
        if serializer.is_valid():
            serializer.update(user,data)
            return True, None  # True for success, and None for no error messages.
        else:
            return False, serializer.errors["password"]# False for failure, and the error messages.

    def requestOTPFroMEmail(self,email):
        user = GenericUser.genericUserManager.getUserByEmail(email)
        if user:
            self.generateOTP(user.id)

    def getUserByEmail(self,email):
        return GenericUser.genericUserManager.getUserByEmail(email)
