from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
import uuid
from api.managers import GenericUserManager
from django.core.validators import MinLengthValidator

class GenericUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nricRegex = RegexValidator(
        regex=r'^[A-Za-z]\d{7}[A-Za-z]$',
        message="NRIC must start with an alphabet character, followed by 8 digits, and ending with an alphabet character."
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
    nric = models.CharField(max_length=9, null=False, blank=False,validators=[nricRegex, MinLengthValidator(9)])
    genericUserManager = GenericUserManager()
    class Meta:
        app_label = "api"

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phoneNum', 'nric']

    def __str__(self):
        return str(self.first_name) + str(self.last_name)
 
    def save(self, *args, **kwargs):
        for field in self._meta.fields:
            if isinstance(field, (models.CharField, models.TextField)):
                value = getattr(self, field.name, None)
                if value == "": 
                    raise ValueError(f"{field.name} : {value} must have more than 5 characters")
                elif value == None:
                    raise ValueError(f"value cannot be none ")
        super().save(*args, **kwargs)

