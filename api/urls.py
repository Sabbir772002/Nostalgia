from django.urls import path
from .views import MyModelListCreateAPIView,MyAPIView,_sign,sign,login_api,ChangePasswordAPIView,show,friends,Owner_update,O_update,UserLogin

urlpatterns = [
    path('', MyModelListCreateAPIView.as_view(), name='mymodel-list-create'),
    path('/orm', MyAPIView.as_view(), name='MyAPIView'),
    path('/changepassword', ChangePasswordAPIView.as_view(), name='changepassword'),
    path('/login', login_api.as_view(), name='login'),
    path('/log', UserLogin.as_view(), name='log'),
    path('/sign', sign.as_view(), name='sign'),
    path('/_sign', _sign.as_view(), name='sign_o'),
    path('/show', show.as_view(), name='show'),
    path('/owner/<int:pk>', Owner_update.as_view(), name='Owner_update'),
    path('/overseer/<int:pk>', O_update.as_view(), name='O_update'),
]
