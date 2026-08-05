import random
import string

from django.contrib.auth import authenticate, login

from api.models import Owner, Overseer
from api.serializers import OwnerSerializer, OverseerSerializer


DEFAULT_PROFILE_IMAGE = "/media/image/download_lX6bjA6.jpeg"


def create_owner_account(data):
    serializer = OwnerSerializer(data=data)
    if serializer.is_valid():
        user = serializer.save()
        return serializer, user
    return serializer, None


def create_overseer_account(data):
    serializer = OverseerSerializer(data=data)
    if serializer.is_valid():
        user = serializer.save()
        return serializer, user
    return serializer, None


def login_as_owner_or_overseer(request, username, password):
    user = authenticate(request, username=username, password=password)
    if user is None:
        return None

    login(request, user)

    owner = Owner.objects.filter(username=username).first()
    if owner is not None:
        return {
            "auth": True,
            "user": OwnerSerializer(owner).data,
        }

    overseer = Overseer.objects.filter(username=username).first()
    if overseer is None:
        return {"auth": True, "user": None}

    serializer = OverseerSerializer(overseer)
    username_parts = username.split("@")
    owner_username = username_parts[1] if len(username_parts) > 1 else username
    owner = Owner.objects.filter(username=owner_username).first()
    image_url = owner.p_image.url if owner and owner.p_image else DEFAULT_PROFILE_IMAGE

    payload = serializer.data
    payload["pp"] = image_url
    payload["p_image"] = image_url
    return {
        "auth": True,
        "user": payload,
    }


def change_password(username, old_password, new_password):
    user = Owner.objects.filter(username=username).first()
    if user is None:
        return False, "User does not exist."

    if not user.check_password(old_password):
        return False, "Old password is incorrect."

    user.set_password(new_password)
    user.save()
    return True, {"message": "Password changed successfully"}


def reset_password(username, new_password):
    user = Owner.objects.filter(username=username).first()
    if user is None:
        return False, {"error": "User not found"}

    user.set_password(new_password)
    user.save()
    return True, {"message": "Password changed successfully"}


def build_otp_response(username):
    user = Owner.objects.filter(username=username).first()
    if user is None:
        return False, {"message": "User not found"}

    verification_code = "".join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return True, {
        "message": "Verification email sent successfully",
        "code": verification_code,
        "username": user.username,
    }