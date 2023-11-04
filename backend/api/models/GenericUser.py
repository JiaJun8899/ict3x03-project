from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
import uuid
from api.managers import GenericUserManager
from django.core.validators import MinLengthValidator

class GenericUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nricRegex = RegexValidator(
        regex=r'^\d{3}[A-Za-z]$',
        message="NRIC should be last 3 digits and the ending character"
    )

    phoneNumRegex = RegexValidator(
        regex=r'^[89]\d{7}$',
        message="Phone number entered is invalid"
    )
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
        blank=False
        )
    phoneNum = models.CharField(max_length=8, null=False,blank=False,validators=[MinLengthValidator(8), phoneNumRegex])
    nric = models.CharField(max_length=4, null=False, blank=False,validators=[nricRegex, MinLengthValidator(4)])
    genericUserManager = GenericUserManager()
    class Meta:
        app_label = "api"

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phoneNum', 'nric']

    def __str__(self):
        return str(self.first_name) + str(self.last_name)
 
