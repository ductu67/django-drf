from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.staff.models import Staffs
from .constants import RolesType

ROLES = (
    (RolesType.ADMIN.value, 'Admin'),
    (RolesType.HR.value, 'HR')
)


class Roles(models.Model):
    name = models.CharField(max_length=30, choices=ROLES)
    status = models.BooleanField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'roles'

    def __str__(self):
        return self.name


class Users(AbstractUser):
    role = models.ForeignKey(Roles, on_delete=models.CASCADE, null=True, blank=True)
    staff = models.ForeignKey(Staffs, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    status = models.BooleanField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username


class PasswordResets(models.Model):
    token = models.CharField(max_length=512, null=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True)
    email = models.EmailField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'password_resets'

    def __str__(self):
        return self.email


class TokenUser(models.Model):
    token = models.CharField(max_length=512)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True)
