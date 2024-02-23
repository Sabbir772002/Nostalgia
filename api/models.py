from django.contrib.auth.models import AbstractBaseUser,Group, BaseUserManager,AbstractUser,Permission,PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.db import models

class MyModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **extra_fields)

class User(AbstractUser,PermissionsMixin):
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_name='api_user_groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='api_user_permissions'
    )

    username = models.CharField(max_length=100, unique=True)
    f_name = models.CharField(max_length=100)
    l_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    dob = models.DateField()
    address = models.CharField(max_length=255)
    password = models.CharField(max_length=255)  # Storing passwords as plain integers is insecure
    nid = models.CharField(max_length=20)
    p_image = models.ImageField(upload_to='image/',null=True)  # ImageField for login image
    walk_type = models.CharField(max_length=100)
    thana = models.ForeignKey('Thana', on_delete=models.CASCADE)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['f_name', 'email', 'phone', 'dob', 'thana', 'nid']

    objects = UserManager()

    def __str__(self):
        return self.username

class Thana(models.Model):
    # Define Thana fields
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class OverseerManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **extra_fields)

class Overseer(AbstractBaseUser):
    username = models.CharField(max_length=100, unique=True)
    Name = models.CharField(max_length=255)
    Phone = models.CharField(max_length=20)
    Email = models.EmailField()
    Location = models.CharField(max_length=255)
    NID = models.CharField(max_length=20)
    Relation = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    Gender = models.CharField(max_length=10)
    thana = models.ForeignKey('Thana', on_delete=models.CASCADE)


    USERNAME_FIELD = 'username'
    # Add any additional fields required for authentication
    # Example:
    # REQUIRED_FIELDS = ['email']

    objects = OverseerManager()

    def __str__(self):
        return self.username
