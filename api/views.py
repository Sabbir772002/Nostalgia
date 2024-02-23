# views.py
from rest_framework import views, status
from rest_framework.response import Response
from .models import MyModel
from .serializers import MyModelSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .serializers import UserSerializer  # Assuming you have a serializer for the User model

class Sign_Api(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            print("done")
            return Response({"message": "User created successfully", "user_id": user.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class MyAPIView(views.APIView):
    def get(self, request):
        # Extract query parameters from the request
        name = request.GET.get('name')
        #age = request.GET.get('age')

        # Initialize queryset
        queryset = MyModel.objects.all()
        print(name)

        # Apply filters based on query parameters
        if name:
            queryset = queryset.filter(name=name)
        #if age:
        #    queryset = queryset.filter(age=age)

        # Convert queryset to a list of dictionaries
        data = list(queryset.values())

        # Return the filtered data as JSON response
        serializer = MyModelSerializer(queryset, many=True)
        return Response(serializer.data)


class MyModelListCreateAPIView(views.APIView):
    def get(self, request):
        queryset = MyModel.objects.all()
        serializer = MyModelSerializer(queryset, many=True)
        return Response(serializer.data)
        
    def post(self, request):
        serializer = MyModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
