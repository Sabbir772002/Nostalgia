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
    username = models.ForeignKey(Owner, on_delete=models.CASCADE)
    walk_id = models.ForeignKey(Walk, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.username} - {self.walk_id}"
    
class Friend(models.Model):
    f_id = models.AutoField(primary_key=True)
    f_created_date = models.DateField()
    is_fnf= models.IntegerField()
    user1 = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='user1_friends')
    user2 = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='user2_friends')
    def __str__(self):
        return f"Friendship between {self.user1.username} and {self.user2.username}"
    
class Chat(models.Model):
    msgID = models.AutoField(primary_key=True)
    message_time = models.DateTimeField()
    Msg = models.CharField(max_length=255)
    Sender = models.ForeignKey(Owner, related_name='sent_messages', on_delete=models.CASCADE)
    Receiver = models.ForeignKey(Owner, related_name='received_messages', on_delete=models.CASCADE)

    def __str__(self):
        return f"Chat message {self.msgID}"
    
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

class Blog(models.Model):
    BlogID = models.AutoField(primary_key=True)
    post_date = models.DateField()
    content = models.TextField()
    title = models.CharField(max_length=255)
    blog_img = models.ImageField(upload_to='blog_images/', null=True, blank=True)  # Assuming blog images are uploaded and stored
    author = models.ForeignKey(Owner, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
class GroupPost(models.Model):
    GPost_id = models.AutoField(primary_key=True)
    GPost_contents = models.CharField(max_length=255)
    GPost_Time = models.DateTimeField()               # Used DateTimeField instead of IntegerField for more precise date time
    GPost_date = models.DateTimeField()               # Our Scehma has it as interger
    GPost_image = models.CharField(max_length=255)
    G_username = models.ForeignKey(Owner, on_delete=models.CASCADE)  # Assuming User model exists

    def __str__(self):
        return f"Group Post {self.GPost_id}"

class IndividualPost(models.Model):
    PostID = models.AutoField(primary_key=True)
    Post_contents = models.CharField(max_length=255)
    Post_date = models.DateField()
    Image = models.CharField(max_length=255)
    PostTime = models.DateTimeField()
    Username = models.ForeignKey(Owner, on_delete=models.CASCADE)  # Assuming User model exists

    def __str__(self):
        return f"Individual Post {self.PostID}"
    
class Group(models.Model):
    G_username = models.CharField(max_length=255)
    Name = models.CharField(max_length=255)
    CreatedDate = models.DateTimeField()
    Topic = models.CharField(max_length=255)
    Privacy = models.CharField(max_length=255)
    Creator = models.ForeignKey(Owner, on_delete=models.CASCADE)

    def __str__(self):
        return self.Name
    
class GroupMember(models.Model):
    MemberID = models.AutoField(primary_key=True)
    JoinDate = models.DateTimeField()
    isAdmin = models.CharField(max_length=10)  # Assuming 'isAdmin' can be 'True' or 'False'
    Block = models.BooleanField(default=False)  # Assuming 'Block' can be True or False
    G_username = models.ForeignKey(Group, on_delete=models.CASCADE)
    member = models.ForeignKey(Owner, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.member.username} in {self.G_username}"
    
class Division(models.Model):
    division = models.CharField(max_length=255)

    def __str__(self):
        return self.division

class District(models.Model):
    district_name = models.CharField(max_length=255)
    division = models.ForeignKey(Division, on_delete=models.CASCADE)

    def __str__(self):
        return self.district_name
    

class PlanTrip(models.Model):
    TripID = models.AutoField(primary_key=True)
    Location = models.CharField(max_length=255)
    Trip_start_date = models.DateField()
    Trip_end_date = models.DateField()
    Trip_propose_date = models.DateField()
    Privacy = models.CharField(max_length=255)
    Creator = models.ForeignKey(Owner, related_name='planned_trips', on_delete=models.CASCADE)
    Thana = models.ForeignKey(Thana, on_delete=models.CASCADE)
    Guide = models.ForeignKey(Guide, on_delete=models.CASCADE)

    def __str__(self):
        return f"Trip {self.TripID}: {self.Location}"
    
class Agency(models.Model):
    Agency_ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=255)
    A_Location = models.CharField(max_length=255)
    Thana = models.ForeignKey(Thana, on_delete=models.CASCADE)

    def __str__(self):
        return self.Name

class Guide(models.Model):
    G_ID = models.AutoField(primary_key=True)
    Phone = models.IntegerField()
    Email = models.EmailField(max_length=255)
    Experience = models.IntegerField()
    G_name = models.CharField(max_length=255)
    Gender = models.CharField(max_length=10)
    DOB = models.DateField()
    Agency_ID = models.ForeignKey(Agency, on_delete=models.CASCADE)

    def __str__(self):
        return self.G_name
    
class TripMember(models.Model):
    TM_id = models.AutoField(primary_key=True)
    cancel_member = models.IntegerField()
    TripID = models.ForeignKey(PlanTrip, on_delete=models.CASCADE)
    T_member = models.ForeignKey(Owner, on_delete=models.CASCADE)

    def __str__(self):
        return f"Trip Member {self.TM_id}"
    
class Blog(models.Model):
    BlogID = models.AutoField(primary_key=True)
    Blog_post_date = models.DateField()
    Content = models.CharField(max_length=255)
    Title = models.CharField(max_length=255)
    Blog_IMG = models.CharField(max_length=255)  # Assuming this stores image path or reference
    Author = models.ForeignKey(Owner, on_delete=models.CASCADE)

    def __str__(self):
        return self.Title
    
class Comment(models.Model):
    CommentID = models.AutoField(primary_key=True)
    Content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    Username = models.ForeignKey(Owner, on_delete=models.CASCADE)
    BlogPost = models.ForeignKey(Blog, on_delete=models.CASCADE)

    def __str__(self):
        return f"Comment {self.CommentID} by {self.Username}"


class Reply(models.Model):
    replyID = models.AutoField(primary_key=True)
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    CommentID = models.ForeignKey(Comment, on_delete=models.CASCADE)
    Username = models.ForeignKey(Owner, on_delete=models.CASCADE)

    def __str__(self):
        return f"Reply {self.replyID} by {self.Username}"
    
