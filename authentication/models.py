from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from random import randint
from django.utils import timezone

# Custom User Account

class AccountManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        print('in create user')
        if not email:
            raise ValueError('Users must have a valid email address')

        if not kwargs.get('phone'):
            raise ValueError('Users must have a valid phone')

        if not kwargs.get('first_name'):
            raise ValueError('Users must have a first name')

        if not kwargs.get('last_name'):
            raise ValueError('Users must have a last name')

        account = self.model(
            email=self.normalize_email(email),
            phone=kwargs.get('phone'),
            first_name=kwargs.get('first_name'),
            last_name=kwargs.get('last_name')
        )
        account.set_password(password)
        account.set_phone_auth_code()
        account.save()

        print('finish create user')
        return account

    def create_superuser(self, email, password, **kwargs):
        account = self.create_user(email, password, **kwargs)

        account.is_admin = True
        account.save()

        return account

class Account(AbstractBaseUser):
    email = models.EmailField(unique=True)
    phone = PhoneNumberField(unique=True)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    is_courier = models.BooleanField(default=True)

    phone_auth_code = models.IntegerField(blank=True, null=True)
    phone_verified = models.BooleanField(default=False)
    phone_verification_date = models.DateTimeField(blank=True, null=True)

    email_auth_code = models.CharField(max_length=100, blank=True, default='')
    email_verified = models.BooleanField(default=False)
    email_verification_date = models.DateTimeField(blank=True, null=True)

    is_admin = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']

    def __unicode__(self):
        return self.email

    def get_full_name(self):
        return ' '.join([self.first_name, self.last_name])

    def get_short_name(self):
        return self.first_name

    @property
    def is_superuser(self):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    def set_phone_auth_code(self):
        self.phone_auth_code = randint(1000, 9999)
        return self.phone_auth_code

    def validate_phone_auth_code(self, code):
        phone_matches = self.phone_auth_code == int(code)

        if phone_matches:
            self.phone_verified = True
            self.phone_verification_date = timezone.now()
            self.save()

        return phone_matches
