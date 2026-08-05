from django.utils import timezone

from api.models import Friend, Notification, Owner, Overseer, Thana, Verified


DEFAULT_PROFILE_IMAGE = "/media/image/download_lX6bjA6.jpeg"


def profile_payload(username, viewer_username=None):
    try:
        user = Owner.objects.get(username=username)
        viewer = Owner.objects.get(username=viewer_username) if viewer_username and viewer_username != username else user
        verified = Verified.objects.filter(user=user).first()
        image_url = user.p_image.url if user.p_image else DEFAULT_PROFILE_IMAGE
        return {
            "ok": True,
            "data": {
                'id': user.id,
                'pp': image_url,
                'p_image': image_url,
                'first_name': user.first_name,
                'username': user.username,
                'last_name': user.last_name,
                'email': user.email,
                'gender': user.gender,
                'phone': user.phone,
                'dob': user.dob,
                'address': user.address,
                'nid': user.nid,
                'thana': Thana.objects.get(thana=user.thana_id).thana,
                'is_fnf': 1 if Friend.objects.filter(user1=user, user2=viewer, is_fnf=1).exists() else 1 if Friend.objects.filter(user2=user, user1=viewer, is_fnf=1).exists() else 0,
                'type': Friend.objects.filter(user1=user, user2=viewer).values_list('type', flat=True).first() if Friend.objects.filter(user1=user, user2=viewer).exists() else Friend.objects.filter(user2=user, user1=viewer).values_list('type', flat=True).first() if Friend.objects.filter(user2=user, user1=viewer).exists() else None,
                'f_created_date': Friend.objects.filter(user1=user, user2=viewer).values_list('f_created_date', flat=True).first() if Friend.objects.filter(user1=user, user2=viewer).exists() else Friend.objects.filter(user2=user, user1=viewer).values_list('f_created_date', flat=True).first() if Friend.objects.filter(user2=user, user1=viewer).exists() else None,
                'f_id': Friend.objects.filter(user1=user, user2=viewer).values_list('f_id', flat=True).first() if Friend.objects.filter(user1=user, user2=viewer).exists() else Friend.objects.filter(user2=user, user1=viewer).values_list('f_id', flat=True).first() if Friend.objects.filter(user2=user, user1=viewer).exists() else None,
                'abedon': 1 if Friend.objects.filter(user1=user, user2=viewer).exists() else 0,
                'good': 1 if Friend.objects.filter(user1=user, user2=viewer).exists() else 1 if Friend.objects.filter(user2=user, user1=viewer).exists() else 0,
                'status': 1 if Friend.objects.filter(user1=user, user2=viewer).exists() else 1 if Friend.objects.filter(user2=user, user1=viewer).exists() else 0,
                'img_privacy': 0,
                'walk_type': user.walk_type,
                'verify': 1 if verified is not None and verified.verified == 1 else 0,
            }
        }
    except Owner.DoesNotExist:
        try:
            user = Overseer.objects.get(username=username)
            return {
                "ok": True,
                "data": {
                    'id': user.id,
                    'pp': user.p_image.url if user.p_image else DEFAULT_PROFILE_IMAGE,
                    'p_image': user.p_image.url if user.p_image else DEFAULT_PROFILE_IMAGE,
                    'first_name': user.first_name,
                    'username': user.username,
                    'last_name': user.last_name,
                    'email': user.email,
                    'gender': user.gender,
                    'phone': user.phone,
                    'dob': user.dob,
                    'address': user.address,
                    'nid': user.nid,
                    'relation': user.Relation,
                    'location': user.Location,
                    'is_overseer': True,
                    'verify': 1,
                }
            }
        except Overseer.DoesNotExist:
            return {"ok": False, "data": {"message": "User not found"}}


def friend_request_payload(user_id, friend_id, relation_type):
    if str(user_id) == str(friend_id):
        return False, {"message": "You can't add yourself as friend"}, 400

    user = Owner.objects.get(id=user_id)
    friend = Owner.objects.get(id=friend_id)
    fnd = Friend.objects.filter(user1=user, user2=friend)
    fnd |= Friend.objects.filter(user2=user, user1=friend)
    if len(fnd) > 0 and fnd[0].is_fnf == 1:
        return False, {"message": "You are already friend"}, 400
    if len(fnd) > 0:
        return False, {"message": "Your request for friend send"}, 201

    fnd = Friend(user1=user, user2=friend, type=relation_type, f_created_date=timezone.now(), is_fnf=0)
    fnd.save()
    Notification.objects.create(
        noti_type="Bondhu",
        noti_msg="send you friend request",
        noti_sender=user,
        noti_receiver=friend,
        noti_status=0,
    )
    return True, {"message": "Friends Added successfully"}, 201


def update_friend_request_payload(user_id, friend_id, relation_type):
    if str(user_id) == str(friend_id):
        return False, {"message": "You can't add yourself as friend"}, 400

    user = Owner.objects.get(id=user_id)
    friend = Owner.objects.get(id=friend_id)
    fnd = Friend.objects.filter(user1=user, user2=friend)
    fnd |= Friend.objects.filter(user2=user, user1=friend)
    if len(fnd) > 0:
        if relation_type == "Delete":
            fnd[0].delete()
            return True, {"message": "Request Deleted successfully"}, 201
        fnd[0].is_fnf = 1 if fnd[0].is_fnf == 0 else fnd[0].is_fnf
        fnd[0].type = relation_type
        fnd[0].save()
        return True, {"message": "Friends Updated successfully"}, 201
    return False, {"message": "Friends not find"}, 400


def delete_friend_request_payload(user_id, friend_id):
    if str(user_id) == str(friend_id):
        return False, {"message": "You can't add yourself as friend"}, 400

    user = Owner.objects.get(id=user_id)
    friend = Owner.objects.get(id=friend_id)
    fnd = Friend.objects.filter(user1=user, user2=friend)
    fnd |= Friend.objects.filter(user2=user, user1=friend)
    if len(fnd) > 0:
        fnd[0].delete()
        return True, {"message": "Friends Deleted successfully"}, 201
    return False, {"message": "Friends not find"}, 400


def friend_list_payload(user_id):
    users = Owner.objects.all()
    serialized_data = []
    current_user = Owner.objects.filter(id=user_id).first() if user_id else None
    for user in users:
        if current_user is None:
            continue
        fnd = Friend.objects.filter(user1=current_user, user2=user)
        fnd2 = Friend.objects.filter(user2=current_user, user1=user)
        fnd = fnd[0] if len(fnd) > 0 else None
        if (fnd is not None and fnd.is_fnf == 1) or (len(fnd2) > 0 and fnd2[0].is_fnf == 1):
            img_url = user.p_image.url if user.p_image else DEFAULT_PROFILE_IMAGE
            serialized_data.append({
                'id': user.id,
                'pp': img_url,
                'p_image': img_url,
                'first_name': user.first_name,
                'username': user.username,
                'last_name': user.last_name,
                'email': user.email,
                'gender': user.gender,
                'phone': user.phone,
                'dob': user.dob,
                'address': user.address,
                'nid': user.nid,
                'thana': Thana.objects.get(thana=user.thana_id).thana,
                'is_fnf': fnd.is_fnf if fnd is not None else fnd2[0].is_fnf if len(fnd2) > 0 else None,
                'type': fnd.type if fnd is not None else fnd2[0].type if len(fnd2) > 0 else None,
                'f_created_date': fnd.f_created_date if fnd is not None else None,
                'f_id': fnd.f_id if fnd is not None else None,
                'abedon': 1 if fnd is not None else 0,
                'good': fnd.user1.username if fnd is not None else None,
                'msg': "gd night",
                'time': "12:00",
            })
    return serialized_data


def friend_suggestion_payload(user_id):
    user_obj = Owner.objects.filter(id=user_id).first() if user_id else None
    if user_obj:
        from api.recommender_service import decoupled_recommender

        ai_friends = decoupled_recommender.get_recommended_friends(user_obj.username, limit=30)
        if ai_friends:
            full_friends_data = []
            for cand in ai_friends:
                cand_user = Owner.objects.filter(id=cand['id']).first()
                if not cand_user:
                    continue
                fnd = Friend.objects.filter(user1=user_obj, user2=cand_user).first()
                fnd2 = Friend.objects.filter(user2=user_obj, user1=cand_user).first()
                full_friends_data.append({
                    'id': cand_user.id,
                    'pp': cand['pp'],
                    'p_image': cand['p_image'],
                    'first_name': cand_user.first_name,
                    'username': cand_user.username,
                    'last_name': cand_user.last_name,
                    'email': cand_user.email,
                    'gender': cand_user.gender,
                    'phone': cand_user.phone,
                    'dob': cand_user.dob,
                    'address': cand_user.address,
                    'nid': cand_user.nid,
                    'thana': cand['thana'],
                    'score': cand['score'],
                    'reason': cand['reason'],
                    'is_fnf': fnd.is_fnf if fnd else fnd2.is_fnf if fnd2 else None,
                    'type': fnd.type if fnd else fnd2.type if fnd2 else None,
                    'f_created_date': fnd.f_created_date if fnd else None,
                    'f_id': fnd.f_id if fnd else None,
                    'abedon': 1 if fnd else 0,
                    'good': fnd.user1.username if fnd else None,
                    'status': 1 if fnd else 1 if fnd2 else 0,
                })
            return True, full_friends_data, "AI Recommended buddies retrieved successfully"

    users = Owner.objects.all()
    serialized_data = []
    current_user = Owner.objects.filter(id=user_id).first() if user_id else None
    for user in users:
        if user_id and str(user.id) == str(user_id):
            continue
        fnd = Friend.objects.filter(user1=current_user, user2=user) if current_user else []
        fnd2 = Friend.objects.filter(user2=current_user, user1=user) if current_user else []
        if len(fnd) > 0 and fnd[0].is_fnf == 1:
            continue
        if len(fnd2) > 0 and fnd2[0].is_fnf == 1:
            continue
        fnd = fnd[0] if len(fnd) > 0 else None
        img_url = user.p_image.url if user.p_image else DEFAULT_PROFILE_IMAGE
        serialized_data.append({
            'id': user.id,
            'pp': img_url,
            'p_image': img_url,
            'first_name': user.first_name,
            'username': user.username,
            'last_name': user.last_name,
            'email': user.email,
            'gender': user.gender,
            'phone': user.phone,
            'dob': user.dob,
            'address': user.address,
            'nid': user.nid,
            'thana': Thana.objects.get(thana=user.thana_id).thana if user.thana_id else '',
            'is_fnf': fnd.is_fnf if fnd is not None else fnd2[0].is_fnf if len(fnd2) > 0 else None,
            'type': fnd.type if fnd is not None else fnd2[0].type if len(fnd2) > 0 else None,
            'f_created_date': fnd.f_created_date if fnd is not None else None,
            'f_id': fnd.f_id if fnd is not None else None,
            'abedon': 1 if fnd is not None else 0,
            'good': fnd.user1.username if fnd is not None else None,
            'status': 1 if fnd is not None else 1 if len(fnd2) > 0 else 0,
        })
    return True, serialized_data, "User information retrieved successfully"