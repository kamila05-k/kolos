from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from .managers import CustomUserManager
from django.utils.timezone import now, timedelta

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    success = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    failed_attempts = models.IntegerField(default=0)
    is_locked = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        # Return only the email
        return self.email

    def lock_account(self):
        if self.failed_attempts >= 4:
            self.is_locked = True
            self.save()

    def reset_failed_attempts(self):
        self.failed_attempts = 0
        self.save()

    def last_attempt(self):
        return self.timestamp

    last_attempt.admin_order_field = 'timestamp'
    last_attempt.short_description = 'Последняя попытка'

