import os

from django.contrib.auth import authenticate, login as auth_login, logout
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from api.models import Friend, Owner

from .services import (
    HOME_LOGIN_ERROR,
    add_friend_remote,
    authenticate_remote_signup,
    compare_default_media_images,
    save_uploaded_images_for_compare,
    send_nostalgia_email,
)


@csrf_exempt
def home(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return render(request, 'home.html')
        else:
            return HttpResponse(HOME_LOGIN_ERROR)
    return render(request, 'home.html')


@csrf_exempt
def log_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return render(request, 'home.html')
        else:
            return HttpResponse(HOME_LOGIN_ERROR)
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


@csrf_exempt
def friends(request):
    return HttpResponse("Hello, this is the friends page!")


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        walk_type = request.POST.get('walk_type', "alone")
        gender = request.POST.get('gender')
        phone = request.POST.get('phone')
        dob = request.POST.get('dob', '2022-01-01')
        address = request.POST.get('address')
        nid = request.POST.get('nid')

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
            'thana': 1,
        }

        try:
            response = authenticate_remote_signup(data)
            if response.status_code == 201:
                return redirect('home')
        except Exception as e:
            print("Signup error:", e)

        return render(request, 'signup.html')
    else:
        return render(request, 'signup.html')


def profile(request):
    if not request.user.is_authenticated:
        return redirect('log_in')
    user = Owner.objects.get(username=request.user.username)
    friends_qs = Owner.objects.all()
    return render(request, 'profile.html', {"profile": user, "friends": friends_qs})


def add_friend(request, id):
    if not request.user.is_authenticated:
        return redirect('log_in')
    try:
        add_friend_remote(request.user.id, id)
    except Exception as e:
        print("Add friend error:", e)

    fnd = Friend.objects.filter(user1=id, is_fnf=1)
    friends_qs = Owner.objects.exclude(id__in=fnd)
    return render(request, 'profile.html', {"profile": Owner.objects.get(id=id), "friends": friends_qs})


def match(request):
    try:
        return JsonResponse(compare_default_media_images())
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def upload_image(request):
    if request.method == 'POST':
        image_path1 = request.FILES.get('image')
        image_path2 = request.FILES.get('image2')
        if image_path1 and image_path2:
            try:
                save_uploaded_images_for_compare(image_path1, image_path2)
                resp = compare_default_media_images()
                confidence = resp.get('confidence', 0)
                if confidence >= 50:
                    http_response = f"<b>Match between two photos is successful with confidence: {confidence:.2f}</b>"
                else:
                    http_response = f"<b>Match between two photos is not successful. Confidence is too low: {confidence:.2f}</b>"
                return HttpResponse(http_response)
            except Exception as e:
                return HttpResponse(f"Error comparing images: {e}")
    return render(request, 'home.html')


def wbuddy(request):
    fnd = Friend.objects.filter(Q(user1=request.user.id) | Q(user2=request.user.id))
    friends_qs = Owner.objects.filter(id__in=fnd)

    paginator = Paginator(friends_qs, 1)
    page = int(request.GET.get('page', 1))
    context = {
        'paginator': paginator,
        'page_obj': paginator.get_page(page),
        'page_numbers_range': range(
            max(1, page - 2), min(paginator.num_pages, page + 2) + 1
        ),
    }
    return render(request, "wbuddyList.html", {'context': context})


def send_email(request):
    if request.method == "POST":
        try:
            send_nostalgia_email(request.user)
        except Exception as e:
            print("Send email error:", e)
        return render(request, 'index.html')
    return render(request, 'index.html')