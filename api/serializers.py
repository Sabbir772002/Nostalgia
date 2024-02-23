from rest_framework import serializers
from .models import MyModel

class MyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyModel
        fields = '__all__'



from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'f_name', 'l_name', 'gender', 'email', 'phone', 'dob', 'address', 'nid', 'p_image', 'walk_type', 'thana']
        read_only_fields = ['id']  # Assuming 'id' is auto-generated and read-only

    def create(self, validated_data):
        # Custom create method if needed
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        # Custom update method if needed
        instance.username = validated_data.get('username', instance.username)
        instance.f_name = validated_data.get('f_name', instance.f_name)
        instance.l_name = validated_data.get('l_name', instance.l_name)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.dob = validated_data.get('dob', instance.dob)
        instance.address = validated_data.get('address', instance.address)
        instance.nid = validated_data.get('nid', instance.nid)
        instance.p_image = validated_data.get('p_image', instance.p_image)
        instance.walk_type = validated_data.get('walk_type', instance.walk_type)
        instance.thana = validated_data.get('thana', instance.thana)
        instance.save()
        return instance 
