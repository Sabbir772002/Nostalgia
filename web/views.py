from django.shortcuts import render
import requests
from django.http import HttpResponse
from django.http import JsonResponse
from api.models import User, Owner, Thana,Overseer
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
           return render(request, 'home.html')

    return render(request, 'home.html')@csrf_exempt
def log_in(request):
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
from django.contrib.auth import logout
def logout_view(request):
    logout(request)
    return redirect('home')

@csrf_exempt
def friends(request):
    print(request.user)
    if(request.user.is_authenticated):
        print("Yeah, youa re boss at web friends page")
    else:
        print("You are not authenticated at web friends page")

    return HttpResponse("Hello, this is the friends page!")

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        walk_type = request.POST.get('walk_type',"alone")
        gender = request.POST.get('gender')
        phone = request.POST.get('phone')
        dob = request.POST.get('dob', '2022-01-01')
        address = request.POST.get('address')
        nid = request.POST.get('nid')
        thana = request.POST.get('thana')
        p_image = request.POST.get('p_image')

        url = "http://127.0.0.1:8000/api/sign" 
        data = {
            'username': username,
            'password': password,
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'walk_type': walk_type,
            'gender': gender,
            'phone': phone,
            'dob': dob,
            'address': address,
            'nid': nid,
            'thana':1,
            #'p_image': 'http://example.com/image.jpg',
        }

        response = requests.post(url, data=data)
        if response.status_code == 201:
            print("Registration successful!")
            return redirect('home')
        else:
            print("Failed to register:", response.text)
                    
        return render(request, 'signup.html')

    else:
        return render(request, 'signup.html')

def profile(request):
    profile=Owner.objects.get(username=request.user.username)
    friends=Owner.objects.all()
    return render(request, 'profile.html',{'profile':profile,'friends':friends})

from django.http import HttpResponse
from PIL import Image
import os
from django.conf import settings

def read_image(image_path):
    # Construct the full path to the image
    full_image_path = os.path.join(settings.MEDIA_ROOT, image_path)

    try:
        # Open the image using PIL
        with open(full_image_path, 'rb') as img_file:
            image_data = img_file.read()
        
        # You can do any processing with the image data here, 
        # such as resizing, cropping, etc., using PIL or any other library

        # Finally, return the image data as an HTTP response
        return HttpResponse(image_data, content_type="image/jpeg")  # Adjust content_type according to your image type
    except FileNotFoundError:
        return HttpResponse("Image not found", status=404)

def load_image_as_binary(image_path):
        try:
            with open(image_path, 'rb') as img_file:
                binary_data = img_file.read()
            return binary_data
        except FileNotFoundError:
            print("Image not found.")
            return None

def read_image_file_as_binary(image_path):
    try:
        # Open the image file
        with open(image_path, 'rb') as img_file:
            # Read the binary data from the file
            binary_data = img_file.read()
        return binary_data
    except FileNotFoundError:
        print("Image file not found.")
        return None

def read_image(image_path):
    try:
        # Open the image file
        with open(image_path, 'rb') as img_file:
            # Use Pillow to open the image
            image = Image.open(img_file)
            return image
    except FileNotFoundError:
        print("Image file not found.")
        return None

import requests

# Read image files as binary data
def read_image_file_as_binary(image_path):
    try:
        with open(image_path, 'rb') as img_file:
            binary_data = img_file.read()
        return binary_data
    except FileNotFoundError:
        print("Image file not found.")
        return None
def match(request):
    image_path1 = r"D:\DEV\Django\Nostalgia\media\bb.png"
    image_path2 = r"D:\DEV\Django\Nostalgia\media\bb.png"

    # Read the image files
    binary_image_data1 = read_image_file_as_binary(image_path1)
    binary_image_data2 = read_image_file_as_binary(image_path2)
    import imageio as iio
    import cv2
    img2 = cv2.imread(image_path2)
    img1 = cv2.imread(image_path1)
 
# read an image 
    # img = Image.open(image_path1)
    # img2=Image.open(image_path2)
    # print(img.format)
    # print(img2.format)



    # API endpoint
    url = "https://api-us.faceplusplus.com/facepp/v3/compare"

    # API Key and Secret
    api_key = "edEq6oq-Eqf3Sq4sfszoXpRQ9FHRRQGx"
    api_secret = "Ky2HfeEgU58UvJkmCt5nIe97DMEeswRy"

    # Prepare the payload
    payload = {
        "api_key": api_key,
        "api_secret": api_secret,
        # "face_token1": "50da07384227fd1480595303ac83ff29",
        # "face_token2": "6fd9b603e6cdb3920480eb8c2cbc6f05",
        "image_file1":img1,
        "image_file2":img2,
    }

    # Send the POST request
    response = requests.post(url, data=payload)

    # Print the response
    print(response.json())
    return JsonResponse(response.json())
