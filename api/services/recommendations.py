from datetime import datetime

from api.ai_client import AIEmbeddingClient
from api.models import (
    Blog,
    Event,
    Friend,
    GroupMember,
    JoinEvent,
    Owner,
    Thana,
    Trip,
    TripMember,
    Walk,
    WalkMember,
    CommunityGroup as Group,
)
from api.recommender import recommender_engine
from api.recommender_service import decoupled_recommender


DEFAULT_PROFILE_IMAGE = "/media/image/download_lX6bjA6.jpeg"
DEFAULT_GROUP_IMAGE = "/media/image/download_lsX6bjA6.jpeg"
DEFAULT_EVENT_IMAGE = "/media/image/default.jpeg"


def recommended_feed_posts(username):
    if not username:
        return []
    return decoupled_recommender.get_recommended_posts(username)


def recommended_friend_suggestions(username=None, user_id=None):
    if not username and user_id:
        try:
            owner = Owner.objects.get(id=user_id)
            username = owner.username
        except Exception:
            pass
    if not username and user_id:
        try:
            owner = Owner.objects.get(username=user_id)
            username = owner.username
        except Exception:
            pass
    if not username:
        return None
    return recommender_engine.get_recommended_friends(username)


def recommended_group_payload(user_id):
    if not user_id:
        return []
    user = Owner.objects.filter(id=user_id).first()
    if user:
        ai_groups = decoupled_recommender.get_recommended_groups(user.username, limit=20)
        if ai_groups:
            return ai_groups

    groups = Group.objects.all()[:20]
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
            'member': 1 if user and GroupMember.objects.filter(G_username=group, member_id=user, accept=1).exists() else 0,
        })
    return groups_data


def recommended_trip_payload(username):
    if not username:
        return []

    ai_trips = decoupled_recommender.get_recommended_trips(username, limit=20)
    user = Owner.objects.filter(username=username).first()
    if ai_trips:
        formatted_trips = []
        for item in ai_trips:
            t = Trip.objects.filter(id=item['id']).first() if 'id' in item else None
            if t:
                formatted_trips.append({
                    'id': t.TripID,
                    'name': t.name,
                    'location': t.Location,
                    'start_date': t.start_date,
                    'end_date': t.end_date,
                    'propose_date': t.propose_date,
                    'privacy': t.Privacy,
                    'creator': t.Creator.username if t.Creator else '',
                    'thana': t.Thana.thana if t.Thana else '',
                    'guide': t.guide,
                    'score': item.get('score', 0.5),
                    'reason': item.get('reason', 'AI Recommended Trip'),
                    'member': 1 if user and TripMember.objects.filter(TripID=t, member=user, Approve=1, cancel=0).exists() else 0,
                    'join': 1 if user and TripMember.objects.filter(TripID=t, member=user, Approve=0, cancel=0).exists() else 0,
                })
        if formatted_trips:
            return {"trips": formatted_trips, "message": "AI Recommended trips retrieved successfully"}

    trips = Trip.objects.all()[:20]
    serialized_data = []
    for trip in trips:
        serialized_data.append({
            'id': trip.TripID,
            'name': trip.name,
            'location': trip.Location,
            'start_date': trip.start_date,
            'end_date': trip.end_date,
            'propose_date': trip.propose_date,
            'privacy': trip.Privacy,
            'creator': trip.Creator.username if trip.Creator else '',
            'thana': trip.Thana.thana if trip.Thana else '',
            'guide': trip.guide,
            'member': 1 if user and TripMember.objects.filter(TripID=trip, member=user, Approve=1, cancel=0).exists() else 0,
            'join': 1 if user and TripMember.objects.filter(TripID=trip, member=user, Approve=0, cancel=0).exists() else 0,
        })
    return {"trips": serialized_data, "message": "Trip information retrieved successfully"}


def recommended_walk_payload(username):
    if not username:
        return {"error": "Username required"}, 400
    if '@' in username:
        username = username.split('@')[1]
    user = Owner.objects.filter(username=username).first()
    if not user:
        return {"error": "User not found"}, 404

    ai_client = AIEmbeddingClient()
    user_vec = decoupled_recommender.get_user_vector(user) if ai_client.is_service_available() else []
    friend_ids = Friend.objects.filter(user1=user, is_fnf=1).values_list('user2_id', flat=True)
    friend_ids2 = Friend.objects.filter(user2=user, is_fnf=1).values_list('user1_id', flat=True)
    friend_ids = list(friend_ids) + list(friend_ids2) + [user.id]
    walks = Walk.objects.filter(w_creator__in=friend_ids).order_by('-walk_date', '-end_date').distinct()

    scored_walks = []
    for walk in walks:
        if walk.privacy == "Bondhu":
            fd = Friend.objects.filter(user1=user, user2=walk.w_creator) | Friend.objects.filter(user2=user, user1=walk.w_creator)
            if not fd.exists():
                continue
        if walk.end_date < datetime.now().date():
            continue

        member_count = WalkMember.objects.filter(walk_id=walk.walk_id, accept=1).count()
        score = member_count * 0.1

        if user_vec and ai_client.is_service_available():
            walk_vec = ai_client.get_event_embedding({
                'title': walk.walk_name,
                'location': walk.address,
                'description': walk.walk_name,
            })
            if walk_vec:
                sim = ai_client.compute_similarity(user_vec, walk_vec)
                score += float(sim) * 0.5

        scored_walks.append((walk, score))

    scored_walks.sort(key=lambda x: x[1], reverse=True)
    walks_data = []
    for walk, score in scored_walks:
        walks_data.append({
            'id': walk.walk_id,
            'w_creator': walk.w_creator.username,
            'img': walk.w_creator.p_image.url if walk.w_creator.p_image else DEFAULT_PROFILE_IMAGE,
            'walk_name': walk.walk_name,
            'propose': walk.propose_date,
            'date': datetime.strptime(str(walk.walk_date), '%Y-%m-%d').strftime('%d %B %Y'),
            'privacy': walk.privacy,
            'end': datetime.strptime(str(walk.end_date), '%Y-%m-%d').strftime('%d %B %Y'),
            'location': walk.address,
            'member': 1 if WalkMember.objects.filter(walk_id=walk.walk_id, username=user).exists() else 0,
            'not_ac': 1 if WalkMember.objects.filter(walk_id=walk.walk_id, username=user, accept=0).exists() else 0,
            'cancel': 1 if WalkMember.objects.filter(walk_id=walk.walk_id, username=user, cancel=1).exists() else 0,
            'time': walk.time,
            'recommendation_score': round(score, 4),
            'reason': 'AI matched your interests' if score > 0.3 else 'Popular in your network',
        })
    return walks_data, 200


def recommended_event_payload(username):
    user = Owner.objects.filter(username=username).first() if username else None
    if not user:
        return {"error": "User not found"}, 404

    ai_client = AIEmbeddingClient()
    user_vec = decoupled_recommender.get_user_vector(user) if ai_client.is_service_available() else []
    events = Event.objects.all()
    scored_events = []
    for event in events:
        member_count = JoinEvent.objects.filter(EventID=event, Approve=1).count()
        score = member_count * 0.1

        if user_vec and ai_client.is_service_available():
            event_vec = ai_client.get_event_embedding({
                'title': event.Event_title,
                'location': event.Address,
                'description': event.Description,
            })
            if event_vec:
                sim = ai_client.compute_similarity(user_vec, event_vec)
                score += float(sim) * 0.5

        scored_events.append((event, score))

    scored_events.sort(key=lambda x: x[1], reverse=True)
    serialized_data = []
    for event, score in scored_events:
        serialized_data.append({
            'id': event.EventID,
            'Description': event.Description,
            'Event_title': event.Event_title,
            'start_time': event.start_time,
            'end_time': event.end_time,
            'start_date': event.start_date,
            'end_date': event.end_date,
            'Address': event.Address,
            'create_date': event.create_date,
            'Approve': event.Approve,
            'E_type': event.E_type,
            'Image': event.Image.url if event.Image else DEFAULT_EVENT_IMAGE,
            'E_creator': event.E_creator.username,
            'privacy': event.privacy,
            'Thana': event.Thana.thana if event.Thana else None,
            'Member': 1 if JoinEvent.objects.filter(EventID=event, Member=user).exists() else 0,
            'recommendation_score': round(score, 4),
            'reason': 'AI matched your interests' if score > 0.3 else 'Popular event',
        })
    return {"events": serialized_data, "message": "Event information retrieved successfully"}, 200