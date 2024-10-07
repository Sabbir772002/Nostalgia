from django.shortcuts import render
import requests
from django.http import HttpResponse
from django.http import JsonResponse
from api.models import User, Owner, Thana,Overseer,Friend
from django.contrib.auth import authenticate, login as a_login
import json
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage, get_connection

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
            print("that not the case")
            return redirect('home')
        else:
            print("Failed to register:", response.text)
                    
        return render(request, 'signup.html')
    else:
        return render(request, 'signup.html')
    
def profile(request):
    user=Owner.objects.get(username=request.user.username)
    friends=Owner.objects.all()
    return render(request, 'profile.html',{"profile":user,"friends":friends})    

def add_friend(request,id):
    url="http://127.0.0.1:8000/api/add_fnf"
    data={
        "user_id":request.user.id,
        "friend_id":id    
    }
    response = requests.post(url, data=data)
    #fnd should be a list of friends from api, make it later...
    fnd=Friend.objects.filter(user1=id,is_fnf=1)
    friends=Owner.objects.exclude(id__in=fnd)
    print(response.json())

    return render(request, 'profile.html',{"profile":Owner.objects.get(id=id),"friends":friends})

import os
from django.conf import settings

def match(request):
    api_key = "edEq6oq-Eqf3Sq4sfszoXpRQ9FHRRQGx"
    api_secret = "Ky2HfeEgU58UvJkmCt5nIe97DMEeswRy"

    image_path1 = r"5.png"
    image_path2 = r"bb.png"

#     # Read the image files
#     binary_image_data1 = read_image_file_as_binary(image_path1)
#     binary_image_data2 = read_image_file_as_binary(image_path2)
#     import imageio as iio
#     import cv2
#     img2 = cv2.imread(image_path2)
#     img1 = cv2.imread(image_path1)
 
# # read an image 
#     # img = Image.open(image_path1)
#     # img2=Image.open(image_path2)
#     # print(img.format)
#     # print(img2.format)

    # API endpoint
    url = "https://api-us.faceplusplus.com/facepp/v3/compare"

    # API Key and Secret

    full_path = os.path.join(settings.MEDIA_ROOT, image_path1)
    full_path2 = os.path.join(settings.MEDIA_ROOT, image_path2)
    import base64

    with open(full_path, 'rb') as img_file:
        image_content = img_file.read()
        base64_image = base64.b64encode(image_content).decode('utf-8')

    with open(full_path2, 'rb') as img_file2:
        image_content2 = img_file2.read()
        base64_image2 = base64.b64encode(image_content2).decode('utf-8')

    # Prepare the payload
    payload = {
        "api_key": api_key,
        "api_secret": api_secret,
        # "face_token1": "50da07384227fd1480595303ac83ff29",
        # "face_token2": "6fd9b603e6cdb3920480eb8c2cbc6f05",
        "image_base64_1":base64_image,
        "image_base64_2":base64_image2,
    }
    # Send the POST request
    response = requests.post(url, data=payload)

    # Print the response
    print(response.json())
    return JsonResponse(response.json())

def upload_image(request):
    api_key = "edEq6oq-Eqf3Sq4sfszoXpRQ9FHRRQGx"
    api_secret = "Ky2HfeEgU58UvJkmCt5nIe97DMEeswRy"
    url = "https://api-us.faceplusplus.com/facepp/v3/compare"

    if request.method == 'POST':
        image_path1 = request.FILES.get('image')
        image_path2 = request.FILES.get('image2')
        #print(image_path1, image_path2)
        if image_path1 and image_path2:
                # image_type1 = imghdr.what(None, image_path1.read())
                # image_type2 = imghdr.what(None, image_path2.read())

                # if image_type1:
                #     print("File 1 is an image of type:", image_type1)
                # else:
                #     print("File 1 is not an image.")
                # if image_type2:
                #     print("File 2 is an image of type:", image_type2)
                # else:
                #   print("File 2 is not an image.")
              
                image_path10 = r"5.png"
                image_path20 = r"bb.png"
                full_path = os.path.join(settings.MEDIA_ROOT, image_path10)
                full_path2 = os.path.join(settings.MEDIA_ROOT, image_path20)
                print(full_path)
                print(full_path2)
                import base64
                file_contents = image_path1.read()
                file_content = image_path2.read()

                # Now you can use 'file_contents' as a bytes-like object
                # For example, if you want to write it to a file:
                with open(full_path, 'wb') as f:
                    f.write(file_contents)
                with open(full_path2, 'wb') as f:
                    f.write(file_content)
                with open(full_path, 'rb') as img_file:
                    image_content = img_file.read()
                    base64_image = base64.b64encode(image_content).decode('utf-8')

                with open(full_path2, 'rb') as img_file2:
                    image_content2 = img_file2.read()
                    base64_image2 = base64.b64encode(image_content2).decode('utf-8')

                # Prepare the payload
                payload = {
                    "api_key": api_key,
                    "api_secret": api_secret,
                    # "image_file1": image_path1,
                    # "image_file2": image_path2,
                    # "face_token1": "50da07384227fd1480595303ac83ff29",
                    # "face_token2": "6fd9b603e6cdb3920480eb8c2cbc6f05",
                    "image_base64_1":base64_image,
                    "image_base64_2":base64_image2,

                }
                # Send the POST request
                response = requests.post(url, data=payload)
                print(response.json())

                # Print the response
                #print(response.json())
                response=response.json()
                confidence = response['confidence']
                threshold = 50

                if confidence >= threshold:
                        http_response = "<b>Match between two photos is successful with confidence: {:.2f}</b>".format(confidence)
                else:
                    http_response = "<b>Match between two photos is not successful. Confidence is too low: {:.2f}</b>".format(confidence)
                    print(http_response)

                return HttpResponse(http_response)
    return render(request, 'home.html')
from django.db.models import Q
from django.core.paginator import Paginator 
def wbuddy(request):
    fnd = Friend.objects.filter(Q(user1=request.user.id) | Q(user2=request.user.id))#, is_fnf=1)
    friends=Owner.objects.filter(id__in=fnd)
    # for expert in experts_users:
    #     expert.save()
    # for expert in friends:
    #         print(expert.first_name)
    print(friends)

    paginator = Paginator(friends,1)
    page = request.GET.get('page', 1)
    page = int(page)
    context = {
        'paginator': paginator,
        'page_obj': paginator.get_page(page),
        'page_numbers_range': range(
            max(1, page - 2), min(paginator.num_pages, page + 2) + 1
        ),
    }
    data = paginator.get_page(page)
    return render(request, "wbuddyList.html", {'context': context})

def send_email(request):
 if request.method == "POST":
    with get_connection(
        host=settings.EMAIL_HOST,
        port=settings.EMAIL_PORT,
        username=settings.EMAIL_HOST_USER,
        password=settings.EMAIL_HOST_PASSWORD,
        use_tls=settings.EMAIL_USE_TLS
    ) as connection:
        subject = "From Nostalgia"  
        request.POST.get("subject")
        email_from = settings.EMAIL_HOST_USER
        [request.POST.get("email"), ]
        mail = "sabbir772002@gmail.com"
        recipient_list = [mail,"nhossain213005@bscse.uiu.ac.bd"]
        message = request.POST.get("message")
        context = {
            "user": request.user
        }
        html_message = render_to_string('mail.html', {
            'context': context})
        mail = EmailMessage(subject, html_message, email_from,
                            recipient_list, connection=connection)
        image_path = os.path.join(settings.MEDIA_ROOT, request.user.image.path)

        # with open(image_path, 'rb') as image_file:
        #                       mail.attach_file(image_path)
        
        # image_content_id = mail.attachments[0][0]
        # image_reference = f'cid:{image_content_id}'
        # print(image_reference)

        # html_content_with_cid = html_message.replace(
        #     request.user.image.url, image_reference)

        #mail.body = html_content_with_cid
        mail.content_subtype = 'html'
        mail.send()

        # html_message = "<p>Hey how are you?</p>"

        # msg.content_subtype = "html"
        # msg.send()
        # EmailMessage(subject, message, email_from,
        #  recipient_list, connection=connection).send()

        return render(request, 'index.html')


from django.shortcuts import render
import requests
from django.http import HttpResponse
from django.http import JsonResponse
from api.models import User, Owner, Thana,Overseer,Friend
from django.contrib.auth import authenticate, login as a_login
import json
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage, get_connection

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
            print("that not the case")
            return redirect('home')
        else:
            print("Failed to register:", response.text)
                    
        return render(request, 'signup.html')
    else:
        return render(request, 'signup.html')
    
def profile(request):
    user=Owner.objects.get(username=request.user.username)
    friends=Owner.objects.all()
    return render(request, 'profile.html',{"profile":user,"friends":friends})    

def add_friend(request,id):
    url="http://127.0.0.1:8000/api/add_fnf"
    data={
        "user_id":request.user.id,
        "friend_id":id    
    }
    response = requests.post(url, data=data)
    #fnd should be a list of friends from api, make it later...
    fnd=Friend.objects.filter(user1=id,is_fnf=1)
    friends=Owner.objects.exclude(id__in=fnd)
    print(response.json())

    return render(request, 'profile.html',{"profile":Owner.objects.get(id=id),"friends":friends})

import os
from django.conf import settings

def match(request):
    api_key = "edEq6oq-Eqf3Sq4sfszoXpRQ9FHRRQGx"
    api_secret = "Ky2HfeEgU58UvJkmCt5nIe97DMEeswRy"

    image_path1 = r"5.png"
    image_path2 = r"bb.png"

#     # Read the image files
#     binary_image_data1 = read_image_file_as_binary(image_path1)
#     binary_image_data2 = read_image_file_as_binary(image_path2)
#     import imageio as iio
#     import cv2
#     img2 = cv2.imread(image_path2)
#     img1 = cv2.imread(image_path1)
 
# # read an image 
#     # img = Image.open(image_path1)
#     # img2=Image.open(image_path2)
#     # print(img.format)
#     # print(img2.format)

    # API endpoint
    url = "https://api-us.faceplusplus.com/facepp/v3/compare"

    # API Key and Secret

    full_path = os.path.join(settings.MEDIA_ROOT, image_path1)
    full_path2 = os.path.join(settings.MEDIA_ROOT, image_path2)
    import base64

    with open(full_path, 'rb') as img_file:
        image_content = img_file.read()
        base64_image = base64.b64encode(image_content).decode('utf-8')

    with open(full_path2, 'rb') as img_file2:
        image_content2 = img_file2.read()
        base64_image2 = base64.b64encode(image_content2).decode('utf-8')

    # Prepare the payload
    payload = {
        "api_key": api_key,
        "api_secret": api_secret,
        # "face_token1": "50da07384227fd1480595303ac83ff29",
        # "face_token2": "6fd9b603e6cdb3920480eb8c2cbc6f05",
        "image_base64_1":base64_image,
        "image_base64_2":base64_image2,
    }
    # Send the POST request
    response = requests.post(url, data=payload)

    # Print the response
    print(response.json())
    return JsonResponse(response.json())

def upload_image(request):
    api_key = "edEq6oq-Eqf3Sq4sfszoXpRQ9FHRRQGx"
    api_secret = "Ky2HfeEgU58UvJkmCt5nIe97DMEeswRy"
    url = "https://api-us.faceplusplus.com/facepp/v3/compare"

    if request.method == 'POST':
        image_path1 = request.FILES.get('image')
        image_path2 = request.FILES.get('image2')
        #print(image_path1, image_path2)
        if image_path1 and image_path2:
                # image_type1 = imghdr.what(None, image_path1.read())
                # image_type2 = imghdr.what(None, image_path2.read())

                # if image_type1:
                #     print("File 1 is an image of type:", image_type1)
                # else:
                #     print("File 1 is not an image.")
                # if image_type2:
                #     print("File 2 is an image of type:", image_type2)
                # else:
                #   print("File 2 is not an image.")
              
                image_path10 = r"5.png"
                image_path20 = r"bb.png"
                full_path = os.path.join(settings.MEDIA_ROOT, image_path10)
                full_path2 = os.path.join(settings.MEDIA_ROOT, image_path20)
                print(full_path)
                print(full_path2)
                import base64
                file_contents = image_path1.read()
                file_content = image_path2.read()

                # Now you can use 'file_contents' as a bytes-like object
                # For example, if you want to write it to a file:
                with open(full_path, 'wb') as f:
                    f.write(file_contents)
                with open(full_path2, 'wb') as f:
                    f.write(file_content)
                with open(full_path, 'rb') as img_file:
                    image_content = img_file.read()
                    base64_image = base64.b64encode(image_content).decode('utf-8')

                with open(full_path2, 'rb') as img_file2:
                    image_content2 = img_file2.read()
                    base64_image2 = base64.b64encode(image_content2).decode('utf-8')

                # Prepare the payload
                payload = {
                    "api_key": api_key,
                    "api_secret": api_secret,
                    # "image_file1": image_path1,
                    # "image_file2": image_path2,
                    # "face_token1": "50da07384227fd1480595303ac83ff29",
                    # "face_token2": "6fd9b603e6cdb3920480eb8c2cbc6f05",
                    "image_base64_1":base64_image,
                    "image_base64_2":base64_image2,

                }
                # Send the POST request
                response = requests.post(url, data=payload)
                print(response.json())

                # Print the response
                #print(response.json())
                response=response.json()
                confidence = response['confidence']
                threshold = 50

                if confidence >= threshold:
                        http_response = "<b>Match between two photos is successful with confidence: {:.2f}</b>".format(confidence)
                else:
                    http_response = "<b>Match between two photos is not successful. Confidence is too low: {:.2f}</b>".format(confidence)
                    print(http_response)

                return HttpResponse(http_response)
    return render(request, 'home.html')
from django.db.models import Q
from django.core.paginator import Paginator 
def wbuddy(request):
    fnd = Friend.objects.filter(Q(user1=request.user.id) | Q(user2=request.user.id))#, is_fnf=1)
    friends=Owner.objects.filter(id__in=fnd)
    # for expert in experts_users:
    #     expert.save()
    # for expert in friends:
    #         print(expert.first_name)
    print(friends)

    paginator = Paginator(friends,1)
    page = request.GET.get('page', 1)
    page = int(page)
    context = {
        'paginator': paginator,
        'page_obj': paginator.get_page(page),
        'page_numbers_range': range(
            max(1, page - 2), min(paginator.num_pages, page + 2) + 1
        ),
    }
    data = paginator.get_page(page)
    return render(request, "wbuddyList.html", {'context': context})

def send_email(request):
 if request.method == "POST":
    with get_connection(
        host=settings.EMAIL_HOST,
        port=settings.EMAIL_PORT,
        username=settings.EMAIL_HOST_USER,
        password=settings.EMAIL_HOST_PASSWORD,
        use_tls=settings.EMAIL_USE_TLS
    ) as connection:
        subject = "From Nostalgia"  
        request.POST.get("subject")
        email_from = settings.EMAIL_HOST_USER
        [request.POST.get("email"), ]
        mail = "sabbir772002@gmail.com"
        recipient_list = [mail,"nhossain213005@bscse.uiu.ac.bd"]
        message = request.POST.get("message")
        context = {
            "user": request.user
        }
        html_message = render_to_string('mail.html', {
            'context': context})
        mail = EmailMessage(subject, html_message, email_from,
                            recipient_list, connection=connection)
        image_path = os.path.join(settings.MEDIA_ROOT, request.user.image.path)

        # with open(image_path, 'rb') as image_file:
        #                       mail.attach_file(image_path)
        
        # image_content_id = mail.attachments[0][0]
        # image_reference = f'cid:{image_content_id}'
        # print(image_reference)

        # html_content_with_cid = html_message.replace(
        #     request.user.image.url, image_reference)

        #mail.body = html_content_with_cid
        mail.content_subtype = 'html'
        mail.send()

        # html_message = "<p>Hey how are you?</p>"

        # msg.content_subtype = "html"
        # msg.send()
        # EmailMessage(subject, message, email_from,
        #  recipient_list, connection=connection).send()

        return render(request, 'index.html')


from django.shortcuts import render
import requests
from django.http import HttpResponse
from django.http import JsonResponse
from api.models import User, Owner, Thana,Overseer,Friend
from django.contrib.auth import authenticate, login as a_login
import json
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage, get_connection

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
            print("that not the case")
            return redirect('home')
        else:
            print("Failed to register:", response.text)
                    
        return render(request, 'signup.html')
    else:
        return render(request, 'signup.html')
    
def profile(request):
    user=Owner.objects.get(username=request.user.username)
    friends=Owner.objects.all()
    return render(request, 'profile.html',{"profile":user,"friends":friends})    

def add_friend(request,id):
    url="http://127.0.0.1:8000/api/add_fnf"
    data={
        "user_id":request.user.id,
        "friend_id":id    
    }
    response = requests.post(url, data=data)
    #fnd should be a list of friends from api, make it later...
    fnd=Friend.objects.filter(user1=id,is_fnf=1)
    friends=Owner.objects.exclude(id__in=fnd)
    print(response.json())

    return render(request, 'profile.html',{"profile":Owner.objects.get(id=id),"friends":friends})

import os
from django.conf import settings

def match(request):
    api_key = "edEq6oq-Eqf3Sq4sfszoXpRQ9FHRRQGx"
    api_secret = "Ky2HfeEgU58UvJkmCt5nIe97DMEeswRy"

    image_path1 = r"5.png"
    image_path2 = r"bb.png"

#     # Read the image files
#     binary_image_data1 = read_image_file_as_binary(image_path1)
#     binary_image_data2 = read_image_file_as_binary(image_path2)
#     import imageio as iio
#     import cv2
#     img2 = cv2.imread(image_path2)
#     img1 = cv2.imread(image_path1)
 
# # read an image 
#     # img = Image.open(image_path1)
#     # img2=Image.open(image_path2)
#     # print(img.format)
#     # print(img2.format)

    # API endpoint
    url = "https://api-us.faceplusplus.com/facepp/v3/compare"

    # API Key and Secret

    full_path = os.path.join(settings.MEDIA_ROOT, image_path1)
    full_path2 = os.path.join(settings.MEDIA_ROOT, image_path2)
    import base64

    with open(full_path, 'rb') as img_file:
        image_content = img_file.read()
        base64_image = base64.b64encode(image_content).decode('utf-8')

    with open(full_path2, 'rb') as img_file2:
        image_content2 = img_file2.read()
        base64_image2 = base64.b64encode(image_content2).decode('utf-8')

    # Prepare the payload
    payload = {
        "api_key": api_key,
        "api_secret": api_secret,
        # "face_token1": "50da07384227fd1480595303ac83ff29",
        # "face_token2": "6fd9b603e6cdb3920480eb8c2cbc6f05",
        "image_base64_1":base64_image,
        "image_base64_2":base64_image2,
    }
    # Send the POST request
    response = requests.post(url, data=payload)

    # Print the response
    print(response.json())
    return JsonResponse(response.json())

def upload_image(request):
    api_key = "edEq6oq-Eqf3Sq4sfszoXpRQ9FHRRQGx"
    api_secret = "Ky2HfeEgU58UvJkmCt5nIe97DMEeswRy"
    url = "https://api-us.faceplusplus.com/facepp/v3/compare"

    if request.method == 'POST':
        image_path1 = request.FILES.get('image')
        image_path2 = request.FILES.get('image2')
        #print(image_path1, image_path2)
        if image_path1 and image_path2:
                # image_type1 = imghdr.what(None, image_path1.read())
                # image_type2 = imghdr.what(None, image_path2.read())

                # if image_type1:
                #     print("File 1 is an image of type:", image_type1)
                # else:
                #     print("File 1 is not an image.")
                # if image_type2:
                #     print("File 2 is an image of type:", image_type2)
                # else:
                #   print("File 2 is not an image.")
              
                image_path10 = r"5.png"
                image_path20 = r"bb.png"
                full_path = os.path.join(settings.MEDIA_ROOT, image_path10)
                full_path2 = os.path.join(settings.MEDIA_ROOT, image_path20)
                print(full_path)
                print(full_path2)
                import base64
                file_contents = image_path1.read()
                file_content = image_path2.read()

                # Now you can use 'file_contents' as a bytes-like object
                # For example, if you want to write it to a file:
                with open(full_path, 'wb') as f:
                    f.write(file_contents)
                with open(full_path2, 'wb') as f:
                    f.write(file_content)
                with open(full_path, 'rb') as img_file:
                    image_content = img_file.read()
                    base64_image = base64.b64encode(image_content).decode('utf-8')

                with open(full_path2, 'rb') as img_file2:
                    image_content2 = img_file2.read()
                    base64_image2 = base64.b64encode(image_content2).decode('utf-8')

                # Prepare the payload
                payload = {
                    "api_key": api_key,
                    "api_secret": api_secret,
                    # "image_file1": image_path1,
                    # "image_file2": image_path2,
                    # "face_token1": "50da07384227fd1480595303ac83ff29",
                    # "face_token2": "6fd9b603e6cdb3920480eb8c2cbc6f05",
                    "image_base64_1":base64_image,
                    "image_base64_2":base64_image2,

                }
                # Send the POST request
                response = requests.post(url, data=payload)
                print(response.json())

                # Print the response
                #print(response.json())
                response=response.json()
                confidence = response['confidence']
                threshold = 50

                if confidence >= threshold:
                        http_response = "<b>Match between two photos is successful with confidence: {:.2f}</b>".format(confidence)
                else:
                    http_response = "<b>Match between two photos is not successful. Confidence is too low: {:.2f}</b>".format(confidence)
                    print(http_response)

                return HttpResponse(http_response)
    return render(request, 'home.html')
from django.db.models import Q
from django.core.paginator import Paginator 
def wbuddy(request):
    fnd = Friend.objects.filter(Q(user1=request.user.id) | Q(user2=request.user.id))#, is_fnf=1)
    friends=Owner.objects.filter(id__in=fnd)
    # for expert in experts_users:
    #     expert.save()
    # for expert in friends:
    #         print(expert.first_name)
    print(friends)

    paginator = Paginator(friends,1)
    page = request.GET.get('page', 1)
    page = int(page)
    context = {
        'paginator': paginator,
        'page_obj': paginator.get_page(page),
        'page_numbers_range': range(
            max(1, page - 2), min(paginator.num_pages, page + 2) + 1
        ),
    }
    data = paginator.get_page(page)
    return render(request, "wbuddyList.html", {'context': context})

def send_email(request):
 if request.method == "POST":
    with get_connection(
        host=settings.EMAIL_HOST,
        port=settings.EMAIL_PORT,
        username=settings.EMAIL_HOST_USER,
        password=settings.EMAIL_HOST_PASSWORD,
        use_tls=settings.EMAIL_USE_TLS
    ) as connection:
        subject = "From Nostalgia"  
        request.POST.get("subject")
        email_from = settings.EMAIL_HOST_USER
        [request.POST.get("email"), ]
        mail = "sabbir772002@gmail.com"
        recipient_list = [mail,"nhossain213005@bscse.uiu.ac.bd"]
        message = request.POST.get("message")
        context = {
            "user": request.user
        }
        html_message = render_to_string('mail.html', {
            'context': context})
        mail = EmailMessage(subject, html_message, email_from,
                            recipient_list, connection=connection)
        image_path = os.path.join(settings.MEDIA_ROOT, request.user.image.path)

        # with open(image_path, 'rb') as image_file:
        #                       mail.attach_file(image_path)
        
        # image_content_id = mail.attachments[0][0]
        # image_reference = f'cid:{image_content_id}'
        # print(image_reference)

        # html_content_with_cid = html_message.replace(
        #     request.user.image.url, image_reference)

        #mail.body = html_content_with_cid
        mail.content_subtype = 'html'
        mail.send()

        # html_message = "<p>Hey how are you?</p>"

        # msg.content_subtype = "html"
        # msg.send()
        # EmailMessage(subject, message, email_from,
        #  recipient_list, connection=connection).send()

        return render(request, 'index.html')


from django.shortcuts import render
import requests
from django.http import HttpResponse
from django.http import JsonResponse
from api.models import User, Owner, Thana,Overseer,Friend
from django.contrib.auth import authenticate, login as a_login
import json
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage, get_connection

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
            print("that not the case")
            return redirect('home')
        else:
            print("Failed to register:", response.text)
                    
        return render(request, 'signup.html')
    else:
        return render(request, 'signup.html')
    
def profile(request):
    user=Owner.objects.get(username=request.user.username)
    friends=Owner.objects.all()
    return render(request, 'profile.html',{"profile":user,"friends":friends})    

def add_friend(request,id):
    url="http://127.0.0.1:8000/api/add_fnf"
    data={
        "user_id":request.user.id,
        "friend_id":id    
    }
    response = requests.post(url, data=data)
    #fnd should be a list of friends from api, make it later...
    fnd=Friend.objects.filter(user1=id,is_fnf=1)
    friends=Owner.objects.exclude(id__in=fnd)
    print(response.json())

    return render(request, 'profile.html',{"profile":Owner.objects.get(id=id),"friends":friends})

import os
from django.conf import settings

def match(request):
    api_key = "edEq6oq-Eqf3Sq4sfszoXpRQ9FHRRQGx"
    api_secret = "Ky2HfeEgU58UvJkmCt5nIe97DMEeswRy"

    image_path1 = r"5.png"
    image_path2 = r"bb.png"

#     # Read the image files
#     binary_image_data1 = read_image_file_as_binary(image_path1)
#     binary_image_data2 = read_image_file_as_binary(image_path2)
#     import imageio as iio
#     import cv2
#     img2 = cv2.imread(image_path2)
#     img1 = cv2.imread(image_path1)
 
# # read an image 
#     # img = Image.open(image_path1)
#     # img2=Image.open(image_path2)
#     # print(img.format)
#     # print(img2.format)

    # API endpoint
    url = "https://api-us.faceplusplus.com/facepp/v3/compare"

    # API Key and Secret

    full_path = os.path.join(settings.MEDIA_ROOT, image_path1)
    full_path2 = os.path.join(settings.MEDIA_ROOT, image_path2)
    import base64

    with open(full_path, 'rb') as img_file:
        image_content = img_file.read()
        base64_image = base64.b64encode(image_content).decode('utf-8')

    with open(full_path2, 'rb') as img_file2:
        image_content2 = img_file2.read()
        base64_image2 = base64.b64encode(image_content2).decode('utf-8')

    # Prepare the payload
    payload = {
        "api_key": api_key,
        "api_secret": api_secret,
        # "face_token1": "50da07384227fd1480595303ac83ff29",
        # "face_token2": "6fd9b603e6cdb3920480eb8c2cbc6f05",
        "image_base64_1":base64_image,
        "image_base64_2":base64_image2,
    }
    # Send the POST request
    response = requests.post(url, data=payload)

    # Print the response
    print(response.json())
    return JsonResponse(response.json())

def upload_image(request):
    api_key = "edEq6oq-Eqf3Sq4sfszoXpRQ9FHRRQGx"
    api_secret = "Ky2HfeEgU58UvJkmCt5nIe97DMEeswRy"
    url = "https://api-us.faceplusplus.com/facepp/v3/compare"

    if request.method == 'POST':
        image_path1 = request.FILES.get('image')
        image_path2 = request.FILES.get('image2')
        #print(image_path1, image_path2)
        if image_path1 and image_path2:
                # image_type1 = imghdr.what(None, image_path1.read())
                # image_type2 = imghdr.what(None, image_path2.read())

                # if image_type1:
                #     print("File 1 is an image of type:", image_type1)
                # else:
                #     print("File 1 is not an image.")
                # if image_type2:
                #     print("File 2 is an image of type:", image_type2)
                # else:
                #   print("File 2 is not an image.")
              
                image_path10 = r"5.png"
                image_path20 = r"bb.png"
                full_path = os.path.join(settings.MEDIA_ROOT, image_path10)
                full_path2 = os.path.join(settings.MEDIA_ROOT, image_path20)
                print(full_path)
                print(full_path2)
                import base64
                file_contents = image_path1.read()
                file_content = image_path2.read()

                # Now you can use 'file_contents' as a bytes-like object
                # For example, if you want to write it to a file:
                with open(full_path, 'wb') as f:
                    f.write(file_contents)
                with open(full_path2, 'wb') as f:
                    f.write(file_content)
                with open(full_path, 'rb') as img_file:
                    image_content = img_file.read()
                    base64_image = base64.b64encode(image_content).decode('utf-8')

                with open(full_path2, 'rb') as img_file2:
                    image_content2 = img_file2.read()
                    base64_image2 = base64.b64encode(image_content2).decode('utf-8')

                # Prepare the payload
                payload = {
                    "api_key": api_key,
                    "api_secret": api_secret,
                    # "image_file1": image_path1,
                    # "image_file2": image_path2,
                    # "face_token1": "50da07384227fd1480595303ac83ff29",
                    # "face_token2": "6fd9b603e6cdb3920480eb8c2cbc6f05",
                    "image_base64_1":base64_image,
                    "image_base64_2":base64_image2,

                }
                # Send the POST request
                response = requests.post(url, data=payload)
                print(response.json())

                # Print the response
                #print(response.json())
                response=response.json()
                confidence = response['confidence']
                threshold = 50

                if confidence >= threshold:
                        http_response = "<b>Match between two photos is successful with confidence: {:.2f}</b>".format(confidence)
                else:
                    http_response = "<b>Match between two photos is not successful. Confidence is too low: {:.2f}</b>".format(confidence)
                    print(http_response)

                return HttpResponse(http_response)
    return render(request, 'home.html')
from django.db.models import Q
from django.core.paginator import Paginator 
def wbuddy(request):
    fnd = Friend.objects.filter(Q(user1=request.user.id) | Q(user2=request.user.id))#, is_fnf=1)
    friends=Owner.objects.filter(id__in=fnd)
    # for expert in experts_users:
    #     expert.save()
    # for expert in friends:
    #         print(expert.first_name)
    print(friends)

    paginator = Paginator(friends,1)
    page = request.GET.get('page', 1)
    page = int(page)
    context = {
        'paginator': paginator,
        'page_obj': paginator.get_page(page),
        'page_numbers_range': range(
            max(1, page - 2), min(paginator.num_pages, page + 2) + 1
        ),
    }
    data = paginator.get_page(page)
    return render(request, "wbuddyList.html", {'context': context})

def send_email(request):
 if request.method == "POST":
    with get_connection(
        host=settings.EMAIL_HOST,
        port=settings.EMAIL_PORT,
        username=settings.EMAIL_HOST_USER,
        password=settings.EMAIL_HOST_PASSWORD,
        use_tls=settings.EMAIL_USE_TLS
    ) as connection:
        subject = "From Nostalgia"  
        request.POST.get("subject")
        email_from = settings.EMAIL_HOST_USER
        [request.POST.get("email"), ]
        mail = "sabbir772002@gmail.com"
        recipient_list = [mail,"nhossain213005@bscse.uiu.ac.bd"]
        message = request.POST.get("message")
        context = {
            "user": request.user
        }
        html_message = render_to_string('mail.html', {
            'context': context})
        mail = EmailMessage(subject, html_message, email_from,
                            recipient_list, connection=connection)
        image_path = os.path.join(settings.MEDIA_ROOT, request.user.image.path)

        # with open(image_path, 'rb') as image_file:
        #                       mail.attach_file(image_path)
        
        # image_content_id = mail.attachments[0][0]
        # image_reference = f'cid:{image_content_id}'
        # print(image_reference)

        # html_content_with_cid = html_message.replace(
        #     request.user.image.url, image_reference)

        #mail.body = html_content_with_cid
        mail.content_subtype = 'html'
        mail.send()

        # html_message = "<p>Hey how are you?</p>"

        # msg.content_subtype = "html"
        # msg.send()
        # EmailMessage(subject, message, email_from,
        #  recipient_list, connection=connection).send()

        return render(request, 'index.html')


                        