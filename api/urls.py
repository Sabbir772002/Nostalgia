from django.urls import path
from .views import MyModelListCreateAPIView,MyAPIView

urlpatterns = [
    path('', MyModelListCreateAPIView.as_view(), name='mymodel-list-create'),
    path('/orm', MyAPIView.as_view(), name='MyAPIView'),
]
