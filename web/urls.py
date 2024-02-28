#cratwe basic urls for the web app
from django.urls import path
from . import views 
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.conf.urls.static import static
from .views import signup, logout_view,log_in,profile

urlpatterns = [
    path('', views.home, name='home'),
    path('friends', views.friends, name='friends'),
    path('signup', views.signup, name='signup'),
    path('logout', views.logout_view, name='logout'),
    path('login', views.log_in, name='log_in'),
    path('profile', views.profile, name='profile'),
    path('login', views.log_in, name='log_in'),
]
