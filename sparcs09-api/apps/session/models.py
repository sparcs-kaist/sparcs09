from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='profile')
    phone = models.CharField(max_length=100, default="")
    address = models.CharField(max_length=500, default="")
    kakao_id = models.CharField(max_length=100, default="")
    terms_agreed = models.BooleanField(default=False)
