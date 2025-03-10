from django.db import models
from django.conf import settings

# Create your models here.


#USER ACCOUNT MODEL
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'Profile for user {self.user.username}'
    
    