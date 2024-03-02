from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager,Group,Permission
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password

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


class User(AbstractBaseUser, PermissionsMixin):
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_name='custom_user_groups'  # Change this to a unique related_name
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='custom_user_permissions'  # Change this to a unique related_name
    )
    # Your
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    phone = models.CharField(max_length=20)
    dob = models.DateField()
    address = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    nid = models.CharField(max_length=20)
    p_image = models.ImageField(upload_to='image/', null=True)
    thana = models.ForeignKey('Thana', on_delete=models.CASCADE)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')


class Thana(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Owner(User):
    walk_type = models.CharField(max_length=100)

    class Meta:
        verbose_name = _('Owner')
        verbose_name_plural = _('Owners')

    def save(self, *args, **kwargs):
        # Update other common fields
        self.password = make_password(self.password)
        super().save(*args, **kwargs)


class Overseer(User):
    Location = models.CharField(max_length=255)
    Relation = models.CharField(max_length=255)

    class Meta:
        verbose_name = _('Overseer')
        verbose_name_plural = _('Overseers')

    def save(self, *args, **kwargs):
        # Update other common fields
        self.password = make_password(self.password)
        super().save(*args, **kwargs)
    

class Hospital(models.Model):
    h_id = models.AutoField(primary_key=True)
    h_name = models.CharField(max_length=255)
    h_location = models.CharField(max_length=255)
    branch = models.CharField(max_length=255)
    thana = models.ForeignKey(Thana, on_delete=models.CASCADE)

    def __str__(self):
        return self.h_name

class Walk(models.Model):
    walk_id = models.AutoField(primary_key=True)
    walk_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    propose_date = models.DateField()
    walk_date = models.DateField()
    privacy = models.CharField(max_length=255)
    w_creator = models.ForeignKey(Owner, on_delete=models.CASCADE)

    def __str__(self):
        return self.walk_name

class CareType(models.Model):
    type = models.CharField(max_length=255)

    def __str__(self):
        return self.type
class Caregiver(models.Model):
    caregiver_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=10)
    phone = models.PositiveIntegerField()
    experience = models.PositiveIntegerField()
    type = models.ForeignKey(CareType, on_delete=models.CASCADE)
    h_id = models.ForeignKey(Hospital, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class WalkMember(models.Model):
    wm_id = models.AutoField(primary_key=True)
    cancel = models.IntegerField()
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    walk_id = models.ForeignKey(Walk, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.username} - {self.walk_id}"
    
class Friend(models.Model):
    f_id = models.AutoField(primary_key=True)
    f_created_date = models.IntegerField()
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user1_friends')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user2_friends')

    def __str__(self):
        return f"Friendship between {self.user1.username} and {self.user2.username}"
    
class Medication(models.Model):
    medication_id = models.AutoField(primary_key=True)
    meds_start_date = models.DateField()
    meds_end_date = models.DateField()
    dose = models.IntegerField()
    times = models.IntegerField()
    user = models.ForeignKey(Owner, on_delete=models.CASCADE)
    med_name = models.ForeignKey('Medicine', on_delete=models.CASCADE)

    def __str__(self):
        return f"Medication ID: {self.medication_id}, User: {self.user}, Med Name: {self.med_name}"
class Medicine(models.Model):
    med_id = models.AutoField(primary_key=True)
    disease = models.CharField(max_length=255)
    content = models.CharField(max_length=255)
    med_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.med_name} - {self.disease}"
<<<<<<< HEAD


=======
>>>>>>> f2a39aec1714df3666fcbd78f5910dda9d6ddf63
