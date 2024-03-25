from django.urls import path
from .views import MyModelListCreateAPIView,MyAPIView,_sign,sign,login_api,ChangePass,show,friends,Owner_update,O_update,UserLogin
from .views import CustomTokenObtainPairView, CustomTokenRefreshView, HelloWorldView
from . import views

urlpatterns = [
    path('', MyModelListCreateAPIView.as_view(), name='mymodel-list-create'),
    path('/orm', MyAPIView.as_view(), name='MyAPIView'),
    path('/changepass', ChangePass.as_view(), name='changepass'),
    path('/login', login_api.as_view(), name='login'),
    path('/log', UserLogin.as_view(), name='log'),
    path('/sign', sign.as_view(), name='sign'),
    path('/_sign', _sign.as_view(), name='sign_o'),
    path('/show', show.as_view(), name='show'),
    path('/owner/<int:pk>', Owner_update.as_view(), name='Owner_update'),
    path('/overseer/<int:pk>', O_update.as_view(), name='O_update'),
    path('/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('/hello/', HelloWorldView.as_view(), name='hello_world'),
    path('/friends/', views.FriendListView.as_view(), name='friend-list'),

]