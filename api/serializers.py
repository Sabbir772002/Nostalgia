from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from api.models import Owner, Overseer, User
from api.models import Friend, Chat, Medication, Medicine, Blog, GroupPost #, IndividualPost, Group, GroupMember, Division, District, PlanTrip, Agency, Guide, TripMember, Upvote, Comment, Reply, PlanEvent, JoinEvent

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner  # Setting it to Owner, as both Owner and Overseer inherit from User
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name', 'gender', 'phone', 'dob', 'address', 'nid', 'p_image', 'thana']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        #svalidated_data['password'] = make_password(validated_data['password'])
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
        #instance.walk_type = validated_data.get('walk_type', instance.walk_type)
        # instance.Location = validated_data.get('Location', instance.Location)
        # instance.Relation = validated_data.get('Relation', instance.Relation)
        instance.save()
        return instance


class OwnerSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = Owner
        fields = UserSerializer.Meta.fields + ['walk_type']

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        instance.walk_type = validated_data.get('walk_type', instance.walk_type)
        instance.save()
        return instance

class OverseerSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = Overseer
        fields = UserSerializer.Meta.fields + ['Location', 'Relation']

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        instance.Location = validated_data.get('Location', instance.Location)
        instance.Relation = validated_data.get('Relation', instance.Relation)
        instance.save()
        return instance

class UserLoginSerializer(serializers.Serializer):
	email = serializers.EmailField()
	password = serializers.CharField()
	def check_user(self, clean_data):
		user = authenticate(username=clean_data['username'], password=clean_data['password'])
		if not user:
			raise ValidationError('user not found')
		return user



class ChangePasswordSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    old_password = serializers.CharField(max_length=128)
    new_password = serializers.CharField(max_length=128)

    def validate(self, data):
        username = data.get('username')
        old_password = data.get('old_password')
        new_password = data.get('new_password')

        # Check if the username exists
        if not User.objects.filter(username=username).exists():
            raise serializers.ValidationError("User does not exist.")

        # Check if the old password matches
        user = User.objects.get(username=username)
        if not user.check_password(old_password):
            raise serializers.ValidationError("Old password is incorrect.")

        # You can add more validation logic here if needed

        return data

    def save(self, **kwargs):
        username = self.validated_data['username']
        new_password = self.validated_data['new_password']
        user = User.objects.get(username=username)
        user.set_password(new_password)
        user.save()

from rest_framework.serializers import ModelSerializer

class ProfileSerilazier(ModelSerializer):
    class Meta:
        model = Owner

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
