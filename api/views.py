# views.py
from rest_framework import views, status
from rest_framework.response import Response
from .serializers import OwnerSerializer,OverseerSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .models import Owner
from .serializers import OwnerSerializer
from django.http import HttpResponse

class sign(APIView):
    def post(self, request):
        print("hey done")
        serializer = OwnerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class _sign(views.APIView):
    def post(self, request):
        serializer = OverseerSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User created successfully", "user_id": user.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.contrib.auth import authenticate, login

class login_api(views.APIView):
    def post(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        if username and password:
            user = authenticate(request, username=username, password=password)
            print("user tomar")
            print(user)
            if user is not None:
                login(request,user)
                return Response({'authenticated': True}, status=status.HTTP_200_OK)
        
        return Response({'authenticated': False}, status=status.HTTP_401_UNAUTHORIZED)


class show(views.APIView):
    def post(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        if(request.user.is_authenticated):
            return Response({'authenticated boSS!': True}, status=status.HTTP_200_OK)
        return Response({'authenticated': False}, status=status.HTTP_401_UNAUTHORIZED)



def friends(request):
    print(request.user)
    if(request.user.is_authenticated):
        print("Yeah, youa re boss")
    else:
        print("You are not authenticated")

    return HttpResponse("Hello, this is the friends page!")

class MyAPIView(views.APIView):
    def get(self, request):
        # Extract query parameters from the request
        name = request.GET.get('name')
        #age = request.GET.get('age')

        # Initialize queryset
        queryset = MyModel.objects.all()
        print(name)

        # Apply filters based on query parameters
        if name:
            queryset = queryset.filter(name=name)
        #if age:
        #    queryset = queryset.filter(age=age)

        # Convert queryset to a list of dictionaries
        data = list(queryset.values())

        # Return the filtered data as JSON response
        serializer = MyModelSerializer(queryset, many=True)
        return Response(serializer.data)


class MyModelListCreateAPIView(views.APIView):
    def get(self, request):
        queryset = MyModel.objects.all()
        serializer = MyModelSerializer(queryset, many=True)
        return Response(serializer.data)
        
    def post(self, request):
        serializer = MyModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password, make_password


class ChangePasswordAPIView(views.APIView):
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']
            username = serializer.validated_data['username']
            print(username)
            user = User.objects.get(username=username)
            user.set_password(new_password)
            return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)

            # Check if the old password is correct
            if check_password(old_password, user.password):
                # Set the new password and save the user object
                user.set_password(new_password)
                user.save()
                return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Old password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
