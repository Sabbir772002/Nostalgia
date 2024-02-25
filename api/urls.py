from django.urls import path
from .views import MyModelListCreateAPIView,MyAPIView,_sign,sign,login_api,ChangePasswordAPIView,show,friends

urlpatterns = [
    path('', MyModelListCreateAPIView.as_view(), name='mymodel-list-create'),
    path('/orm', MyAPIView.as_view(), name='MyAPIView'),
    path('/changepassword', ChangePasswordAPIView.as_view(), name='changepassword'),
    path('/login', login_api.as_view(), name='login'),
    path('/sign', sign.as_view(), name='sign'),
    path('/_sign', _sign.as_view(), name='_sign'),
    path('/show', show.as_view(), name='show'),
    #path('/friends', friends, name='friends'),
]
