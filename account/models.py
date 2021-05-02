from typing import Dict
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError("User should have a username")
        if email is None:
            raise TypeError("User should have an email")
        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, username, email, password):
        if username is None:
            raise TypeError("User should have a username")
        if email is None:
            raise TypeError("User should have an email")
        if password is None:
            raise TypeError("Password should not be None")
        user = self.create_user(username, email, password)
        user.is_staff=True
        user.is_superuser=True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    phone_number = models.CharField(max_length=10, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username", )

    objects = UserManager()

    def __str__(self) -> str:
        return self.email

    def get_token(self) -> Dict:
        data = {}
        refresh = RefreshToken.for_user(self)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        self.last_login = timezone.now()
        # NOTE: This will trigger post save of user
        self.save(update_fields=["last_login"])
        return data
