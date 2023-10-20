from django.contrib.auth import authenticate, login
from django_otp.plugins.otp_email.models import  EmailDevice
from api.models.GenericUser import GenericUser
from django.contrib.auth import logout

class AuthService:

    def __init__(self):
        self.user = None
        self.emailDevice = EmailDevice()

    def authenticateUser(self, request, username, password):
        self.user = authenticate(request, username=username, password=password)
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

    def verifyOTP(self, uuid,otpToken):
        user = self.user or self.getUserByUUID(uuid)
        self.emailDevice = EmailDevice.objects.get_or_create(user=user, email=user.email)[0]
        return self.emailDevice.verify_token(otpToken)

    def getUserByUUID(self, uuid):
        return GenericUser.genericUserManager.getByUUID(uuid)
    
    @staticmethod
    def logout(request):
        return logout(request)
