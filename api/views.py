# views.py
from rest_framework import views, status
from rest_framework.response import Response
from .serializers import OwnerSerializer,OverseerSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import OwnerSerializer
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import OwnerSerializer, OverseerSerializer,ChangePasswordSerializer,ProfileSerilazier,OwnwerUpdateSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.models import Owner, Overseer,Friend,Thana
from .serializers import OwnerSerializer, OverseerSerializer,UserLoginSerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
import os
from django.shortcuts import render

class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    
    def get(self, request):
        return Response(data={"message": "Hello, world!"})
class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = (permissions.AllowAny,)

class HelloWorldView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        return Response(data={"message": "Hello, world!"})


class O_update(APIView):
    def put(self, request, pk):
        try:
            #Retrieve the overseer object to be updated
            overseer = Overseer.objects.get(pk=pk)
        except Overseer.DoesNotExist:
            return Response({"error": "Overseer not found"}, status=status.HTTP_404_NOT_FOUND)

        # Deserialize the incoming data
        serializer = OverseerSerializer(overseer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        try:
            # Retrieve the overseer object to be updated
            overseer = Overseer.objects.get(pk=pk)
        except Overseer.DoesNotExist:
            return Response({"error": "Overseer not found"}, status=status.HTTP_404_NOT_FOUND)

        # Deserialize the incoming data, but only partially update the overseer
        serializer = OverseerSerializer(overseer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class Owner_update(APIView):
    def put(self, request, username):
        try:
           #print(request.data)
            # Retrieve the user object to be updated
            owner = Owner.objects.get(username=username)
        except Owner.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Deserialize the incoming data
        serializer = OwnwerUpdateSerializer(owner, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
       #print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        try:
            # Retrieve the user object to be updated
            owner = Owner.objects.get(pk=pk)
        except Owner.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Deserialize the incoming data, but only partially update the user
        serializer = OwnerSerializer(owner, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class sign(APIView):
    def post(self, request):
        #print(request.data)
        serializer = OwnerSerializer(data=request.data)
        print("why didnt working?")
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else :
            print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class _sign(views.APIView):
    def post(self, request):
        serializer = OverseerSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User created successfully", "user_id": user.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.contrib.auth import authenticate, login

class UserLogin(APIView):
	permission_classes = (permissions.AllowAny,)
	authentication_classes = (SessionAuthentication,)
	def post(self, request):
		data = request.data
		assert validate_email(data)
		assert validate_password(data)
		serializer = UserLoginSerializer(data=data)
		if serializer.is_valid(raise_exception=True):
			user = serializer.check_user(data)
			login(request, user)
			return Response(serializer.data, status=status.HTTP_200_OK)
        
from django.contrib.auth import logout

class login_api(views.APIView):
    def post(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        #serializer = UserLoginSerializer(data=data)
        print(data)
        #logout(request)

        if username and password:
            user = authenticate(request, username=username, password=password)
            print(user)
            if user is not None:
                login(request,user)
                user=Owner.objects.get(username=username)
                serializer = OwnerSerializer(user)

                return Response({'auth': True,'user':serializer.data}, status=status.HTTP_200_OK)
        
        return Response({'auth': False}, status=status.HTTP_401_UNAUTHORIZED)


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
        print(request.user)
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
from django.contrib.auth.hashers import check_password, make_password


class ChangePass(views.APIView):
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        print(request.user)
        if serializer.is_valid():
            print(serializer.validated_data)
            print("YOu are in changepass class")
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']
            username = serializer.validated_data['username']
            user = User.objects.get(username=username)
            if(user.check_password(old_password)):
                user.set_password(new_password)
                user.save()
                return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
            return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)

            if check_password(old_password, user.password):
                user.set_password(new_password)
                user.save()
                return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Old password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class add_fnf(APIView):
    def post(self, request):
        data = request.data
        if(str(data['user_id']) == str(data['friend_id'])):
            return Response({"message": "You can't add yourself as friend"}, status=status.HTTP_400_BAD_REQUEST)

        fnd=Friend.objects.filter(user1=Owner.objects.get(id=data['user_id']),user2=Owner.objects.get(id=data['friend_id']))
        if(len(fnd) > 0 and fnd[0].is_fnf == 1):
            return Response({"message": "You are already friend"}, status=status.HTTP_400_BAD_REQUEST)
        #check who send fnd request(future work)
        if(len(fnd) > 0):
            return Response({"message": "Your request for friend send"}, status=status.HTTP_400_BAD_REQUEST)
        from django.utils import timezone
        fnd=Friend(user1=Owner.objects.get(id=data['user_id']),user2=Owner.objects.get(id=data['friend_id']),f_created_date=timezone.now(),is_fnf=0)
        fnd.save()
        return Response({"message": "Friends Added successfully"}, status=status.HTTP_201_CREATED)


class FriendList(APIView):
    def get(self, request):
        users = Owner.objects.all()
        # Serialize the data
        serialized_data = []
        for user in users:
            serialized_data.append({
                'id': user.id,
                'pp': user.p_image.url if user.p_image else "media\image\download_lX6bjA6.jpeg",
                'first_name': user.first_name,
                'username': user.username,
                'last_name': user.last_name,
                'email': user.email,
                'gender': user.gender,
                'phone': user.phone,
                'dob': user.dob,
                'address': user.address,
                'nid': user.nid,
                'thana': Thana.objects.get(id=user.thana_id).name,
            })
        
        return Response({"users": serialized_data, "message": "User information retrieved successfully"}, status=status.HTTP_200_OK)


class Profile(APIView):
    def get(self, request, username):
        try:
            user = Owner.objects.get(username=username)
            user=OwnerSerializer(user)
            print(user.data)
           # if(user.is_valid()):
           # print(user.data)
            return Response(user.data, status=status.HTTP_200_OK)
            # print(user.errors)
            # return Response({"message": "User not serialize"}, status=status.HTTP_404_NOT_FOUND)

        except Owner.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
import requests
import random
import string

class EmailVerificationAPIView(APIView):
    def post(self, request):
        # Extract the email address from the request data
        email_address = request.data.get('email')

        # Verify the email address using an email verification API (optional)
        # You can skip the verification API and directly send the email
        # is_email_valid = self.verify_email(email_address)

        # Generate a verification code
        verification_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

        # Send verification email with the verification code
        self.send_verification_email(email_address, verification_code)

        return Response({"message": "Verification email sent successfully", "verification_code": verification_code}, status=status.HTTP_200_OK)

    def send_verification_email(self, email_address, verification_code):
        # Send verification email using Django's email functionality
        subject = 'Email Verification'
        message = f'Your verification code is: {verification_code}'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email_address]

        send_mail(subject, message, from_email, recipient_list)
class profile(APIView):
    def get(self, request):
        data = request.data
        print(data)
        return Response({"message": "Friends Retrive successfully"}, status=status.HTTP_201_CREATED)


from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Friend
from .serializers import FriendSerializer
from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework import status

class FriendListView(generics.ListAPIView):
    serializer_class = FriendSerializer
    #permission_classes = [IsAuthenticated]  # Requires authentication
    paginate_by = 10  # Number of items per page (adjust as needed)

    def get_queryset(self):
        # Get the current user from the request
        user = self.request.user

        # Filter friends where the user is either user1 or user2 (excluding the current user)
        queryset = Friend.objects.filter(user1=user) | Friend.objects.filter(user2=user)
        queryset = queryset.exclude(user1=user) | queryset.exclude(user2=user)
        
        return queryset
    
    def get(self, request, *args, **kwargs):
        # Check if the request is for paginated data
        page_number = request.query_params.get('page')
        if page_number:
            return self.list(request, *args, **kwargs)  # Call list method for paginated response
        else:
            # Handle non-paginated GET request (e.g., retrieve specific friend details)
            friend_id = kwargs.get('pk')  # Get the friend ID from URL parameters
            try:
                friend = Friend.objects.get(pk=friend_id)
            except Friend.DoesNotExist:
                return Response({"error": "Friend not found"}, status=status.HTTP_404_NOT_FOUND)

            # Check if the current user is user1 or user2 in the friendship
            current_user = request.user
            if friend.user1 == current_user:
                friend_owner = friend.user2
            else:
                friend_owner = friend.user1

            # Serialize the friend owner object
            owner_serializer = OwnerSerializer(friend_owner)
            return Response(owner_serializer.data)


import os
import base64
import requests

class FaceCompareAPI:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.url = "https://api-us.faceplusplus.com/facepp/v3/compare"

    def compare_images(self, image_path1, image_path2):
        # Read image files and convert them to base64 strings
        base64_image1 = self.encode_image_to_base64(image_path1)
        base64_image2 = self.encode_image_to_base64(image_path2)

        # Prepare the payload
        payload = {
            "api_key": self.api_key,
            "api_secret": self.api_secret,
            "image_base64_1": base64_image1,
            "image_base64_2": base64_image2,
        }

        # Send the POST request to Face++ API
        response = requests.post(self.url, data=payload)
        response_json = response.json()

        # Process the response and return the result
        return self.process_response(response_json)

    def encode_image_to_base64(self, image_path):
        with open(image_path, 'rb') as img_file:
            image_content = img_file.read()
            base64_image = base64.b64encode(image_content).decode('utf-8')
        return base64_image

    def process_response(self, response_json):
        confidence = response_json.get('confidence', 0)
        threshold = 50
        if confidence >= threshold:
            return "Match between two photos is successful with confidence: {:.2f}".format(confidence)
        else:
            return "Match between two photos is not successful. Confidence is too low: {:.2f}".format(confidence)

class WalkingBuddyList(APIView):
    def get(self, request):
        users = Owner.objects.all()
        # Serialize the data
        serialized_data = []
        for user in users:
            serialized_data.append({
                'id': user.id,
                'pp': user.p_image.url if user.p_image else "media\image\download_lX6bjA6.jpeg",
                'first_name': user.first_name,
                'username': user.username,
                'last_name': user.last_name,
                'email': user.email,
                'gender': user.gender,
                'phone': user.phone,
                'dob': user.dob,
                'address': user.address,
                'nid': user.nid,
                'thana': Thana.objects.get(id=user.thana_id).name,
            })
        
        return Response({"users": serialized_data, "message": "User information retrieved successfully"}, status=status.HTTP_200_OK)

