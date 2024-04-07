# views.py
from rest_framework import views, status
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import OwnerSerializer, OverseerSerializer,ChangePasswordSerializer,ProfileSerilazier,OwnwerUpdateSerializer,PassResetSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.models import Owner, Overseer,Friend,Thana,User,PlanEvent,Upvote,Blog,Chat,Notification
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
from django.http import Http404


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
        #print("you are in put")
        # Deserialize the incoming data
        serializer = OwnwerUpdateSerializer(owner, data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        print(serializer.errors)
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
        print(serializer.errors)
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
    user = Owner.objects.get(username="nuha1")
    queryset = Friend.objects.filter(user1=user.id) | Friend.objects.filter(user2=user.id)
    queryset = queryset.exclude(user1=user.id) | queryset.exclude(user2=user.id)
    print(queryset)
    fndlist=[Owner.objects.get(id=fr.user1.id) for fr in queryset]
    print(fndlist)
    return queryset

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
            print("You are in changepass class")
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

from django.contrib.auth.hashers import make_password

class PassReset(views.APIView):
    def post(self, request):
        print(request.data)
        serializer = PassResetSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            new_password = serializer.validated_data['new_password']
            done = serializer.validated_data['done']
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            
            user.set_password(new_password)
            user.save()
            #print(username)
            #print(new_password)
            return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class add_fnf(APIView):
    def post(self, request):
        data = request.data
        if(str(data['user_id']) == str(data['friend_id'])):
            return Response({"message": "You can't add yourself as friend"}, status=status.HTTP_400_BAD_REQUEST)
        print(data)

        fnd=Friend.objects.filter(user1=Owner.objects.get(id=data['user_id']),user2=Owner.objects.get(id=data['friend_id']))
        fnd|=Friend.objects.filter(user2=Owner.objects.get(id=data['user_id']),user1=Owner.objects.get(id=data['friend_id']))
        if(len(fnd) > 0 and fnd[0].is_fnf == 1):
            return Response({"message": "You are already friend"}, status=status.HTTP_400_BAD_REQUEST)
        #check who send fnd request(future work)
        if(len(fnd) > 0):
            return Response({"message": "Your request for friend send"}, status=status.HTTP_400_BAD_REQUEST)
        from django.utils import timezone
        print(data['type'])
        fnd=Friend(user1=Owner.objects.get(id=data['user_id']),user2=Owner.objects.get(id=data['friend_id']),type=data['type'],f_created_date=timezone.now(),is_fnf=0)
        fnd.save()
        noti=Notification(noti_type="Bondhu",noti_msg="send you friend request",noti_sender=Owner.objects.get(id=data['user_id']),noti_receiver=Owner.objects.get(id=data['friend_id']),noti_status=0)
        noti.save()
        return Response({"message": "Friends Added successfully"}, status=status.HTTP_201_CREATED)

class update_fnf(APIView):
    def post(self, request):
        data = request.data
        if(str(data['user_id']) == str(data['friend_id'])):
            return Response({"message": "You can't add yourself as friend"}, status=status.HTTP_400_BAD_REQUEST)

        fnd=Friend.objects.filter(user1=Owner.objects.get(id=data['user_id']),user2=Owner.objects.get(id=data['friend_id']))
        fnd|=Friend.objects.filter(user2=Owner.objects.get(id=data['user_id']),user1=Owner.objects.get(id=data['friend_id']))
        #print(fnd)
        #check who send fnd request(future work)
        if(len(fnd) > 0):
            fnd[0].is_fnf= 1 if fnd[0].is_fnf== 0 else fnd[0].is_fnf
            fnd[0].type=data['type']
            fnd[0].save()
            return Response({"message": "Friends Updated successfully"}, status=status.HTTP_201_CREATED)

        return Response({"message": "Friends not find"}, status=status.HTTP_400_BAD_REQUEST)
class Delete_fnd(APIView):
    def post(self, request):
        data = request.data
        if(str(data['user_id']) == str(data['friend_id'])):
            return Response({"message": "You can't add yourself as friend"}, status=status.HTTP_400_BAD_REQUEST)

        fnd=Friend.objects.filter(user1=Owner.objects.get(id=data['user_id']),user2=Owner.objects.get(id=data['friend_id']))
        fnd|=Friend.objects.filter(user2=Owner.objects.get(id=data['user_id']),user1=Owner.objects.get(id=data['friend_id']))
        #print(fnd)
        #check who send fnd request(future work)
        if(len(fnd) > 0):
            fnd[0].delete()
            return Response({"message": "Friends Deleted successfully"}, status=status.HTTP_201_CREATED)

        return Response({"message": "Friends not find"}, status=status.HTTP_400_BAD_REQUEST)


class FriendList(APIView):
    def get(self, request):
        users = Owner.objects.all()
        userid=request.GET.get('user_id')
        print("ami esesi akhon from groupsshow")
        print(userid)
        # Serialize the data
        serialized_data = []
        for user in users:
            fnd=Friend.objects.filter(user1=Owner.objects.get(id=userid),user2=user.id)
            fnd2=Friend.objects.filter(user2=Owner.objects.get(id=userid),user1=user.id)
            fnd=fnd[0] if len(fnd) > 0 else None
            if(fnd is not None or len(fnd2)>0):
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
                        'thana': Thana.objects.get(thana=user.thana_id).thana,
                        'is_fnf': fnd.is_fnf if fnd is not None else fnd2[0].is_fnf if len(fnd2)>0 else None,
                        'type': fnd.type if fnd is not None else fnd2[0].type if len(fnd2)>0 else None,
                        'f_created_date': fnd.f_created_date if fnd is not None else  None,
                        'f_id': fnd.f_id if fnd is not None else None,
                        'abedon': 1 if fnd is not None else 0,
                        'good': fnd.user1.username if fnd is not None else None,
                        'msg': "gd night",
                        'time': "12:00",
                    })
        print(serialized_data)
        return Response({"users": serialized_data, "message": "User information retrieved successfully"}, status=status.HTTP_200_OK)



class FindFriend(APIView):
    def get(self, request):
        userid=request.GET.get('user_id')
       # users = Owner.objects.exclude(id=userid)
        users = Owner.objects.all()

        # Serialize the data
        serialized_data = []
        for user in users:
                fnd=Friend.objects.filter(user1=Owner.objects.get(id=userid),user2=user.id)
                fnd2=Friend.objects.filter(user2=Owner.objects.get(id=userid),user1=user.id)

                if(str(user.id) == str(userid)):
                    continue
                if(len(fnd)>0 and fnd[0].is_fnf==1):
                    continue
                if(len(fnd2)>0 and fnd2[0].is_fnf==1):
                    continue
                fnd=fnd[0] if len(fnd) > 0 else None
            
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
                        'thana': Thana.objects.get(thana=user.thana_id).thana,
                        'is_fnf': fnd.is_fnf if fnd is not None else fnd2[0].is_fnf if len(fnd2)>0 else None,
                        'type': fnd.type if fnd is not None else fnd2[0].type if len(fnd2)>0 else None,
                        'f_created_date': fnd.f_created_date if fnd is not None else  None,
                        'f_id': fnd.f_id if fnd is not None else None,
                        'abedon': 1 if fnd is not None else 0,
                        'good': fnd.user1.username if fnd is not None else None,
                         'status': 1 if fnd is not None else 1 if len(fnd2)>0 else 0,
                    })
        print(serialized_data)
        
        
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
#change it for email....
class OTPAPI(APIView):
    def post(self, request):
        # Extract the email address from the request data
        #print(request.data)
        username = request.data.get('input')

        # Verify the email address using an email verification API (optional)
        # You can skip the verification API and directly send the email
        # is_email_valid = self.verify_email(email_address)
        try:
            user = Owner.objects.get(username=username)
            #print(user)
            email_address = user.email
            #print(email_address)
            verification_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
            print(verification_code)
            # Send verification email with the verification code

            #uncomment when send mail....
            #self.send_verification_email(email_address, verification_code)
            return Response({"message": "Verification email sent successfully", "code": verification_code,"username":user.username}, status=status.HTTP_200_OK)
        except Owner.DoesNotExist:
                print("User not found")
                return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        

    def send_verification_email(self, email_address, verification_code):
        # Send verification email using Django's email functionality
        subject = 'Email Verification Code from Nostalgia'
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
        fndlist=[Owner.objects.get(id=fr.user1_id) for fr in queryset]
        print(fndlist)
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

class FaceCompareAPIBox:
    def __init__(self):
        api_key = "edEq6oq-Eqf3Sq4sfszoXpRQ9FHRRQGx"
        api_secret = "Ky2HfeEgU58UvJkmCt5nIe97DMEeswRy"
        url = "https://api-us.faceplusplus.com/facepp/v3/compare"

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
        

import base64
class FaceApiCompare:
    API_KEY = "edEq6oq-Eqf3Sq4sfszoXpRQ9FHRRQGx"
    API_SECRET = "Ky2HfeEgU58UvJkmCt5nIe97DMEeswRy"
    URL = "https://api-us.faceplusplus.com/facepp/v3/compare"

    def encode_image_to_base64(self, image_path):
        with open(image_path, 'rb') as img_file:
            image_content = img_file.read()
            base64_image = base64.b64encode(image_content).decode('utf-8')
        return base64_image

    def compare_images(self, image_base64_1, image_base64_2):
        # Prepare the payload for Face++ API
        payload = {
            "api_key": self.API_KEY,
            "api_secret": self.API_SECRET,
            "image_base64_1": image_base64_1,
            "image_base64_2": image_base64_2,
        }

        # Send POST request to Face++ API
        response = requests.post(self.URL, data=payload)
        response_json = response.json()

        # Process the response and return the result
        confidence = response_json.get('confidence', 0)
        threshold = 50
        if confidence >= threshold:
            result = "Match between two photos is successful with confidence: {:.2f}".format(confidence)
        else:
            result = "Match between two photos is not successful. Confidence is too low: {:.2f}".format(confidence)

        return result
    
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import base64

face_api_compare = FaceApiCompare()

from django.http import JsonResponse
from rest_framework.views import APIView
import base64

face_api_compare = FaceApiCompare()
class CompareImagesView(APIView):
    def post(self, request, *args, **kwargs):
        # Get image data from the POST request
        print(request.FILES)
        image_file1 = request.FILES.get('image1')
        image_file2 = request.FILES.get('image2')

        if not (image_file1 and image_file2):
            return JsonResponse({'error': 'Missing image data in request'}, status=400)
        print("hoise")

        # Convert images to base64 strings
        image_base64_1 = base64.b64encode(image_file1.read()).decode('utf-8')
        image_base64_2 = base64.b64encode(image_file2.read()).decode('utf-8')

        # Perform image comparison using FaceApiCompare class method
        result = face_api_compare.compare_images(image_base64_1, image_base64_2)

        # Return the comparison result as JSON response
        return JsonResponse({'result': result})


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
                'thana': Thana.objects.get(thana=user.thana).thana,
            })
        
        return Response({"buddy": serialized_data, "message": "walking buddy information retrieved successfully"}, status=status.HTTP_200_OK)

from rest_framework.response import Response
from rest_framework import status
from .models import User, Thana

class OverseerList(APIView):
    def get(self, request):
        target = request.GET.get('target')  # Assuming 'target' is passed as a query parameter
        print(target)
        if not target:
            return Response({"message": "Please provide a target value"}, status=status.HTTP_400_BAD_REQUEST)
        target="@"+target
        users = Overseer.objects.filter(username__contains=target)
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
                'relation':user.Relation,
                'thana': Thana.objects.get(id=user.thana_id).name,
            })
        
        return Response({"users": serialized_data, "message": "User information retrieved successfully"}, status=status.HTTP_200_OK)


    
from rest_framework.generics import ListAPIView, CreateAPIView
from .models import Blog,Upvote
from .serializers import BlogSerializer
from django.http import JsonResponse
class BlogListView(APIView):
    def get(self, request):
        # Retrieve all Blog objects from the database
            queryset = Blog.objects.all().order_by('-post_date', '-post_time')
            blogs_data = []
            username = request.GET.get('username')
           # print(username)

            for blog in queryset:
                #print(blog.author)
                blog_data = {
                    'id': blog.blogid,
                    'author': Owner.objects.get(username=blog.author).username,
                    'author_img': Owner.objects.get(username=blog.author).p_image.url if Owner.objects.get(username=blog.author).p_image else "/media/image/download_lsX6bjA6.jpeg",
                    'content': blog.content,
                    'post_date': blog.post_date,
                    'post_time': blog.post_time,
                    'blog_img': blog.blog_img.url if blog.blog_img else None,
                    'upvote': Upvote.objects.filter(blogid=blog.blogid).count(),
                    'is_upvoted':1 if Upvote.objects.filter(blogid=blog.blogid,Username=Owner.objects.get(username=username)).count() > 0 else 0
                }
                blogs_data.append(blog_data)
           # print(blogs_data)

            return JsonResponse(blogs_data, safe=False)

from django.http import JsonResponse
from django.views import View
from .models import Blog, Upvote

class UpvoteAPIView(APIView):
    def post(self, request):
        if request.method == 'POST':
            id = request.data['id']
            username = request.data['username']
            blog = Blog.objects.get(blogid=id)
            owner=Owner.objects.get(username=username)
            print("yo esei noti bro...")
            print(owner.username)
            upvoted = Upvote.objects.filter(
                Username=Owner.objects.get(username=username), blogid=id)
            if len(upvoted)==0:
                print("banao")
                upvote_instance = Upvote(Username=Owner.objects.get(username=username), blogid=blog)
                upvote_instance.save()
                upvote_instance1 = Upvote(Username=Owner.objects.get(username=username), blogid=blog)
                upvote_instance1.save()
                Noti=Notification(noti_type="Upvote",noti_msg="upvoted your blog",noti_sender=Owner.objects.get(username=username),noti_receiver=Owner.objects.get(username=blog.author),noti_status=0)
                Noti.save()
            if len(upvoted)==1:
                upvote_instance = Upvote(Username=Owner.objects.get(username=username), blogid=blog)
                upvote_instance.save()
                #this have to think, bcz, user knwo who withdraw his upvote
                Noti=Notification(noti_type="Upvote",noti_msg="reupvoted your blog",noti_sender=Owner.objects.get(username=username),noti_receiver=Owner.objects.get(username=blog.author),noti_status=0)
                Noti.save()
            else: 
                upvote_instance = Upvote.objects.filter(Username=owner, blogid=blog).first()
                upvote_instance.delete()
            blog=Blog.objects.get(blogid=id)
            blog_data = {
                    'id': blog.blogid,
                    'author': Owner.objects.get(username=blog.author).username,
                    'author_img': Owner.objects.get(username=blog.author).p_image.url if Owner.objects.get(username=blog.author).p_image else "/media/image/download_lsX6bjA6.jpeg",
                    'content': blog.content,
                    'post_date': blog.post_date,
                    'post_time': blog.post_time,
                    'blog_img': blog.blog_img.url if blog.blog_img else None,
                    'upvote': Upvote.objects.filter(blogid=blog.blogid).count(),
                    'is_upvoted':1 if Upvote.objects.filter(blogid=blog.blogid,Username=Owner.objects.get(username=username)).count() >  1 else 0
                }
            return JsonResponse(blog_data, safe=False)
        else:
            return JsonResponse({'message': 'Invalid request method'}, status=400)

class BlogSingleView(APIView):
    def get(self, request):
        # Retrieve all Blog objects from the database
            username = request.GET.get('username')
            print("shuno na go kotha")
            print(username)
            queryset = Blog.objects.filter(author=Owner.objects.get(username=username).id).order_by('-post_date', '-post_time')
            blogs_data = []
            print(Owner.objects.get(username=username).id)

            for blog in queryset:
                #print(blog.author)
                blog_data = {
                    'id': blog.blogid,
                    'author': Owner.objects.get(username=blog.author).username,
                    'author_img': Owner.objects.get(username=blog.author).p_image.url if Owner.objects.get(username=blog.author).p_image else "/media/image/download_lsX6bjA6.jpeg",
                    'content': blog.content,
                    'post_date': blog.post_date,
                    'post_time': blog.post_time,
                    'blog_img': blog.blog_img.url if blog.blog_img else None
                }
                blogs_data.append(blog_data)

            return JsonResponse(blogs_data, safe=False)




@method_decorator(csrf_exempt, name='dispatch')
class BlogCreateView(CreateAPIView):
    #serializer_class = BlogSerializer
    def post(self, request, *args, **kwargs):
        # Retrieve data from the request
        username = request.data['username']
        data = request.data
        user = Owner.objects.get(username=username)
        # print(data)
        blog_img = request.data.get('blog_img')
        #print(blog_img)
        if blog_img is not None:
            blog = Blog.objects.create(
                    author=user,
                    content=data['content'],
                    post_date=data['post_date'],
                    post_time=data['post_time'],
                    blog_img=blog_img if blog_img else None
                )
                # Save the blog instance
            blog.save()
        else :
            blog = Blog.objects.create(
                author=user,
                content=data['content'],
                post_date=data['post_date'],
                post_time=data['post_time'],
            )
            blog.save()
        return Response({"message": "Blog created successfully"}, status=status.HTTP_201_CREATED)
    
from .models import PlanEvent  
from .serializers import PlanEventSerializer
class PlanEventCreateAPIView(APIView):
    def post(self, request):
        fields = ['Description', 'Event_title', 'Event_start_time', 'Event_end_time',
                  'Event_start_date', 'Event_end_date', 'Address', 'Event_create_date',
                  'Event_Approve', 'E_type', 'Image', 'E_creator', 'Thana']
        data = {key: request.data[key] for key in fields if key in request.data}
        serializer = PlanEventSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PlanEventListAPIView(APIView):
    def get(self, request):
        events = PlanEvent.objects.all()
        serializer = PlanEventSerializer(events, many=True)
        return Response(serializer.data)

class PlanEventUpdateAPIView(APIView):
    def put(self, request, pk):
        event = PlanEvent.objects.get(pk=pk)
        fields = ['Description', 'Event_title', 'Event_start_time', 'Event_end_time',
                  'Event_start_date', 'Event_end_date', 'Address', 'Event_create_date',
                  'Event_Approve', 'E_type', 'Image', 'E_creator', 'Thana']
        data = {key: request.data[key] for key in fields if key in request.data}
        serializer = PlanEventSerializer(event, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        event = PlanEvent.objects.get(pk=pk)
        fields = ['Description', 'Event_title', 'Event_start_time', 'Event_end_time',
                  'Event_start_date', 'Event_end_date', 'Address', 'Event_create_date',
                  'Event_Approve', 'E_type', 'Image', 'E_creator', 'Thana']
        data = {key: request.data[key] for key in fields if key in request.data}
        serializer = PlanEventSerializer(event, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
from .models import Walk
from .serializers import WalkSerializer
from datetime import datetime
from django.db.models import Q

class WalkListView(APIView):
    def get(self, request):
        username = request.GET.get('username')
        print("ami hatar manush khujte assi.....")
        user = Owner.objects.get(username=username)
        print(user.username)
        #walks = Walk.objects.filter(Q(w_creator=user) | Q(walkmember__username=user)).order_by('walk_date').distinct()
        walks=Walk.objects.all()
        walks_data = []
        for walk in walks:
            #print(walk.w_creator.p_image)
            walk_data = {
                'id': walk.walk_id,
                'userid': walk.w_creator.id,
                'w_creator': walk.w_creator.username,
                'img': walk.w_creator.p_image.url if walk.w_creator.p_image else "/media/image/download_lsX6bjA6.jpeg",
                'walk_name': walk.walk_name,
                'propose': walk.propose_date,
                'date': datetime.strptime(str(walk.walk_date), '%Y-%m-%d').strftime('%d %B %Y'),
                'privacy': walk.privacy,
                'end': datetime.strptime(str(walk.end_date), '%Y-%m-%d').strftime('%d %B %Y'),
                'location': walk.address,
                'member': 1 if WalkMember.objects.filter(walk_id=walk.walk_id,username=user).exists() else 0,
                'not_ac': 1 if WalkMember.objects.filter(walk_id=walk.walk_id,username=user, accept=0).exists() else 0,
                'cancel': 1 if WalkMember.objects.filter(walk_id=walk.walk_id,username=user, cancel=1).exists() else 0,
                #time banate hbe
            }
            walks_data.append(walk_data)
        print(walks_data)
        return Response(walks_data, status=status.HTTP_200_OK)

    @csrf_exempt
    def post(self, request):
        data = request.data
        username = data.get('w_creator')
        user = Owner.objects.get(username=username)
        data['propose_date'] = data['walk_date']
        data['privacy'] = "Bondhu"
        data['w_creator'] = user.id
        serializer = WalkSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            walk_member=WalkMember(walk_id=Walk.objects.get(walk_id=serializer.data['walk_id']),username=user,accept=1,cancel=0)
            walk_member.save()
            print("walk member created")
            return Response({"message": "Walk created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class NotificationView(APIView):
    def get(self, request):
        username = request.GET.get('username')
        print("notification Bro....")
        print(username)
        noti = Notification.objects.filter(noti_receiver=Owner.objects.get(username=username)).order_by('noti_date','-noti_time')
        noti_data = []
        for n in noti:
            noti_data.append({
                'id': n.noti_id,
                'sender': n.noti_sender.username,
                'img': n.noti_sender.p_image.url if n.noti_sender.p_image else "/media/image/download_lsX6bjA6.jpeg",
                'msg': n.noti_msg,
                'date': n.noti_date,
                'time': n.noti_time,
                'type': n.noti_type,
                'status': n.noti_status
            })
        return Response(noti_data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        print(data)
        username = data.get('username')
        user = Owner.objects.get(username=username)
        data['noti_sender'] = user.id
        data['noti_date'] = datetime.now().strftime('%Y-%m-%d')
        data['noti_time'] = datetime.now().strftime('%H:%M:%S')
        serializer = NotificationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Notification created successfully"}, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from .models import Comment
from datetime import datetime, timedelta    

from datetime import datetime

def format_time_ago(timestamp):
    # Calculate the time difference
    time_difference = datetime.utcnow() - timestamp

    # Convert time difference to days, hours, and minutes
    days_difference = time_difference.days
    minutes_difference = time_difference.seconds // 60
    hours_difference = minutes_difference // 60

    if days_difference > 30:
        months_difference = days_difference // 30
        return f"{months_difference} months ago"
    elif days_difference >= 2:
        return f"{days_difference} days ago"
    elif days_difference == 1:
        return "1 day ago"
    elif hours_difference >= 2:
        return f"{hours_difference} hours ago"
    elif hours_difference == 1:
        return "1 hour ago"
    elif minutes_difference >= 2:
        return f"{minutes_difference} minutes ago"
    else:
        return "just now"

class BlogCommentsView(APIView):
    def get(self, request):
           #Retrieve all Blog objects from the database
           # username = request.GET.get('username')
            print("retrive comment")
            #print(username)
            blog = request.GET.get('blog')
            blog=Blog.objects.get(blogid=blog)
            print(blog.content)
            queryset = Comment.objects.filter(blogid=blog).order_by( '-time')
            blogs_data = []
            #print(Owner.objects.get(username=username).id)
            for blog in queryset:
                #print(blog.comment)
                #timestamp = blog.time.replace(tzinfo=timezone.utc)
                blog_data = {
                    'id': blog.cmnt_id,
                    'author': blog.username.username,
                    'author_img': Owner.objects.get(username=blog.username).p_image.url if Owner.objects.get(username=blog.username).p_image else "/media/image/download_lsX6bjA6.jpeg",
                    'content': blog.comment,
                    'time': blog.time,
                    'blog': blog.blogid.blogid
                }
                blogs_data.append(blog_data)
            print(blogs_data)
            return JsonResponse(blogs_data, safe=False)
from django.utils import timezone 
@method_decorator(csrf_exempt, name='dispatch')
class CommentCreateView(CreateAPIView):
    #serializer_class = BlogSerializer
    def post(self, request, *args, **kwargs):
        print("comment create")
        print(request.data)
        # Retrieve data from the request
        username = request.data['author']
        print(username)
        data = request.data
        user = Owner.objects.get(username=username)
        # print(data)
        blog_img = ""#request.data.get('blog_img')
        #print(blog_img)
        if blog_img is not None:
            blog = Comment.objects.create(
                   blogid=Blog.objects.get(blogid=data['blog']),
                    username=user,
                    comment=data['content'],
                    time = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
                )
                # Save the blog instance
            blog.save()
        else :
            blog = Blog.objects.create(
                blogid=Blog.objects.get(blogid=data['blog']),
                username=user,
                comment=data['content'],
                time= timezone.now().strftime('%Y-%m-%d %H:%M:%S')
            )
            blog.save()
        return Response({"message": "Comment created successfully"}, status=status.HTTP_201_CREATED)


from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from django.db.models import Count
from django.db.models import F, ExpressionWrapper, fields
from django.db.models.functions import Length
from django.db.models import FloatField
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class HTimeline(APIView):
    def get(self, request):
        username=request.GET.get("username")
        print(username)
        user=User.objects.get(username=username)
        print(user)
        user_blogs = Blog.objects.filter(author__username=username)
        user_comments = Comment.objects.filter(username__username=username)

        user_content=[]
        for blog in user_blogs:
            user_content.append(blog.content)
        for comment in user_comments:
            user_content.append(comment.comment)

        # Get all blogs excluding the user's blogs
        all_blogs = Blog.objects.exclude(author__username=username)
        # Combine the content of all blogs and comments
        all_content = []
        for blog in all_blogs:
            all_content.append(blog.content)
            # Also consider comments associated with this blog
            comments = Comment.objects.filter(blogid=blog.blogid)
            for comment in comments:
                all_content.append(comment.comment)

        # Calculate TF-IDF vectors
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(user_content + all_content)
        print(tfidf_matrix)

        # Calculate cosine similarity
        user_tfidf = tfidf_matrix[:len(user_content)]
        all_tfidf = tfidf_matrix[len(user_content):]
        similarity_matrix = cosine_similarity(user_tfidf, all_tfidf)

        # Sort blogs based on cosine similarity
        similarity_scores = similarity_matrix.mean(axis=0)  # Taking mean across user content
        sorted_indices = [int(i) for i in np.argsort(similarity_scores)[::-1]]
        # Retrieve sorted blogs
        sorted_blogs = [all_blogs[i] for i in sorted_indices]

        blogs_data = []
        for blog in sorted_blogs:
            blog_data = {
                'id': blog.blogid,
                'author': blog.author.username,
                'author_img': blog.author.p_image.url if blog.author.p_image else "/media/image/download_lsX6bjA6.jpeg",
                'content': blog.content,
                'post_date': blog.post_date,
                'post_time': blog.post_time,
                'blog_img': blog.blog_img.url if blog.blog_img else None,
                'upvote': blog.upvote_set.count(),
                'is_upvoted': 1 if blog.upvote_set.filter(Username__username=username).exists() else 0
            }
            blogs_data.append(blog_data)

        return Response(blogs_data)


from .models import WalkMember
class WalkMembers(APIView):
    def get_age(self, dob):
        today = datetime.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        return age

    def get(self,request):
        walk_id=request.GET.get('id')
        walk=Walk.objects.get(walk_id=walk_id)
        members=WalkMember.objects.filter(walk_id=walk_id,cancel=0,accept=1)
        members_data=[]
        print("ami hatar manush khuji akhon!")
        for member in members:
            members_data.append({
                'id': member.username.id,
                'username': member.username.username,
                'img': member.username.p_image.url if member.username.p_image else "/media/image/download_lsX6bjA6.jpeg",
                'first_name': member.username.first_name,
                'last_name': member.username.last_name,
                'email': member.username.email,
                'phone': member.username.phone,
                'dob': self.get_age(member.username.dob),
                'gender': member.username.gender
            })
        print(members_data)
        return Response(members_data)

class Walk_request(APIView):
    def post(self,request):
        walk_id=request.data['id']
        username=request.data['username']
        walk=Walk.objects.get(walk_id=walk_id)
        bot=WalkMember.objects.filter(walk_id=walk,username=Owner.objects.get(username=username))
        if(len(bot)>0):
            return Response({"user": bot[0].username.username})      
        members=WalkMember.objects.create(username=Owner.objects.get(username=username),walk_id=Walk.objects.get(walk_id=walk_id),cancel=0,accept=0)
        members.save()
        print("accept koro na?")
        return Response({"message": "Request sent successfully"}, status=status.HTTP_201_CREATED)

class update_member(APIView):
    def post(self,request):
        walk_id=request.data['id']
        username=request.data['username']
        walk=Walk.objects.get(walk_id=walk_id)
        bot=WalkMember.objects.filter(walk_id=walk,username=Owner.objects.get(username=username))
        if(len(bot)>0):
            return Response({"user": bot[0].username.username})      
        members=WalkMember.objects.create(username=Owner.objects.get(username=username),walk_id=Walk.objects.get(walk_id=walk_id),cancel=0,accept=0)
        members.save()
        print("accept koro na?")
        return Response({"message": "Request sent successfully"}, status=status.HTTP_201_CREATED)

class WalkNotMember(APIView):
    def get_age(self, dob):
        today = datetime.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        return age 

    def get(self,request):
        walk_id=request.GET.get('id')
        walk=Walk.objects.get(walk_id=walk_id)
        members=WalkMember.objects.filter(walk_id=walk_id,accept=0)
        print(members)
        members_data=[]
        print("moner mto kw nai!")
        for member in members:
            members_data.append({
                'id': member.username.id,
                'username': member.username.username,
                'img': member.username.p_image.url if member.username.p_image else "/media/image/download_lsX6bjA6.jpeg",
                'first_name': member.username.first_name,
                'last_name': member.username.last_name,
                'email': member.username.email,
                'phone': member.username.phone,
                'dob': self.get_age(member.username.dob),
                'gender': member.username.gender 
            
            })
        print(members_data) 
        return Response(members_data)

class Handlemember(APIView):
    def post(self,request):
        if request.data['type'] == 'confirm':
            walk_id=request.data['walk_id']
            user_id=request.data['id']
            user=Owner.objects.get(id=user_id)
            walk=Walk.objects.get(walk_id=walk_id)
            members=WalkMember.objects.filter(walk_id=walk,username=user)
            print(members)
            if(len(members)>0):
                members[0].accept=1
                members[0].save()
                return Response({"user": members[0].username.username})
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
from .models import Group
class Add_group(APIView):
    def post(self,request):
        data=request.data
        print(data)
        if(Group.objects.filter(G_username=data['username']).exists()):
            return Response({"msg": "Group already exists"})
        group=Group.objects.create(G_name=data['name'],Creator=Owner.objects.get(id=data['id']),CreatedDate=datetime.now().strftime('%Y-%m-%d'),G_username=data['username'],Privacy=data['privacy'],Topic=data['topic'],time=datetime.now().strftime('%H:%M:%S'))
        group.save()
        return Response({"message": "Group created successfully"}, status=status.HTTP_201_CREATED)
        
class My_Group(APIView):
    def get(self,request):
        username=request.GET.get('user_id')
        user=Owner.objects.get(id=username)
        groups=Group.objects.all()
        groups_data=[]
        for group in groups:
            groups_data.append({
                'username': group.G_username,
                'name': group.G_name,
                'creator': group.Creator.username,
                'created_date': group.CreatedDate,
                'privacy': group.Privacy,
                'topic': group.Topic,
                'time': group.time,
                'gp': group.Creator.p_image.url if group.Creator.p_image else "/media/image/download_lsX6bjA6.jpeg",

            })
        return Response(groups_data)

class GroupProfile(APIView):
    def get(self,request,username):
        print("asi nai grope profile")
        print(username)
        group=Group.objects.get(G_username=username)
        data={
            'username': group.G_username,
            'name': group.G_name,
            'creator': group.Creator.username,
            'created_date': group.CreatedDate,
            'privacy': group.Privacy,
            'topic': group.Topic,
            'time': group.time,
            'gp': group.Creator.p_image.url if group.Creator.p_image else "/media/image/download_lsX6bjA6.jpeg",
        }
        print(data)

        return Response(data)
class GP_post(APIView):
    def get(self,request,username):
        group=Group.objects.get(G_username=username)
        posts=GroupPost.objects.filter(group_id=group)
        posts_data=[]
        for post in posts:
            posts_data.append({
                'id': post.post_id,
                'author': post.username.username,
                'author_img': post.username.p_image.url if post.username.p_image else "/media/image/download_lsX6bjA6.jpeg",
                'content': post.content,
                'post_date': post.post_date,
                'post_time': post.post_time,
                'post_img': post.post_img.url if post.post_img else None,
            #     'upvote': GroupUpvote.objects.filter(post_id=post).count(),
            #     'is_upvoted': 1 if GroupUpvote.objects.filter(post_id=post,Username=Owner.objects.get(username=username)).exists() else 0
             })
        return Response(posts_data)


class GT_post(APIView):
    def get(self,request):
        username=request.GET.get('username')
        print(username)


from django.http import JsonResponse
from django.views import View
from .models import GroupPost, GroupUpvote

class GroupUpvoteAPIView(APIView):
    def post(self, request):
        if request.method == 'POST':
            id = request.data['id']
            username = request.data['username']
            blog = GroupPost.objects.get(blogid=id)
            owner=Owner.objects.get(username=username)
            print("yo esei noti bro...")
            print(owner.username)
            upvoted = GroupUpvote.objects.filter(
                Username=Owner.objects.get(username=username), blogid=id)
            if len(upvoted)==0:
                print("banao")
                upvote_instance = GroupUpvote(Username=Owner.objects.get(username=username), blogid=blog)
                upvote_instance.save()
                upvote_instance1 = GroupUpvote(Username=Owner.objects.get(username=username), blogid=blog)
                upvote_instance1.save()
                Noti=Notification(noti_type="Upvote",noti_msg="upvoted your blog",noti_sender=Owner.objects.get(username=username),noti_receiver=Owner.objects.get(username=blog.author),noti_status=0)
                Noti.save()
            if len(upvoted)==1:
                upvote_instance = GroupUpvote(Username=Owner.objects.get(username=username), blogid=blog)
                upvote_instance.save()
                #this have to think, bcz, user knwo who withdraw his upvote
                Noti=Notification(noti_type="Upvote",noti_msg="reupvoted your blog",noti_sender=Owner.objects.get(username=username),noti_receiver=Owner.objects.get(username=blog.author),noti_status=0)
                Noti.save()
            else: 
                upvote_instance = GroupUpvote.objects.filter(Username=owner, blogid=blog).first()
                upvote_instance.delete()
            blog=GroupPost.objects.get(blogid=id)
            blog_data = {
                    'id': blog.blogid,
                    'author': Owner.objects.get(username=blog.author).username,
                    'author_img': Owner.objects.get(username=blog.author).p_image.url if Owner.objects.get(username=blog.author).p_image else "/media/image/download_lsX6bjA6.jpeg",
                    'content': blog.content,
                    'post_date': blog.post_date,
                    'post_time': blog.post_time,
                    'blog_img': blog.blog_img.url if blog.blog_img else None,
                    'upvote': GroupUpvote.objects.filter(blogid=blog.blogid).count(),
                    'is_upvoted':1 if GroupUpvote.objects.filter(blogid=blog.blogid,Username=Owner.objects.get(username=username)).count() >  1 else 0
                }
            return JsonResponse(blog_data, safe=False)
        else:
            return JsonResponse({'message': 'Invalid request method'}, status=400)

