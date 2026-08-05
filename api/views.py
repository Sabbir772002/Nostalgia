          
import base64
import io
import json
import os
import random
import string
from datetime import datetime, timedelta

import numpy as np
import requests
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions, status, views
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.views import APIView

from api.ai_client import AIEmbeddingClient
from api.cache_utils import get_cached_or_set, invalidate_feed_cache, invalidate_post_cache
from .services.auth import (
    build_otp_response,
    change_password,
    create_owner_account,
    create_overseer_account,
    login_as_owner_or_overseer,
    reset_password,
)
from .services.blogs import (
    blog_detail,
    create_blog,
    create_comment,
    list_blogs,
    list_comments,
    record_blog_view,
    single_user_blogs,
    timeline_posts,
    toggle_upvote,
)
from .services.groups import (
    add_group_post,
    create_group,
    delete_group_membership,
    group_members_payload,
    group_posts_for_group,
    group_posts_for_member_feed,
    group_profile_payload,
    group_request_action,
    join_group,
    list_user_groups,
    request_members_payload,
    update_group_payload,
)
from .services.activity import (
    done_action,
    done_get,
    event_members_payload,
    event_not_member_payload,
    event_request_action,
    handle_event_member,
    handle_trip_member,
    handle_walk_member,
    medtime_get,
    medtime_post,
    medication_create_action,
    medication_list_payload,
    trip_members_payload,
    trip_not_member_payload,
    trip_request_action,
    trip_update_action,
    walk_members_payload,
    walk_not_member_payload,
    walk_request_action,
)
from .services.discovery import (
    add_handler_action,
    add_info_payload,
    find_district_payload,
    find_thana_payload,
    search_blog_payload,
    search_friend_box_payload,
    search_friend_payload,
)
from .serializers import (
    ChangePasswordSerializer,
    FriendSerializer,
    NotificationSerializer,
    OwnerSerializer,
    OwnerUpdateSerializer,
    OverseerSerializer,
    PassResetSerializer,
    PlanEventSerializer,
    UserLoginSerializer,
    WalkSerializer,
)
from api.models import (
    BlogView,
    Caregiver,
    Chat,
    Comment,
    DoneMed,
    Division,
    Event,
    Friend,
    GroupMember,
    GroupPost,
    JoinEvent,
    MedAlert,
    Medication,
    Notification,
    Owner,
    Overseer,
    Thana,
    Trip,
    TripMember,
    Walk,
    WalkMember,
    User,
    Verified,
    CommunityGroup as Group,
)
from .services.social import (
    delete_friend_request_payload,
    friend_list_payload,
    friend_request_payload,
    friend_suggestion_payload,
    profile_payload,
    update_friend_request_payload,
)
from .services.recommendations import (
    recommended_event_payload,
    recommended_feed_posts,
    recommended_friend_suggestions,
    recommended_group_payload,
    recommended_trip_payload,
    recommended_walk_payload,
)
from .services.vision import FaceApiCompareService, compare_uploaded_images

                                
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
            overseer = Overseer.objects.get(pk=pk)
        except Overseer.DoesNotExist:
            return Response({"error": "Overseer not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = OverseerSerializer(overseer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        try:
            overseer = Overseer.objects.get(pk=pk)
        except Overseer.DoesNotExist:
            return Response({"error": "Overseer not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = OverseerSerializer(overseer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                            
@method_decorator(csrf_exempt, name='dispatch')
class Owner_update(APIView):
    def put(self, request, username):
        try:
            owner = Owner.objects.get(username=username)
            serializer = OwnerUpdateSerializer(owner, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Owner.DoesNotExist:
            try:
                overseer = Overseer.objects.get(username=username)
                serializer = OverseerSerializer(overseer, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                print(serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Overseer.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        try:
            owner = Owner.objects.get(pk=pk)
        except Owner.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = OwnerSerializer(owner, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                              
@method_decorator(csrf_exempt, name='dispatch')
class sign(APIView):
    def post(self, request):
        serializer, user = create_owner_account(request.data)
        if user is not None:
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                                 
@method_decorator(csrf_exempt, name='dispatch')
class _sign(views.APIView):
    def post(self, request):
        serializer, user = create_overseer_account(request.data)
        if user is not None:
            return Response({"message": "User created successfully", "user_id": user.id}, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                               
from django.contrib.auth import authenticate, login

class UserLogin(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (SessionAuthentication,)
    def post(self, request):
        data = request.data
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
        if username and password:
            result = login_as_owner_or_overseer(request, username, password)
            if result is not None:
                return Response(result, status=status.HTTP_200_OK)
        return Response({'auth': False}, status=status.HTTP_401_UNAUTHORIZED)

                                 
class show(views.APIView):
    def post(self, request):
        if request.user.is_authenticated:
            return Response({'authenticated boSS!': True}, status=status.HTTP_200_OK)
        return Response({'authenticated': False}, status=status.HTTP_401_UNAUTHORIZED)

                                  
def friends(request):
    user = Owner.objects.get(username="nuha1")
    queryset = Friend.objects.filter(user1=user.id) | Friend.objects.filter(user2=user.id)
    queryset = queryset.exclude(user1=user.id) | queryset.exclude(user2=user.id)
    print(queryset)
    fndlist = [Owner.objects.get(id=fr.user1.id) for fr in queryset]
    print(fndlist)
    return queryset

                                   
class MyAPIView(views.APIView):
    def get(self, request):
        name = request.GET.get('name')
        queryset = MyModel.objects.all()
        if name:
            queryset = queryset.filter(name=name)
        serializer = MyModelSerializer(queryset, many=True)
        return Response(serializer.data)

                               
class ChangePass(views.APIView):
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            success, payload = change_password(
                serializer.validated_data['username'],
                serializer.validated_data['old_password'],
                serializer.validated_data['new_password'],
            )
            if success:
                return Response(payload, status=status.HTTP_200_OK)
            return Response({'error': payload}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                                        
class PassReset(views.APIView):
    def post(self, request):
        serializer = PassResetSerializer(data=request.data)
        if serializer.is_valid():
            success, payload = reset_password(
                serializer.validated_data['username'],
                serializer.validated_data['new_password'],
            )
            if success:
                return Response(payload, status=status.HTTP_200_OK)
            return Response(payload, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                                 
class add_fnf(APIView):
    def post(self, request):
        data = request.data
        success, payload, code = friend_request_payload(data['user_id'], data['friend_id'], data['type'])
        return Response(payload, status=code)

class update_fnf(APIView):
    def post(self, request):
        data = request.data
        success, payload, code = update_friend_request_payload(data['user_id'], data['friend_id'], data['type'])
        return Response(payload, status=code)

class Delete_fnd(APIView):
    def post(self, request):
        data = request.data
        success, payload, code = delete_friend_request_payload(data['user_id'], data['friend_id'])
        return Response(payload, status=code)

class FriendList(APIView):
    def get(self, request):
        userid = request.GET.get('user_id')
        serialized_data = friend_list_payload(userid)
        return Response({"users": serialized_data, "message": "User information retrieved successfully"}, status=status.HTTP_200_OK)

                                             
class FindFriend(APIView):
    def get(self, request):
        userid = request.GET.get('user_id')
        success, payload, message = friend_suggestion_payload(userid)
        if success and isinstance(payload, list) and message == "AI Recommended buddies retrieved successfully":
            return Response({"users": payload, "message": message}, status=status.HTTP_200_OK)
        return Response({"users": payload, "message": message}, status=status.HTTP_200_OK)

                                  
                                                        
                                  

                                    
class RecommendedFeedView(APIView):
    """
    Returns a ranked feed of blog posts using AI similarity + popularity signals.
    """
    def get(self, request):
        username = request.GET.get("username")
        if not username:
            return Response({"error": "Username parameter is required"}, status=400)
        recommended_posts = recommended_feed_posts(username)
                                  
        return Response(recommended_posts, status=200)

                                          
HTimeline = RecommendedFeedView

                                           
class RecommendedFriendsView(APIView):
    """
    Returns a ranked list of friend suggestions using location, walk style, and AI embedding similarity.
    """
    def get(self, request):
        username = request.GET.get('username')
        user_id = request.GET.get('user_id')
        suggestions = recommended_friend_suggestions(username=username, user_id=user_id)
        if suggestions is None:
            return Response({"error": "user_id or username required"}, status=400)

        return Response({"users": suggestions, "message": "User suggestions retrieved successfully"}, status=status.HTTP_200_OK)

               
FriendSugg = RecommendedFriendsView

                          
class RecommendedGroupsView(APIView):
    """
    Returns a ranked list of community groups using AI topic similarity with the user.
    """
    def get(self, request):
        user_id = request.GET.get('user_id')
        if not user_id:
            return Response([], status=200)
        return Response(recommended_group_payload(user_id), status=200)

               
Not_My_Group = RecommendedGroupsView

                         
class RecommendedTripsView(APIView):
    """
    Returns a ranked list of trips using AI similarity with the user profile.
    """
    def get(self, request):
        username = request.GET.get('username')
        return Response(recommended_trip_payload(username), status=status.HTTP_200_OK)

    def post(self, request):
                                               
        user = Owner.objects.get(username=request.data["t_creator"])
        data = request.data
        trip = Trip.objects.create(
            name=data['trip_name'],
            Creator=Owner.objects.get(username=data['t_creator']),
            Location=data['address'],
            start_date=data['start_date'],
            propose_date=data['propose_date'],
            end_date=data['end_date'],
            Privacy=data['privacy'],
            Thana=Thana.objects.get(thana=data['thana']),
            guide=data['guide']
        )
        trip.save()
        return Response({"message": "Trip Created successfully"}, status=status.HTTP_200_OK)

               
TripListView = RecommendedTripsView

                                           
class RecommendedWalksView(APIView):
    """
    Returns a ranked list of walks using AI similarity with the user's profile, plus existing logic.
    """
    def get(self, request):
        username = request.GET.get('username')
        payload, code = recommended_walk_payload(username)
        return Response(payload, status=code)

    @csrf_exempt
    def post(self, request):
                                               
        data = request.data
        username = data.get('w_creator')
        user = Owner.objects.get(username=username)
        data['propose_date'] = data['walk_date']
        data['privacy'] = "Bondhu"
        data['w_creator'] = user.id
        serializer = WalkSerializer(data=data)
        if serializer.is_valid() and data.get('type') == "Update":
            walk = Walk.objects.get(walk_id=data['id'])
            walk.walk_name = data['walk_name']
            walk.walk_date = data['walk_date']
            walk.end_date = data['end_date']
            walk.address = data['address']
            walk.time = data['time']
            walk.save()
            return Response({"message": "Walk updated successfully"}, status=status.HTTP_201_CREATED)
        if serializer.is_valid():
            serializer.save()
            walk_member = WalkMember(walk_id=Walk.objects.get(walk_id=serializer.data['walk_id']), username=user, accept=1, cancel=0)
            walk_member.save()
            return Response({"message": "Walk created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

               
WalkListView = RecommendedWalksView

                                            
class RecommendedEventsView(APIView):
    """
    Returns a ranked list of events using AI similarity with the user profile.
    """
    def get(self, request):
        username = request.GET.get('username')
        payload, code = recommended_event_payload(username)
        return Response(payload, status=code)

    def post(self, request):
                                                
        user = Owner.objects.get(username=request.data["e_creator"])
        data = request.data
        event = Event.objects.create(
            E_creator=Owner.objects.get(username=data['e_creator']),
            Event_title=data['title'],
            start_date=data['start_date'],
            create_date=data['create_date'],
            end_date=data['end_date'],
            privacy=data['privacy'],
            Address=data['address'],
            Approve=1,
            start_time=data['start_time'],
            end_time=data['end_time'],
            Description=data['Description'],
            E_type=data['type'],
            Thana=Thana.objects.get(thana=data['thana'])
        )
        event.save()
        return Response({"message": "Event Created successfully"}, status=status.HTTP_200_OK)

               
EventListView = RecommendedEventsView

                                  
                                        
                                  

                   
class OTPAPI(APIView):
    def post(self, request):
        username = request.data.get('input')
        success, payload = build_otp_response(username)
        if success:
            return Response(payload, status=status.HTTP_200_OK)
        return Response(payload, status=status.HTTP_404_NOT_FOUND)

                       
class Profile(APIView):
    def get(self, request, username):
        user2 = request.GET.get('user')
        result = profile_payload(username, user2)
        if result["ok"]:
            return Response(result["data"], status=status.HTTP_200_OK)
        return Response(result["data"], status=status.HTTP_404_NOT_FOUND)

                             
class BlogListView(APIView):
    def get(self, request):
        username = request.GET.get('username')
        try:
            page = int(request.GET.get('page', 1))
        except (ValueError, TypeError):
            page = 1
        try:
            page_size = int(request.GET.get('page_size', 10))
        except (ValueError, TypeError):
            page_size = 10

        cache_key = f"blog_list_{username}_p{page}_s{page_size}"
        data = get_cached_or_set(cache_key, lambda: list_blogs(username, page, page_size), timeout=60)
        if 'page' not in request.GET:
            return JsonResponse(data.get("posts", []), safe=False)
        return JsonResponse(data, safe=False)


class HTimeline(APIView):
    """
    Paginated & Redis-cached Home Timeline endpoint.
    Cache key: htimeline_{username}_p{page}_s{page_size}
    """
    def get(self, request):
        username = request.GET.get('username')
        try:
            page = int(request.GET.get('page', 1))
        except (ValueError, TypeError):
            page = 1
        try:
            page_size = int(request.GET.get('page_size', 10))
        except (ValueError, TypeError):
            page_size = 10

        cache_key = f"htimeline_{username}_p{page}_s{page_size}"
        data = get_cached_or_set(cache_key, lambda: timeline_posts(username, page, page_size), timeout=60)
        if 'page' not in request.GET:
            return JsonResponse(data.get("posts", []), safe=False)
        return JsonResponse(data, safe=False)


class UpvoteAPIView(APIView):
    def post(self, request):
        if request.method == 'POST':
            id = request.data.get('id') or request.data.get('blog_id') or request.data.get('blog')
            username = request.data.get('username') or request.data.get('author')
            if not id or not username:
                return JsonResponse({'error': 'id and username are required'}, status=400)
            try:
                blog_data = toggle_upvote(id, username)
            except (Blog.DoesNotExist, Owner.DoesNotExist):
                return JsonResponse({'error': 'Blog or Owner not found'}, status=404)
            return JsonResponse(blog_data, safe=False)
        else:
            return JsonResponse({'message': 'Invalid request method'}, status=400)

class BlogSingleView(APIView):
    def get(self, request):
        username = request.GET.get('username')
        return JsonResponse(single_user_blogs(username), safe=False)

@method_decorator(csrf_exempt, name='dispatch')
class BlogCreateView(CreateAPIView):
    def post(self, request, *args, **kwargs):
        username = request.data['username']
        data = request.data
        blog = create_blog(username, data)

        try:
            from api.tasks import generate_post_vector_task
            generate_post_vector_task.enqueue(post_id=blog.blogid)
        except Exception as e:
            logger.warning(f"Failed to enqueue generate_post_vector_task: {e}")

        return Response({"message": "Blog created successfully"}, status=status.HTTP_201_CREATED)

                                   
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

                            
class NotificationView(APIView):
    def get(self, request):
        username = request.GET.get('username')
        noti = Notification.objects.filter(noti_receiver=Owner.objects.get(username=username)).order_by('-noti_date', '-noti_time')
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

                        
class BlogCommentsView(APIView):
    def get(self, request):
        blog = request.GET.get('blog')
        return JsonResponse(list_comments(blog), safe=False)

@method_decorator(csrf_exempt, name='dispatch')
class CommentCreateView(CreateAPIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        username = data.get('author') or data.get('username')
        blog_id = data.get('blog') or data.get('blog_id') or data.get('id')
        content = data.get('content') or data.get('comment')

        if not username or not blog_id or not content:
            return Response({"error": "author, blog, and content are required fields"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            _, payload = create_comment(username, blog_id, content)
            return Response(payload, status=status.HTTP_201_CREATED)
        except (Owner.DoesNotExist, Blog.DoesNotExist) as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

                                            
class WalkMembers(APIView):
    def get_age(self, dob):
        today = datetime.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        return age

    def get(self, request):
        walk_id = request.GET.get('id')
        walk = Walk.objects.get(walk_id=walk_id)
        members = WalkMember.objects.filter(walk_id=walk_id, cancel=0, accept=1)
        members_data = []
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
        return Response(members_data)

class Walk_request(APIView):
    def post(self, request):
        walk_id = request.data['id']
        username = request.data['username']
        walk = Walk.objects.get(walk_id=walk_id)
        bot = WalkMember.objects.filter(walk_id=walk, username=Owner.objects.get(username=username))
        if len(bot) > 0:
            return Response({"user": bot[0].username.username})
        members = WalkMember.objects.create(username=Owner.objects.get(username=username), walk_id=Walk.objects.get(walk_id=walk_id), cancel=0, accept=0)
        members.save()
        return Response({"message": "Request sent successfully"}, status=status.HTTP_201_CREATED)

class WalkNotMember(APIView):
    def get_age(self, dob):
        today = datetime.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        return age

    def get(self, request):
        walk_id = request.GET.get('id')
        walk = Walk.objects.get(walk_id=walk_id)
        members = WalkMember.objects.filter(walk_id=walk_id, accept=0)
        members_data = []
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
        return Response(members_data)

class Handlemember(APIView):
    def post(self, request):
        if request.data['type'] == 'confirm':
            walk_id = request.data['walk_id']
            user_id = request.data['id']
            user = Owner.objects.get(id=user_id)
            walk = Walk.objects.get(walk_id=walk_id)
            members = WalkMember.objects.filter(walk_id=walk, username=user)
            if len(members) > 0:
                members[0].accept = 1
                members[0].save()
                return Response({"user": members[0].username.username})
        if request.data['type'] == 'delete':
            walk_id = request.data['walk_id']
            user_id = request.data['id']
            user = Owner.objects.get(id=user_id)
            walk = Walk.objects.get(walk_id=walk_id)
            members = WalkMember.objects.filter(walk_id=walk, username=user)
            if len(members) > 0:
                members[0].delete()
                return Response({"user": members[0].username.username})
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

                           
class Add_group(APIView):
    def post(self, request):
        success, payload, code = create_group(request.data)
        return Response(payload, status=code)

class My_Group(APIView):
    def get(self, request):
        username = request.GET.get('user_id')
        return Response(list_user_groups(username))

                                                             
                                                                                              

class GroupProfile(APIView):
    def get(self, request, username):
        return Response(group_profile_payload(username, request.GET.get('user_id')))

class GP_post(APIView):
    def get(self, request):
        username = request.GET.get('username')
        return Response(group_posts_for_group(username))

class GT_post(APIView):
    def get(self, request):
        username = request.GET.get('username')
        return Response(group_posts_for_member_feed(username))

class JoinGroup(APIView):
    def post(self, request):
        success, payload, code = join_group(request.data)
        return Response(payload, status=code)

@method_decorator(csrf_exempt, name='dispatch')
class AddGroupPost(CreateAPIView):
    def post(self, request, *args, **kwargs):
        return Response(add_group_post(request.data), status=status.HTTP_201_CREATED)

class GroupMembers(APIView):
    def get(self, request):
        username = request.GET.get('username')
        return Response(group_members_payload(username))

class RequestMembers(APIView):
    def get(self, request):
        username = request.GET.get('username')
        return Response(request_members_payload(username))

class GroupRequest(APIView):
    def post(self, request):
        success, payload, code = group_request_action(request.data)
        return Response(payload, status=code)

                                                       
try:
    import easyocr
    import cv2
    EASYOCR_AVAILABLE = True
except ImportError:
    EASYOCR_AVAILABLE = False
    easyocr = None
    cv2 = None

class NIDImage(APIView):
    def post(self, request):
                                                           
                                                          
        return Response({"message": "NID processing done"}, status=status.HTTP_200_OK)

                         
class CareGiver(APIView):
    def get(self, request):
        caregivers = Caregiver.objects.all()
        caregivers_data = []
        for caregiver in caregivers:
            caregivers_data.append({
                'id': caregiver.caregiver_id,
                'name': caregiver.name,
                'img': "/media/images/download.jpeg",
                'email': caregiver.email,
                'phone': caregiver.phone,
                'dob': caregiver.dob,
                'experience': caregiver.experience,
                'gender': caregiver.gender,
                'type': caregiver.type.type,
                'hname': caregiver.h_id.h_name,
                'branch': caregiver.h_id.branch,
                'thana': caregiver.h_id.thana.thana,
                'location': caregiver.h_id.h_location
            })
        return Response(caregivers_data)

                                                         
class EventMembers(APIView):
    def get(self, request):
        event_id = request.GET.get('id')
        return Response(event_members_payload(event_id))

class EventNotMember(APIView):
    def get(self, request):
        event_id = request.GET.get('id')
        return Response(event_not_member_payload(event_id))

class HandleEventmember(APIView):
    def post(self, request):
        success, payload, code = handle_event_member(request.data['type'], request.data['event_id'], request.data['id'])
        return Response(payload, status=code)

class Event_request(APIView):
    def post(self, request):
        success, payload, code = event_request_action(request.data['id'], request.data['username'])
        return Response(payload, status=code)

                                      
class TripMembers(APIView):
    def get(self, request):
        trip_id = request.GET.get('id')
        return Response(trip_members_payload(trip_id))

class Trip_request(APIView):
    def post(self, request):
        success, payload, code = trip_request_action(request.data['id'], request.data['username'])
        return Response(payload, status=code)

class TripNotMember(APIView):
    def get(self, request):
        trip_id = request.GET.get('id')
        return Response(trip_not_member_payload(trip_id))

class HandleTripmember(APIView):
    def post(self, request):
        success, payload, code = handle_trip_member(request.data['type'], request.data['tid'], request.data['id'])
        return Response(payload, status=code)

                           
class TripUpdate(APIView):
    def post(self, request):
        success, payload, code = trip_update_action(request.data)
        return Response(payload, status=code)

                          
class MedicationBox(APIView):
    def get(self, request):
        return Response(medication_list_payload(request.GET.get('username')))

    def post(self, request):
        return Response(medication_create_action(request.data, request.FILES.get('img')), status=status.HTTP_201_CREATED)

class Done(APIView):
    def post(self, request):
        return Response(done_action(request.data), status=status.HTTP_201_CREATED)

    def get(self, request):
        return Response(done_get(request.GET.get('username'), request.GET.get('date'), request.GET.get('time')))

class MedTime(APIView):
    def get(self, request):
        return Response(medtime_get(request.GET.get('username')))

    def post(self, request):
        payload = medtime_post(request.data)
        return Response(payload, status=status.HTTP_201_CREATED)

                      
class Search(APIView):
    def get(self, request):
        return Response(search_blog_payload(request.GET.get('search'), request.GET.get('username')))

class Searchfnd(APIView):
    def get(self, request):
        success, payload, code = search_friend_payload(request.GET.get('search', ''), request.GET.get('username'))
        return Response(payload, status=code)

    def post(self, request):
                                                    
        return Response({"message": "POST method not implemented"})

                                   
class DeleteGroup(APIView):
    def post(self, request):
        return Response(delete_group_membership(request.data), status=status.HTTP_201_CREATED)

class OverseerDelete(APIView):
    def post(self, request):
        data = request.data
        name = data['username'].split('@')[0]
        top = data['username'].split('@')[1]
        overseer = Overseer.objects.filter(username__icontains="@" + top)
        if len(overseer) > 1:
            overseer = Overseer.objects.get(username=name + "@" + top)
            overseer.delete()
            return Response({"message": "Overseer deleted successfully"}, status=status.HTTP_201_CREATED)
        return Response({"message": "Overseer Cannot be Deleted!"}, status=status.HTTP_201_CREATED)

class AddHandler(APIView):
    def post(self, request):
        return Response(add_handler_action(request.data), status=status.HTTP_201_CREATED)

class PostUpdate(APIView):
    def put(self, request):
        data = request.data
        post = Blog.objects.get(blogid=data['id'])
        post.content = data['content']
        post.save()
        return Response({"message": "Post updated successfully"}, status=status.HTTP_201_CREATED)

    def post(self, request):
        data = request.data
        post = Blog.objects.get(blogid=data['id'])
        post.delete()
        return Response({"message": "Post deleted successfully"}, status=status.HTTP_201_CREATED)

class SearchFndBox(APIView):
    def get(self, request):
        return Response({"users": search_friend_box_payload(request.GET.get('search'), request.GET.get('username')), "message": "User information retrieved successfully"}, status=status.HTTP_200_OK)

class Addinfo(APIView):
    def get(self, request):
        return Response(add_info_payload(request.GET.get('user_id')))

class UpdateGroup(APIView):
    def post(self, request):
        return Response(update_group_payload({**request.data, 'img': request.FILES.get('img')}), status=status.HTTP_201_CREATED)

class FindThana(APIView):
    def get(self, request):
        return JsonResponse(find_thana_payload(request.GET.get('district')), safe=False)

class FindDistrict(APIView):
    def get(self, request):
        return JsonResponse(find_district_payload(request.GET.get('division')), safe=False)

class AllOwners(APIView):
    def get(self, request):
        owners = Owner.objects.all()
        data = [{'username': o.username, 'first_name': o.first_name, 'last_name': o.last_name} for o in owners]
        return Response(data, status=status.HTTP_200_OK)

                                          
class FriendListView(ListAPIView):
    serializer_class = FriendSerializer
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        queryset = Friend.objects.filter(user1=user) | Friend.objects.filter(user2=user)
        queryset = queryset.exclude(user1=user) | queryset.exclude(user2=user)
        return queryset

    def get(self, request, *args, **kwargs):
        page_number = request.query_params.get('page')
        if page_number:
            return self.list(request, *args, **kwargs)
        else:
            friend_id = kwargs.get('pk')
            try:
                friend = Friend.objects.get(pk=friend_id)
            except Friend.DoesNotExist:
                return Response({"error": "Friend not found"}, status=status.HTTP_404_NOT_FOUND)
            current_user = request.user
            if friend.user1 == current_user:
                friend_owner = friend.user2
            else:
                friend_owner = friend.user1
            owner_serializer = OwnerSerializer(friend_owner)
            return Response(owner_serializer.data)

                            
class OverseerList(APIView):
    def get(self, request):
        target = request.GET.get('target')
        if not target:
            return Response({"message": "Please provide a target value"}, status=status.HTTP_400_BAD_REQUEST)
        target = "@" + target
        users = Overseer.objects.filter(username__contains=target)
        serialized_data = []
        for user in users:
            img_url = user.p_image.url if user.p_image else "/media/image/download_lsX6bjA6.jpeg"
            serialized_data.append({
                'id': user.id,
                'pp': img_url,
                'p_image': img_url,
                'first_name': user.first_name,
                'username': user.username,
                'last_name': user.last_name,
                'email': user.email,
                'gender': user.gender,
                'phone': user.phone,
                'dob': user.dob,
                'address': user.address,
                'nid': user.nid,
                'relation': user.Relation,
            })
        return Response({"users": serialized_data, "message": "User information retrieved successfully"}, status=status.HTTP_200_OK)

                                                   
class FaceApiCompare(FaceApiCompareService):
    pass


face_api_compare = FaceApiCompare()

class CompareImagesView(APIView):
    def post(self, request, *args, **kwargs):
        image_file1 = request.FILES.get('image1')
        image_file2 = request.data['image2']
        payload, code = compare_uploaded_images(image_file1, image_file2)
        return JsonResponse(payload, status=code)

class CompareImages(APIView):
    def post(self, request, *args, **kwargs):
        image_file2 = request.data['image2']
        image_file1 = request.data['image1']
        if not (image_file1 and image_file2):
            return JsonResponse({'error': 'Missing image data in request'}, status=400)
                                
        return JsonResponse({'result': 'processed'})


@method_decorator(csrf_exempt, name='dispatch')
class BlogViewAPIView(APIView):
    """
    Records post view duration (dwell time) from feed or post detail view.
    """
    def post(self, request):
        data = request.data
        username = data.get('username')
        blog_id = data.get('blog_id') or data.get('id')
        view_duration = data.get('view_duration', 0.0)

        try:
            view_duration = float(view_duration)
        except (ValueError, TypeError):
            view_duration = 0.0

        if not username or not blog_id:
            return Response({"error": "username and blog_id are required"}, status=400)

        bv, blog = record_blog_view(username, blog_id, view_duration)
        if not bv or not blog:
            return Response({"error": "User or Blog not found"}, status=404)

        return Response({
            "message": "Blog view recorded successfully",
            "view_id": bv.id,
            "duration": view_duration
        }, status=status.HTTP_201_CREATED)


class BlogDetailAPIView(APIView):
    """
    Returns full post details for single-post FB-style detail modal view.
    """
    def get(self, request):
        blog_id = request.GET.get('id') or request.GET.get('blog_id')
        username = request.GET.get('username')

        if not blog_id:
            return Response({"error": "blog_id parameter is required"}, status=400)

        data = blog_detail(username, blog_id)
        if not data:
            return Response({"error": "Blog post not found"}, status=404)
        return Response(data, status=status.HTTP_200_OK)


class FriendSugg(APIView):
    def get(self, request):
        user_id = request.GET.get('user_id')
        username = request.GET.get('username')

        user = None
        if user_id:
            user = Owner.objects.filter(id=user_id).first()
        if not user and username:
            user = Owner.objects.filter(username=username).first()

        if user:
            friend_ids_1 = Friend.objects.filter(user1=user).values_list('user2_id', flat=True)
            friend_ids_2 = Friend.objects.filter(user2=user).values_list('user1_id', flat=True)
            excluded_ids = set(friend_ids_1).union(set(friend_ids_2))
            excluded_ids.add(user.id)
            suggested = Owner.objects.exclude(id__in=excluded_ids)[:10]
        else:
            suggested = Owner.objects.all()[:10]

        users_data = []
        for o in suggested:
            img_url = o.p_image.url if o.p_image else "/media/image/download_lsX6bjA6.jpeg"
            users_data.append({
                'id': o.id,
                'first_name': o.first_name,
                'last_name': o.last_name,
                'username': o.username,
                'pp': img_url,
                'p_image': img_url,
                'thana': o.thana.thana if hasattr(o, 'thana') and o.thana else ''
            })

        return Response({"users": users_data, "message": "Friend suggestions retrieved successfully"}, status=status.HTTP_200_OK)
