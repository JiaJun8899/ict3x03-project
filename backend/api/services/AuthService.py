from django.contrib.auth import authenticate, login

class AuthService:
    @staticmethod
    def authenticateUser(request, username, password):
        user = authenticate(request, username=username, password=password)
        if user:
            # Django's login function sets the user ID in the session
            login(request, user)
            return True
        return False

