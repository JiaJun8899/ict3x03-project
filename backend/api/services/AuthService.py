from django.contrib.auth import authenticate, login
from django_otp.plugins.otp_email.models import  EmailDevice
from api.models.GenericUser import GenericUser
from django.contrib.auth import logout

class AuthService:

    def __init__(self):
        self.user = None
        self.emailDevice = EmailDevice()
    
    def setEmailDevice(self):
        if self.user != None:
            self.emailDevice = EmailDevice.objects.get_or_create(user=self.user, email=self.user.email,name="EMAIL")[0]

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
            isVerified = self.emailDevice.verify_token(otpToken)
        return isVerified

    def LoginUser(self, request):
        temp_user_id = request.session.get('temp_id', None)
        if temp_user_id is not None:
            self.user =GenericUser.genericUserManager.getByUUID(temp_user_id)
            login(request, self.user)  # This will create a session
            return self.user
        return None;

    def getUserByUUID(self, uuid):
        return GenericUser.genericUserManager.getByUUID(uuid)

    @staticmethod
    def logout(request):
        return logout(request)

    def updatePassword(self,uuid,newpassword):
        user = GenericUser.genericUserManager(uuid)
        user.set_password(newpassword)
        user.save()

    def sendOTPForUpdatePassword(self,email):
        user = GenericUser.genericUserManager.get(email=email)
        if user:
            return self.generateOTP(user.id)
        return False

    def checkPasswordValidity(self,password):
        #validate password
        return True

    def getUserBySessionRequest(self, request):
        user_id = request.session.get('_auth_user_id', None)
        if user_id is not None:
            return self.getUserByUUID(user_id)
        return None

    def changePassword(self,user,password):
        user.set_password(password)
        user.save()
        return True

    def requestOTPFroMEmail(self,email):
        user = GenericUser.genericUserManager.getUserByEmail(email)
        if user:
            self.generateOTP(user.id)

    def getUserByEmail(self,email):
        return GenericUser.genericUserManager.getUserByEmail(email)
