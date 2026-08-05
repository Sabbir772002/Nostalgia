                                  
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('friends', views.friends, name='friends'),
    path('signup', views.signup, name='signup'),
    path('logout', views.logout_view, name='logout'),
    path('login', views.log_in, name='log_in'),
    path('profile', views.profile, name='profile'),
    path('100', views.match, name='match'),
    path('add_friend/<int:id>', views.add_friend, name='add_friend'),
    path('upload', views.upload_image, name='upload_image'),
    path('wbuddy', views.wbuddy, name='wbuddy'),

]
