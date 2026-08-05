                
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework.serializers import ValidationError, ModelSerializer

from api.models import Owner, Overseer, User
from api.models import (
    Friend, Chat, Medication, Medicine, Blog, GroupPost,
    IndividualPost, CommunityGroup, GroupMember,
    Division, District, Trip, Agency, Guide, TripMember,
    Upvote, Comment, Reply, Event, JoinEvent, Walk, WalkMember,
    Notification                               
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner                                             
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name',
                  'gender', 'phone', 'dob', 'address', 'p_image', 'nid', 'thana']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.dob = validated_data.get('dob', instance.dob)
        instance.address = validated_data.get('address', instance.address)
        instance.nid = validated_data.get('nid', instance.nid)
        instance.p_image = validated_data.get('p_image', instance.p_image)
        instance.thana = validated_data.get('thana', instance.thana)
        instance.save()
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        fallback_url = "/media/image/download_lX6bjA6.jpeg"
        p_image_val = data.get('p_image')
        if not p_image_val:
            p_image_val = fallback_url
        data['p_image'] = p_image_val
        data['pp'] = p_image_val
        return data


class OwnerSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = Owner
        fields = UserSerializer.Meta.fields + ['walk_type']

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        instance.walk_type = validated_data.get('walk_type', instance.walk_type)
        instance.save()
        return instance


class OwnerUpdateSerializer(UserSerializer):
    walk_type = serializers.CharField(max_length=100)

    class Meta(UserSerializer.Meta):
        model = Owner
        fields = UserSerializer.Meta.fields + ['walk_type']
        extra_kwargs = {
            'password': {'read_only': True},
        }

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        instance.walk_type = validated_data.get('walk_type', instance.walk_type)
        instance.save()
        return instance


class OverseerSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = Overseer
        fields = [field for field in UserSerializer.Meta.fields if field != 'thana'] + ['Location', 'Relation']

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        instance.Location = validated_data.get('Location', instance.Location)
        instance.Relation = validated_data.get('Relation', instance.Relation)
        instance.save()
        return instance


class OverseerUpdateSerializer(serializers.ModelSerializer):
    Location = serializers.CharField(max_length=100)
    Relation = serializers.CharField(max_length=100)

    class Meta:
        model = Overseer
        fields = '__all__'
        extra_kwargs = {
            'password': {'read_only': True},
        }

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        instance.Location = validated_data.get('Location', instance.Location)
        instance.Relation = validated_data.get('Relation', instance.Relation)
        instance.save()
        return instance


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def check_user(self, clean_data):
        user = authenticate(username=clean_data['username'], password=clean_data['password'])
        if not user:
            raise ValidationError('user not found')
        return user


class PassResetSerializer(serializers.Serializer):
    new_password = serializers.CharField(min_length=1, max_length=128)
    username = serializers.CharField()
    done = serializers.IntegerField()

    def validate_username(self, value):
        if not User.objects.filter(username=value).exists():
            raise serializers.ValidationError("User does not exist.")
        return value

    def validate_new_password(self, value):
        return value

    def validate_done(self, value):
        if value != 1:
            raise serializers.ValidationError("OTP is not verified")
        return value


class ChangePasswordSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    old_password = serializers.CharField(max_length=128)
    new_password = serializers.CharField(max_length=128)

    def validate(self, data):
        username = data.get('username')
        old_password = data.get('old_password')

        if not User.objects.filter(username=username).exists():
            raise serializers.ValidationError("User does not exist.")

        user = User.objects.get(username=username)
        if not user.check_password(old_password):
            raise serializers.ValidationError("Old password is incorrect.")

        return data

    def save(self, **kwargs):
        username = self.validated_data['username']
        new_password = self.validated_data['new_password']
        user = User.objects.get(username=username)
        user.set_password(new_password)
        user.save()


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Owner
        fields = '__all__'


class FriendSerializer(serializers.ModelSerializer):
    user1 = OwnerSerializer(read_only=True)
    user2 = OwnerSerializer(read_only=True)

    class Meta:
        model = Friend
        fields = ['f_id', 'f_created_date', 'user1', 'user2']

    def create(self, validated_data):
        user1_data = validated_data.pop('user1')
        user2_data = validated_data.pop('user2')

        user1 = Owner.objects.get(pk=user1_data['id'])
        user2 = Owner.objects.get(pk=user2_data['id'])

        friend = Friend.objects.create(user1=user1, user2=user2, **validated_data)
        return friend


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['blogid', 'post_date', 'post_time', 'content', 'blog_img', 'author']

    def create(self, validated_data):
        return Blog.objects.create(**validated_data)


class WalkMemberSerializer(serializers.ModelSerializer):
    username = serializers.PrimaryKeyRelatedField(queryset=Owner.objects.all())
    walk_id = serializers.PrimaryKeyRelatedField(queryset=Walk.objects.all())

    class Meta:
        model = WalkMember
        fields = ['wm_id', 'cancel', 'username', 'walk_id']

    def update(self, instance, validated_data):
        instance.cancel = validated_data.get('cancel', instance.cancel)
        instance.save()
        return instance


class PlanEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['EventID', 'Description', 'Event_title', 'start_time',
                  'end_time', 'start_date', 'end_date',
                  'Address', 'create_date', 'Approve',
                  'E_type', 'Image', 'E_creator', 'Thana']

    def create(self, validated_data):
        return Event.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.Description = validated_data.get('Description', instance.Description)
        instance.Event_title = validated_data.get('Event_title', instance.Event_title)
        instance.start_time = validated_data.get('start_time', instance.start_time)
        instance.end_time = validated_data.get('end_time', instance.end_time)
        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.Address = validated_data.get('Address', instance.Address)
        instance.create_date = validated_data.get('create_date', instance.create_date)
        instance.Approve = validated_data.get('Approve', instance.Approve)
        instance.E_type = validated_data.get('E_type', instance.E_type)
        instance.Image = validated_data.get('Image', instance.Image)
        instance.E_creator = validated_data.get('E_creator', instance.E_creator)
        instance.Thana = validated_data.get('Thana', instance.Thana)
        instance.save()
        return instance


class WalkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Walk
        fields = ('walk_id', 'walk_name', 'address', 'propose_date', 'walk_date',
                  'time', 'end_date', 'privacy', 'w_creator')


                                                    
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['noti_id', 'noti_date', 'noti_msg', 'noti_time',
                  'noti_type', 'noti_status', 'noti_receiver', 'noti_sender']
        read_only_fields = ['noti_id', 'noti_date', 'noti_time']

    def create(self, validated_data):
                                                                                         
        return Notification.objects.create(**validated_data)