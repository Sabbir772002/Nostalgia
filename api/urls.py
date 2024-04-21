from django.urls import path
from .views import MyModelListCreateAPIView,MyAPIView,_sign,sign,login_api,ChangePass,show,friends,Owner_update,O_update,UserLogin
from .views import CustomTokenObtainPairView, CustomTokenRefreshView, HelloWorldView,add_fnf,Profile
from .views import CustomTokenObtainPairView, CustomTokenRefreshView, HelloWorldView
from .views import PlanEventCreateAPIView, PlanEventListAPIView, PlanEventUpdateAPIView
from . import views
from .views import CustomTokenObtainPairView, CustomTokenRefreshView, HelloWorldView,add_fnf,FriendListView, FriendList
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns=[
    path('', MyModelListCreateAPIView.as_view(), name='mymodel-list-create'),
    path('orm', MyAPIView.as_view(), name='MyAPIView'),
    path('changepass', ChangePass.as_view(), name='changepass'),
    path('login', login_api.as_view(), name='login'),
    path('log', UserLogin.as_view(), name='log'),
    path('sign', sign.as_view(), name='sign'),
    path('add_overseer', _sign.as_view(), name='add_overseer'),
    path('show', show.as_view(), name='show'),
    path('owner/<username>', Owner_update.as_view(), name='Owner_update'),
    path('overseer/<int:pk>', O_update.as_view(), name='O_update'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('hello/', HelloWorldView.as_view(), name='hello_world'),
    path('friends', views.FriendList.as_view(), name='friend-list'),
    path('overseerlist', views.OverseerList.as_view(), name='overseerlist'),
    path('friend', views.friends, name='friend'),
    path('findfriend', views.FindFriend.as_view(), name='findfriend'),
    path('add_fnf', add_fnf.as_view(), name='add_fnf'),
    path('update_fnf', views.update_fnf.as_view(), name='update_fnf'),
    path('profile/<username>', Profile.as_view(), name='profile'),
    path('otp', views.OTPAPI.as_view(), name='otp'),
    path('resetpass', views.PassReset.as_view(), name='resetpass'),
    path('blog', views.BlogListView.as_view(), name='blog'),
    path('singleblog', views.BlogSingleView.as_view(), name='singleblog'),
    path('addblog', views.BlogCreateView.as_view(), name='addblog'),
    path('add_group', views.Add_group.as_view(), name='add_group'),
    path('my_groups', views.My_Group.as_view(), name='my_groups'),
    path('g_profile/<username>', views.GroupProfile.as_view(), name='g_profile'),
    path('gp_post', views.GP_post.as_view(), name='GP_post'),
    path('gt_post', views.GT_post.as_view(), name='GT_post'),
    path('api/events/create/', PlanEventCreateAPIView.as_view(), name='event-create'),
    path('api/events/list/', PlanEventListAPIView.as_view(), name='event-list'),
    path('api/events/update/<int:pk>/', PlanEventUpdateAPIView.as_view(), name='event-update'),
    path('compare', views.CompareImagesView.as_view(), name='compare_images'),
    path('upvote', views.UpvoteAPIView.as_view(), name='upvote'),
    path('walk', views.WalkListView.as_view(), name='walk'),
    path('walkmembers', views.WalkMembers.as_view(), name='walk_members'),
    path('delete_fnd', views.Delete_fnd.as_view(), name='delete_fnd'),
    path('notification', views.NotificationView.as_view(), name='notification'),
    path('comments', views.BlogCommentsView.as_view(), name='comments'),
    path('comment', views.CommentCreateView.as_view(), name='newcomment'),
    path('htimeline', views.HTimeline.as_view(), name='htimeline'),
    path('walk_request', views.Walk_request.as_view(), name='walk_request'),
    path('walk!members', views.WalkNotMember.as_view(), name='walk!members'),
    path('handlemember', views.Handlemember.as_view(), name='Handlemember'),
    path('join_group', views.JoinGroup.as_view(), name='join_group'),
    path('addgroupost', views.AddGroupPost.as_view(), name='addgroupost'),
    path('groupmembers', views.GroupMembers.as_view(), name='groupmembers'),
    path('requestmembers',views.RequestMembers.as_view(), name='requestmembers'),
    path('grouprequest',views.GroupRequest.as_view(), name='grouprequest'),
    path('friendsugg',views.FriendSugg.as_view(), name='friendsugg'),
    path('caregiver',views.CareGiver.as_view(), name='caregiver'),
    # path('nidtext',views.NIDText.as_view(), name='nidtext'),
    # path('nidimg',views.NIDImage.as_view(), name='nidimg'),
    # path('dnid',views.DecodeImageView.as_view(), name='dnid'),
    #work doneZZ
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)