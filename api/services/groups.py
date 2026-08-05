from datetime import datetime

from api.models import CommunityGroup as Group, GroupMember, GroupPost, Owner

DEFAULT_PROFILE_IMAGE = "/media/image/download_lsX6bjA6.jpeg"


def create_group(data):
    if Group.objects.filter(G_username=data['username']).exists():
        return False, {"msg": "Group already exists"}, 200
    group = Group.objects.create(
        G_name=data['name'],
        Creator=Owner.objects.get(id=data['id']),
        CreatedDate=datetime.now().strftime('%Y-%m-%d'),
        G_username=data['username'],
        Privacy=data['privacy'],
        Topic=data['topic'],
        time=datetime.now().strftime('%H:%M:%S'),
    )
    group.save()
    GroupMember.objects.create(
        G_username=Group.objects.get(G_username=data['username']),
        member_id=Owner.objects.get(id=data['id']).id,
        accept=1,
        Block=2,
    )
    return True, {"message": "Group created successfully"}, 201


def list_user_groups(user_id):
    user = Owner.objects.get(id=user_id)
    groups = GroupMember.objects.filter(member_id=user, accept=1).values_list('G_username', flat=True).distinct()
    groups = Group.objects.filter(G_username__in=groups)
    groups_data = []
    for group in groups:
        groups_data.append({
            'username': group.G_username,
            'name': group.G_name,
            'creator': group.Creator.username,
            'created_date': group.CreatedDate,
            'privacy': group.Privacy,
            'topic': group.Topic,
            'time': group.time,
            'img': group.img.url if group.img else DEFAULT_PROFILE_IMAGE,
            'member': 1 if GroupMember.objects.filter(G_username=group, member_id=user, accept=1).exists() else 0,
        })
    return groups_data


def group_profile_payload(username, viewer_id):
    user = Owner.objects.get(id=viewer_id)
    group = Group.objects.get(G_username=username)
    return {
        'username': group.G_username,
        'name': group.G_name,
        'img': group.img.url if group.img else DEFAULT_PROFILE_IMAGE,
        'admin': group.Creator.username,
        'created_date': group.CreatedDate,
        'privacy': group.Privacy,
        'topic': group.Topic,
        'time': group.time,
        'gp': group.Creator.p_image.url if group.Creator.p_image else DEFAULT_PROFILE_IMAGE,
        'member': 1 if GroupMember.objects.filter(G_username=group, member_id=user, accept=1).exists() else 0,
        'accept': 1 if GroupMember.objects.filter(G_username=group, member_id=user, accept=0).exists() else 0,
    }


def group_posts_for_group(username):
    group = Group.objects.get(G_username=username)
    posts = GroupPost.objects.filter(G_username=group).order_by('-GPost_date', '-GPost_Time')
    posts_data = []
    for post in posts:
        posts_data.append({
            'id': post.GPost_id,
            'group_username': post.G_username.G_username,
            'author': post.p_username.username,
            'group_name': post.G_username.G_name,
            'author_img': post.p_username.p_image.url if post.p_username.p_image else DEFAULT_PROFILE_IMAGE,
            'content': post.GPost_contents,
            'post_date': post.GPost_date,
            'post_time': post.GPost_Time,
            'post_img': post.GPost_image.url if post.GPost_image else None,
        })
    return posts_data


def group_posts_for_member_feed(username):
    groups = GroupMember.objects.filter(member_id=Owner.objects.get(username=username), accept=1).values_list('G_username', flat=True).distinct()
    posts = GroupPost.objects.filter(G_username__in=groups).order_by('-GPost_date', '-GPost_Time')
    posts_data = []
    for post in posts:
        posts_data.append({
            'id': post.GPost_id,
            'group_username': post.G_username.G_username,
            'author': post.p_username.username,
            'group_name': post.G_username.G_name,
            'author_img': post.p_username.p_image.url if post.p_username.p_image else DEFAULT_PROFILE_IMAGE,
            'content': post.GPost_contents,
            'post_date': post.GPost_date,
            'post_time': post.GPost_Time,
            'post_img': post.GPost_image.url if post.GPost_image else None,
        })
    return posts_data


def join_group(data):
    group = Group.objects.get(G_username=data['group'])
    member_id = Owner.objects.get(id=data['user_id']).id
    if data['type'] == 'Delete':
        group_member = GroupMember.objects.filter(G_username=group, member_id=member_id)
        group_member.delete()
        return True, {"message": "Request deleted successfully"}, 201
    if GroupMember.objects.filter(G_username=group, member_id=member_id).exists():
        return False, {"msg": "You are already a member of this group", "ok": 0}, 200
    group_member = GroupMember.objects.create(G_username=group, member_id=member_id, accept=0, Block=0)
    group_member.save()
    return True, {"message": "Request sent successfully"}, 201


def add_group_post(data):
    user = Owner.objects.get(username=data['username'])
    group = Group.objects.get(G_username=data['gp'])
    blog_img = data.get('blog_img')
    if blog_img is not None:
        post = GroupPost.objects.create(
            G_username=group,
            p_username=user,
            GPost_contents=data['content'],
            GPost_date=data['post_date'],
            GPost_Time=data['post_time'],
            GPost_image=blog_img,
        )
    else:
        post = GroupPost.objects.create(
            G_username=group,
            p_username=user,
            GPost_contents=data['content'],
            GPost_date=data['post_date'],
            GPost_Time=data['post_time'],
        )
    post.save()
    return {"message": "Group Blog created successfully"}


def group_members_payload(username):
    group = Group.objects.get(G_username=username)
    members = GroupMember.objects.filter(G_username=group, accept=1)
    members_data = []
    for member in members:
        members_data.append({
            'id': member.MemberID,
            'username': member.member.username,
            'img': member.member.p_image.url if member.member.p_image else DEFAULT_PROFILE_IMAGE,
            'first_name': member.member.first_name,
            'last_name': member.member.last_name,
            'email': member.member.email,
            'phone': member.member.phone,
            'dob': member.member.dob,
            'Since': member.JoinDate,
            'gender': member.member.gender,
        })
    return members_data


def request_members_payload(username):
    group = Group.objects.get(G_username=username)
    members = GroupMember.objects.filter(G_username=group, accept=0)
    members_data = []
    for member in members:
        members_data.append({
            'member_id': member.MemberID,
            'id': member.member.id,
            'username': member.member.username,
            'img': member.member.p_image.url if member.member.p_image else DEFAULT_PROFILE_IMAGE,
            'first_name': member.member.first_name,
            'last_name': member.member.last_name,
            'email': member.member.email,
            'phone': member.member.phone,
            'dob': member.member.dob,
            'Since': member.JoinDate,
        })
    return members_data


def group_request_action(data):
    group = GroupMember.objects.filter(G_username=Group.objects.get(G_username=data['group']), member_id=Owner.objects.get(id=data['user_id']).id)
    if len(group) == 0:
        return False, {"msg": "User not found"}, 200
    group = group[0]
    if data['type'] == 'Delete':
        group.delete()
        return True, {"message": "Request deleted successfully"}, 201
    if data['type'] == "confirm":
        group.accept = 1
        group.save()
        return True, {"message": "Request accepted successfully"}, 201
    if data['type'] == "Block":
        group.Block = 1
        group.save()
        return True, {"message": "Request blocked successfully"}, 201
    if data['type'] == "Unblock":
        group.Block = 0
        group.save()
        return True, {"message": "Request unblocked successfully"}, 201
    if data['type'] == "Remove":
        group.delete()
        return True, {"message": "Request removed successfully"}, 201
    return False, {"message": "Invalid request"}, 400


def delete_group_membership(data):
    gmember = GroupMember.objects.get(G_username=data['guser'], member_id=Owner.objects.get(username=data['username']))
    gmember.delete()
    return {"message": "Group deleted successfully"}


def update_group_payload(data):
    group = Group.objects.get(G_username=data['username'])
    group.G_name = data['name']
    group.Privacy = data['privacy']
    group.Topic = data['topic']
    img = data.get('img')
    if img:
        group.img = img
    group.save()
    return {"message": "Group updated successfully"}