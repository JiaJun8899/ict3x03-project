from django.db import models

class NOK(models.Model):
    name = models.CharField(max_length=100)
    relationship = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    age= models.CharField(max_length=15, blank=True, default="15")
    # One-to-One relationship with NormalUser
    normal_user = models.OneToOneField(
        'NormalUser', 
        on_delete=models.CASCADE, 
        primary_key=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'api'

