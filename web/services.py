import base64
import os

import requests
from django.conf import settings
from django.core.mail import EmailMessage, get_connection
from django.template.loader import render_to_string


HOME_LOGIN_ERROR = "mile nai vai tomar username or password"
DEFAULT_SIGNUP_API_URL = os.environ.get("NOSTALGIA_SIGNUP_API_URL", "http://127.0.0.1:8001/api/sign")
DEFAULT_FRIEND_API_URL = os.environ.get("NOSTALGIA_FRIEND_API_URL", "http://127.0.0.1:8001/api/add_fnf")
FACEPP_API_URL = os.environ.get(
    "FACEPP_API_URL",
    "https://api-us.faceplusplus.com/facepp/v3/compare",
)
FACEPP_API_KEY = os.environ.get("FACEPP_API_KEY", "edEq6oq-Eqf3Sq4sfszoXpRQ9FHRRQGx")
FACEPP_API_SECRET = os.environ.get("FACEPP_API_SECRET", "Ky2HfeEgU58UvJkmCt5nIe97DMEeswRy")
DEFAULT_FACE_IMAGE_ONE = "5.png"
DEFAULT_FACE_IMAGE_TWO = "bb.png"


def authenticate_remote_signup(payload):
    return requests.post(DEFAULT_SIGNUP_API_URL, data=payload)


def add_friend_remote(user_id, friend_id):
    payload = {"user_id": user_id, "friend_id": friend_id}
    return requests.post(DEFAULT_FRIEND_API_URL, data=payload)


def compare_images_from_paths(image_path_one, image_path_two):
    with open(image_path_one, "rb") as image_file_one:
        base64_image_one = base64.b64encode(image_file_one.read()).decode("utf-8")
    with open(image_path_two, "rb") as image_file_two:
        base64_image_two = base64.b64encode(image_file_two.read()).decode("utf-8")

    payload = {
        "api_key": FACEPP_API_KEY,
        "api_secret": FACEPP_API_SECRET,
        "image_base64_1": base64_image_one,
        "image_base64_2": base64_image_two,
    }
    return requests.post(FACEPP_API_URL, data=payload)


def compare_default_media_images():
    image_path_one = os.path.join(settings.MEDIA_ROOT, DEFAULT_FACE_IMAGE_ONE)
    image_path_two = os.path.join(settings.MEDIA_ROOT, DEFAULT_FACE_IMAGE_TWO)
    response = compare_images_from_paths(image_path_one, image_path_two)
    return response.json()


def save_uploaded_images_for_compare(upload_one, upload_two):
    image_path_one = os.path.join(settings.MEDIA_ROOT, DEFAULT_FACE_IMAGE_ONE)
    image_path_two = os.path.join(settings.MEDIA_ROOT, DEFAULT_FACE_IMAGE_TWO)

    with open(image_path_one, "wb") as output_one:
        output_one.write(upload_one.read())
    with open(image_path_two, "wb") as output_two:
        output_two.write(upload_two.read())

    return image_path_one, image_path_two


def send_nostalgia_email(user):
    with get_connection(
        host=settings.EMAIL_HOST,
        port=settings.EMAIL_PORT,
        username=settings.EMAIL_HOST_USER,
        password=settings.EMAIL_HOST_PASSWORD,
        use_tls=settings.EMAIL_USE_TLS,
    ) as connection:
        subject = "From Nostalgia"
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ["sabbir772002@gmail.com", "nhossain213005@bscse.uiu.ac.bd"]
        context = {"user": user}
        html_message = render_to_string("mail.html", {"context": context})
        mail = EmailMessage(subject, html_message, email_from, recipient_list, connection=connection)
        mail.content_subtype = "html"
        mail.send()