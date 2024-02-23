from django.urls import path
from .views import MyModelListCreateAPIView,MyAPIView,Sign_Api

urlpatterns = [
    path('', MyModelListCreateAPIView.as_view(), name='mymodel-list-create'),
    path('/orm', MyAPIView.as_view(), name='MyAPIView'),
    path('/login', MyAPIView.as_view(), name='login'),
    path('/sign', Sign_Api.as_view(), name='sign'),
]
