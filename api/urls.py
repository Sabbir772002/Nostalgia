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


urlpatterns = [
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
    path('compare', views.CompareImagesView.as_view(), name='compare_images'),
    path('walkmember', views.WalkMemberView.as_view(), name='walkmember'),

]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
