from django.db.models import Q

from api.models import Additional, Blog, District, Friend, Owner, Thana, Upvote

DEFAULT_PROFILE_IMAGE = "/media/image/download_lsX6bjA6.jpeg"
DEFAULT_PROFILE_IMAGE_ALT = "/media/image/download_lX6bjA6.jpeg"


def search_blog_payload(search, username):
    blog = Blog.objects.filter(content__icontains=search)
    if search == " ":
        blog = Blog.objects.all()

    user = Owner.objects.get(username=username)
    blog_data = []
    for post in blog:
        blog_data.append({
            'id': post.blogid,
            'author': post.author.username,
            'content': post.content,
            'author_img': post.author.p_image.url if post.author.p_image else DEFAULT_PROFILE_IMAGE,
            'date': post.post_date,
            'time': post.post_time,
            'blog_img': post.blog_img.url if post.blog_img else None,
            'upvote': Upvote.objects.filter(blogid=post).count(),
            'is_upvoted': 1 if Upvote.objects.filter(blogid=post, Username=user).exists() else 0,
        })
    return blog_data


def search_friend_payload(search, username):
    if not username:
        return False, {"error": "Username is required"}, 400

    user = Owner.objects.get(username=username)
    userbox = Owner.objects.filter(Q(username__icontains=search) | Q(first_name__icontains=search) | Q(last_name__icontains=search))
    user_data = []
    for sorted_user in userbox:
        if sorted_user == user:
            continue
        img_url = sorted_user.p_image.url if sorted_user.p_image else DEFAULT_PROFILE_IMAGE_ALT
        fnd = Friend.objects.filter(user1=user, user2=sorted_user)
        fnd2 = Friend.objects.filter(user2=user, user1=sorted_user)
        fnd = fnd[0] if len(fnd) > 0 else None
        user_data.append({
            'id': sorted_user.id,
            'first_name': sorted_user.first_name,
            'last_name': sorted_user.last_name,
            'username': sorted_user.username,
            'email': sorted_user.email,
            'gender': sorted_user.gender,
            'phone': sorted_user.phone,
            'dob': sorted_user.dob,
            'address': sorted_user.address,
            'nid': sorted_user.nid,
            'thana': Thana.objects.get(thana=sorted_user.thana).thana,
            'pp': img_url,
            'p_image': img_url,
            'is_fnf': fnd.is_fnf if fnd is not None else fnd2[0].is_fnf if len(fnd2) > 0 else 0,
            'type': fnd.type if fnd is not None else fnd2[0].type if len(fnd2) > 0 else None,
            'f_created_date': fnd.f_created_date if fnd is not None else fnd2[0].f_created_date if len(fnd2) > 0 else None,
            'f_id': fnd.f_id if fnd is not None else fnd2[0].f_id if len(fnd2) > 0 else None,
            'abedon': 1 if fnd is not None else 0,
            'good': fnd.user1.username if fnd is not None else fnd2[0].user1.username if len(fnd2) > 0 else None,
            'status': 1 if fnd is not None else 1 if len(fnd2) > 0 else 0,
        })
    return True, {"users": user_data, "message": "User retrieved successfully"}, 200


def search_friend_box_payload(search, username):
    box = Owner.objects.get(username=username)
    userbox = Owner.objects.filter(Q(username__icontains=search) | Q(first_name__icontains=search) | Q(last_name__icontains=search))
    user_data = []
    users = Owner.objects.all()
    for user in users:
        fnd = Friend.objects.filter(user1=Owner.objects.get(id=box.id), user2=user.id)
        fnd2 = Friend.objects.filter(user2=Owner.objects.get(id=box.id), user1=user.id)
        fnd = fnd[0] if len(fnd) > 0 else None
        if user not in userbox:
            continue
        if (fnd is not None and fnd.is_fnf == 1) or (len(fnd2) > 0 and fnd2[0].is_fnf == 1):
            img_url = user.p_image.url if user.p_image else DEFAULT_PROFILE_IMAGE_ALT
            user_data.append({
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
    return user_data


def add_info_payload(user_id):
    user = Owner.objects.get(id=user_id)
    add = Additional.objects.filter(user=user)
    add_data = []
    for entry in add:
        add_data.append({
            'id': entry.id,
            'type': 1 if entry.type in ["Study", "College", "School", "University"] else 0,
            'content': entry.content,
        })
    return add_data


def add_handler_action(data):
    add = Additional.objects.create(user=Owner.objects.get(username=data['username']), type=data['type'], content=data['content'])
    add.save()
    return {"message": "Extra Info added successfully"}


def find_thana_payload(district_id):
    return list(Thana.objects.filter(district_id=district_id).values_list('thana', flat=True))


def find_district_payload(division_id):
    return list(District.objects.filter(division_id=division_id).values_list('district', flat=True))