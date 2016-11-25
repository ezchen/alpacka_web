from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField

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
        account.save()

        print('finish create user')
        return account

    def create_superuser(self, email, password, **kwargs):
        account = self.create_user(email, password, kwargs)

        account.is_admin = True
        account.save()

        return account

class Account(AbstractBaseUser):
    email = models.EmailField(unique=True)
    phone = PhoneNumberField(unique=True)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    is_courier = models.BooleanField(default=False)

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
