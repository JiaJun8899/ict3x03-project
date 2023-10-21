from django.contrib.auth import authenticate, login
from django_otp.plugins.otp_email.models import  EmailDevice
from api.models.GenericUser import GenericUser
from django.contrib.auth import logout

class AuthService:

    def __init__(self):
        self.user = None
        self.emailDevice = EmailDevice()

    def authenticateUser(self, request, username, password):
        self.user = authenticate(username=username, password=password)
        if self.user:
            self.emailDevice = EmailDevice.objects.get_or_create(user=self.user, email=self.user.email,name="EMAIL")[0]
        return self.user

    def generateOTP(self, uuid=None):
        user = self.user or self.getUserByUUID(uuid)
        if user:
            self.emailDevice = EmailDevice.objects.get_or_create(user=user, email=user.email)[0]
            self.emailDevice.generate_challenge()
            return True
        return False

    def verifyOTP(self, request , uuid,otpToken):
        user = self.user or self.getUserByUUID(uuid)
        self.emailDevice = EmailDevice.objects.get_or_create(user=user, email=user.email)[0]
        isVerified = self.emailDevice.verify_token(otpToken)
        if isVerified:
           return self.LoginUser(request)
        return None 

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
