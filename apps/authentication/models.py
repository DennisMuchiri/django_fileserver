from django.db import models
import jwt
from datetime import datetime, timedelta, date
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db.models import Q
import logging

from apps.ke_mixcloud_core.models import AbstractBase

logger = logging.getLogger(__name__)


class UserManager(BaseUserManager):

    def get_queryset(self):
        return super(UserManager, self).get_queryset().filter(deleted=False)

    def create_user(self, username, email, password=None, **kwargs):
        first_name = kwargs.get('first_name', None)
        last_name = kwargs.get('last_name', None)
        phone_number = kwargs.get('phone_number', None)

        createdate = kwargs.get('createdate', None)
        if createdate is None:
            createdate=date.today()
        txndate = kwargs.get('txndate', None)
        if txndate is None:
            txndate=datetime.now()


        approved = kwargs.get('approved', True)
        approved_by = kwargs.get('approved_by', None)
        approveddate = kwargs.get('approveddate', datetime.now())


        if first_name is None:
            raise TypeError('Users must have a first name.')

        if last_name is None:
            raise TypeError('Users must have a last name.')

        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        if phone_number is None:
            raise TypeError('Users must have a phone number.')



        user = self.model(
            username=username,
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            createdate=createdate,
            txndate=txndate,

            approved=approved,
            approved_by=approved_by,
            approveddate=approveddate,

        )
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, first_name, last_name, phone_number, password=None):
        '''
        Set SYSTEM PERMISSION FOR THE SUPER USER
        '''


        if password is None:
            raise TypeError('Superusers must have a password.')
        user = self.create_user(username=username,
                                email=email,
                                password=password,
                                first_name=first_name,
                                last_name=last_name,
                                phone_number=phone_number
                                )
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class CustomUser(AbstractBaseUser, PermissionsMixin, AbstractBase):
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ('-created_at', '-updated_at')


    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)

    # DEFAULT FIELDS
    createdate = models.DateField(default=date.today, blank=True, null=True)
    txndate = models.DateTimeField(default=datetime.now)
    approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey('authentication.CustomUser', models.DO_NOTHING, db_column='approved_by', blank=True, null=True)
    approveddate = models.DateTimeField(blank=True, null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'phone_number']

    objects = UserManager()

    def __str__(self):

        return self.username

    @property
    def get_full_name(self):

        return self.first_name + ' ' + self.last_name


    def get_short_name(self):
        return self.username

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=30)
        data = {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'exp': int(dt.timestamp())
        }
        token = jwt.encode(data, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')

    @classmethod
    def get_employees(cls):
        return CustomUser.objects.all()

    @classmethod
    def get_single_emp(cls, username):
        return CustomUser.objects.get(employee=username)

    def get_permissions(self):
        return self.role.permissionsmaps.all()

    def has_perm(self, perm, obj=None):
        if self.is_superuser:
            return True
        else:
            return False

    def has_perms(self, perm_list, obj=None):
        return all(self.has_perm(perm, obj) for perm in perm_list)


