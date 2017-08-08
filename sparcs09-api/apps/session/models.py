from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    """
    Represents a group of additional information for an user

    Attributes:
        user: the user
        phone: the phone number of the user
        address: the address of the user
        kakao_id: the KakaoTalk id of the user
        terms_agreed: the flags that denotes this user agreed to our terms
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='profile')
    phone = models.CharField(max_length=100, default="")
    address = models.CharField(max_length=500, default="")
    kakao_id = models.CharField(max_length=100, default="")
    terms_agreed = models.BooleanField(default=False)
