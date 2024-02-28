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
    

class Friend(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user1_friends')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user2_friends')
    f_created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user1.username} - {self.user2.username}"
    

class Medication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    med_name = models.ForeignKey('MedName', on_delete=models.CASCADE)
    meds_start_date = models.DateField()
    meds_end_date = models.DateField()
    dose = models.PositiveIntegerField()
    times = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.med_name} - {self.user.username}"

class Medicine(models.Model):
    med_id = models.AutoField(primary_key=True)
    disease = models.CharField(max_length=255)
    content = models.CharField(max_length=255)
    med_name = models.CharField(max_length=255)

    def __str__(self):
        return self.med_name
    

class Hospital(models.Model):
    h_id = models.AutoField(primary_key=True)
    h_name = models.CharField(max_length=255)
    h_location = models.CharField(max_length=255)
    branch = models.CharField(max_length=255)
    thana = models.ForeignKey(Thana, on_delete=models.CASCADE)

    def __str__(self):
        return self.h_name
    
class Caregiver(models.Model):
    caregiver_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=10)
    phone = models.PositiveIntegerField()
    experience = models.PositiveIntegerField()
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    h_id = models.ForeignKey(Hospital, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class CareType(models.Model):
    type = models.CharField(max_length=255)

    def __str__(self):
        return self.type

class WalkMember(models.Model):
    wm_id = models.AutoField(primary_key=True)
    cancel = models.IntegerField()
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    walk_id = models.ForeignKey(Walk, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.username} - {self.walk_id}"


class Walk(models.Model):
    walk_id = models.AutoField(primary_key=True)
    walk_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    w_propose_date = models.DateField()
    walk_date = models.DateField()
    privacy = models.CharField(max_length=255)
    w_creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.walk_name