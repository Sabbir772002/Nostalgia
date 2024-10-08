from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager,Group,Permission
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password
from django.utils import timezone

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
class Division(models.Model):
    division = models.CharField(max_length=100, unique=True,primary_key=True)
    def __str__(self):
        return self.division

class District(models.Model):
    district= models.CharField(max_length=100, unique=True,primary_key=True)
    division = models.ForeignKey(Division, on_delete=models.CASCADE)

    def __str__(self):
        return self.district
class Thana(models.Model):
    thana = models.CharField(max_length=100,primary_key=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    def __str__(self):
        return self.thana

class Owner(User):
    walk_type = models.CharField(max_length=100)

    class Meta:
        verbose_name = _('Owner')
        verbose_name_plural = _('Owners')

    def save(self, *args, **kwargs):
        # Update other common fields
        self.password = make_password(self.password)
        super().save(*args, **kwargs)


class Additional(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Owner, on_delete=models.CASCADE)
    type= models.CharField(max_length=255)
    content = models.CharField(max_length=255)
    def __str__(self):
        return self.type+":"+self.content


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
class Verified(models.Model):
    verified = models.BooleanField(default=False)
    user=models.ForeignKey(Owner, on_delete=models.CASCADE,primary_key=True)
    def __str__(self):
        return self.verified
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
    walk_name = models.CharField(max_length=255)#null mean general walk or individual walk
    address = models.CharField(max_length=255)
    propose_date = models.DateField()
    walk_date = models.DateField()
    end_date = models.DateField() #null mean for once
    privacy = models.CharField(max_length=255)
    time=models.TimeField()
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
    email = models.EmailField()
    dob = models.DateField()
    def __str__(self):
        return self.name
class WalkMember(models.Model):
    wm_id = models.AutoField(primary_key=True)
    cancel = models.IntegerField()
    username = models.ForeignKey(Owner, on_delete=models.CASCADE)
    walk_id = models.ForeignKey(Walk, on_delete=models.CASCADE)
    accept = models.IntegerField()

    def __str__(self):
        return f"{self.username} - {self.walk_id}"
class Friend(models.Model):
    f_id = models.AutoField(primary_key=True)
    f_created_date = models.DateField()
    is_fnf= models.IntegerField()
    type= models.CharField(max_length=255)
    type = models.CharField(max_length=255)
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
    dose = models.CharField(max_length=100)
    after= models.CharField(max_length=100)
    night= models.IntegerField()
    morning = models.IntegerField()
    noon = models.IntegerField()
    note= models.CharField(max_length=255)
    user = models.ForeignKey(Owner, on_delete=models.CASCADE)
   # med_name = models.ForeignKey('Medicine', on_delete=models.CASCADE)
    med_name = models.CharField(max_length=255)
    img = models.ImageField(upload_to='med_images/', null=True, blank=True)
    def __str__(self):
        return f"Medication ID: {self.medication_id}, User: {self.user}, Med Name: {self.med_name}"
class MedAlert(models.Model):
    userid = models.ForeignKey(Owner, on_delete=models.CASCADE,primary_key=True)
    morning = models.TimeField()
    noon = models.TimeField()
    night = models.TimeField()
    interval = models.IntegerField()
    alert_message = models.CharField(max_length=255)
    def str(self):
     return f"Med Alert: Morning: {self.morning}, Noon: {self.noon}, Night: {self.night}"
class DoneMed(models.Model):
    done_id = models.AutoField(primary_key=True)
    done_date = models.DateField(max_length=255)
    done_time = models.CharField(max_length=255)
    user = models.ForeignKey(Owner, on_delete=models.CASCADE)
    def __str__(self):
        return f"Done ID: {self.done_id}, User: {self.user}"
class Medicine(models.Model):
    med_id = models.AutoField(primary_key=True)
    disease = models.CharField(max_length=255)
    content = models.CharField(max_length=255)
    med_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.med_name} - {self.disease}"

class Blog(models.Model):
    blogid = models.AutoField(primary_key=True)
    post_date = models.DateField()
    post_time=models.TimeField()
    content = models.TextField()
    blog_img = models.ImageField(upload_to='blog_images/', null=True, blank=True)  # Assuming blog images are uploaded and stored
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.content
class Group(models.Model):
    G_username = models.CharField(max_length=255,primary_key=True)
    G_name = models.CharField(max_length=255)
    CreatedDate = models.DateField(default=timezone.now)
    Topic = models.CharField(max_length=255)
    Privacy = models.CharField(max_length=255)
    time = models.TimeField()
    Creator = models.ForeignKey(Owner, on_delete=models.CASCADE)
    img=models.ImageField(upload_to='group_images/', null=True, blank=True)
    def __str__(self):
        return self.G_name

class GroupMember(models.Model):
    MemberID = models.AutoField(primary_key=True)
    JoinDate = models.DateField(default=timezone.now)
    isAdmin = models.CharField(max_length=10)
    Block = models.IntegerField()
    G_username = models.ForeignKey(Group, on_delete=models.CASCADE,to_field='G_username')
    member = models.ForeignKey(Owner, on_delete=models.CASCADE)
    accept = models.IntegerField()

    def __str__(self):
        return f'Member ID: {self.MemberID}, Username: {self.G_username.G_username}'
    
class Agency(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    image = models.ImageField(upload_to='image/', null=True)
    thana = models.ForeignKey(Thana, on_delete=models.CASCADE)
    rating = models.FloatField()
    def __str__(self):
        return self.name

class Guide(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    image = models.ImageField(upload_to='image/', null=True)
    thana = models.ForeignKey(Thana, on_delete=models.CASCADE)
    rating = models.FloatField()
    experience = models.IntegerField()
    dob = models.DateField()
    agency = models.ForeignKey('Agency', on_delete=models.CASCADE)
    def __str__(self):
        return self.G_name

class Trip(models.Model):
    TripID = models.AutoField(primary_key=True)
    name=models.CharField(max_length=255)
    Location = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    propose_date = models.DateField(default=timezone.now)
    Privacy = models.CharField(max_length=255)
    Creator = models.ForeignKey(Owner, on_delete=models.CASCADE)
    Thana = models.ForeignKey(Thana, on_delete=models.CASCADE)
    #guide = models.ForeignKey(Guide, on_delete=models.CASCADE)
    guide=models.CharField(max_length=255)

    def __str__(self):
        return f'Trip ID: {self.TripID}, Location: {self.Location}'

class TripMember(models.Model):
    Tid = models.AutoField(primary_key=True)
    cancel = models.IntegerField()
    TripID = models.ForeignKey(Trip, on_delete=models.CASCADE)
    member = models.ForeignKey(Owner, on_delete=models.CASCADE)
    Approve = models.IntegerField()
    def __str__(self):
        return f'Trip ID: {self.TripID}, Member ID: {self.member}'

class GroupPost(models.Model):
    GPost_id = models.AutoField(primary_key=True)
    GPost_contents = models.TextField()
    GPost_Time = models.TimeField()
    GPost_date = models.DateField()
    GPost_image = models.ImageField(upload_to='image/', null=True)
    G_username = models.ForeignKey(Group, on_delete=models.CASCADE)
    p_username=models.ForeignKey(Owner,on_delete=models.CASCADE)


    def __str__(self):
        return f'Group Post ID: {self.GPost_id}, Contents: {self.GPost_contents}'    

class IndividualPost(models.Model):
    PostID = models.AutoField(primary_key=True)
    Post_contents = models.TextField()
    Post_date = models.DateField()
    Image = models.ImageField(upload_to='image/', null=True)
    PostTime = models.IntegerField()
    Username = models.ForeignKey(Owner, on_delete=models.CASCADE)

    def __str__(self):
        return f'Post ID: {self.PostID}, Contents: {self.Post_contents}'

class Event(models.Model):
    EventID = models.AutoField(primary_key=True)
    Description = models.CharField(max_length=255)
    Event_title = models.CharField(max_length=255)
    start_time = models.TimeField()
    end_time = models.TimeField()
    start_date = models.DateField()
    end_date = models.DateField()
    Address = models.CharField(max_length=255)
    create_date = models.DateField()
    Approve = models.IntegerField()
    E_type = models.CharField(max_length=255)
    privacy = models.CharField(max_length=255)
    Image = models.ImageField(upload_to='Eventimage/', null=True)
    E_creator = models.ForeignKey(Owner, on_delete=models.CASCADE)
    Thana = models.ForeignKey(Thana, on_delete=models.CASCADE)
    privacy=models.CharField(max_length=255)
    def __str__(self):
        return self.Event_title
    
class JoinEvent(models.Model):
    JoinID = models.AutoField(primary_key=True)
    Approve = models.IntegerField()
    Member = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='joined_events')
    EventID = models.ForeignKey(Event, on_delete=models.CASCADE)
    cancel = models.IntegerField()
    def __str__(self):
        return f'Join ID: {self.JoinID}, Event ID: {self.EventID}'    


class Upvote(models.Model):
    blogid = models.ForeignKey(Blog, on_delete=models.CASCADE)
    Username = models.ForeignKey(Owner, on_delete=models.CASCADE)
    # class Meta:up
    #     primary_key = ['PostID', 'Username']

    def __str__(self):
        return f"Upvote - Post ID: {self.blogid.blogid}, Username: {self.Username.username}"

class Comment(models.Model):
    cmnt_id = models.AutoField(primary_key=True)
    blogid = models.ForeignKey(Blog, on_delete=models.CASCADE)
    username = models.ForeignKey(
        Owner, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)
    time = models.DateTimeField(default=timezone.now())
    def __str__(self):
        return f"Comment ID: {self.cmnt_id}, Post ID: {self.blogid}, Username: {self.username}, Name: {self.comment}"


class Reply(models.Model):
    Reply_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        Owner, on_delete=models.CASCADE)
    cmnt_id = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name="replies")
    Reply_msg = models.CharField(max_length=500)
    time = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return f"Comment ID: {self.cmnt_id}, Post ID: {self.Reply_id}, Username: {self.user}, Name: {self.Reply_msg}"        
class Notification(models.Model):
    noti_id = models.AutoField(primary_key=True)
    #noti_msg = models.CharField(max_length=255)
    noti_date = models.DateField(default=timezone.now())
    noti_msg = models.TextField()
    noti_time = models.DateTimeField(default=timezone.now())
    noti_type = models.CharField(max_length=255) #friend request, walk request, event request
    noti_status = models.CharField(max_length=255)#unseen or seen
    noti_receiver = models.ForeignKey(Owner, on_delete=models.CASCADE)
    noti_sender = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='sent_notifications')

    def __str__(self):
        return f"Notification ID: {self.noti_id}, Message: {self.noti_msg}"
    
class GroupUpvote(models.Model):
    blogid = models.ForeignKey(GroupPost, on_delete=models.CASCADE)
    Username = models.ForeignKey(Owner, on_delete=models.CASCADE)


    def __str__(self):
        return f"GroupUpvote - Post ID: {self.blogid.blogid}, Username: {self.Username.username}"    
    
class GroupComment(models.Model):
    cmnt_id = models.AutoField(primary_key=True)
    blogid = models.ForeignKey(GroupPost, on_delete=models.CASCADE)
    username = models.ForeignKey(
        Owner, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)
    time = models.DateTimeField(default=timezone.now())
    def __str__(self):
        return f"GroupComment ID: {self.cmnt_id}, Post ID: {self.blogid}, Username: {self.username}, Name: {self.comment}"
    
class GroupReply(models.Model):
    Reply_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        Owner, on_delete=models.CASCADE)
    cmnt_id = models.ForeignKey(
        GroupComment, on_delete=models.CASCADE, related_name="replies")
    Reply_msg = models.CharField(max_length=500)
    time = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return f"GroupComment ID: {self.cmnt_id}, Post ID: {self.Reply_id}, Username: {self.user}, Name: {self.Reply_msg}"        

class GhureAshi(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    image = models.ImageField(upload_to='image/', null=True)
    thana = models.ForeignKey(Thana, on_delete=models.CASCADE)
    rating = models.FloatField()
    def __str__(self):
        return self.name

