from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from api.models import Owner, Overseer

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
        instance.walk_type = validated_data.get('walk_type', instance.walk_type)
        # instance.Location = validated_data.get('Location', instance.Location)
        # instance.Relation = validated_data.get('Relation', instance.Relation)
        instance.save()
        return instance

class OwnerSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = Owner

class OverseerSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = Overseer
