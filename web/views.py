from django.shortcuts import render
import requests
from django.http import HttpResponse
from django.http import JsonResponse
from api.models import User
from django.contrib.auth import authenticate, login as a_login
import json
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def home(request):
    if request.method == 'POST':
        # Access form field values from request.POST
        username = request.POST.get('username')
        password = request.POST.get('password')
        # data = json.loads(request.body)
        # username = data.get('username')
        # password = data.get('password')

        remember_me = request.POST.get('remember_me')  # Assuming you have a checkbox with the name 'remember_me'
        # Do something with the form data (e.g., validate, authenticate user)
        # Example: Authenticate user using Django's built-in authentication system
        #print(username, password)
        user = authenticate(request, username=username, password=password)
        print(user)

        if user is not None:
            a_login(request, user)  # Assuming you have imported the login function
            if request.user.is_authenticated:
                print("User is authenticatedd at web")  # This line will be executed if the user is authenticated
            else:
                print("User is not authenticated at web")

            return render(request, 'home.html')
        else:
            # User authentication failed
            return HttpResponse("mile nai vai tomar username or password")  # Example response
    else:  
           return render(request, 'login.html')

    return render(request, 'login.html')


@csrf_exempt
def friends(request):
    print(request.user)
    if(request.user.is_authenticated):
        print("Yeah, youa re boss at web friends page")
    else:
        print("You are not authenticated at web friends page")

    return HttpResponse("Hello, this is the friends page!")