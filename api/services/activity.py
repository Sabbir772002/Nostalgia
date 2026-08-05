from datetime import datetime

from django.utils import timezone

from api.models import (
    DoneMed,
    Event,
    JoinEvent,
    MedAlert,
    Medication,
    Owner,
    Thana,
    Trip,
    TripMember,
    Walk,
    WalkMember,
)

DEFAULT_PROFILE_IMAGE = "/media/image/download_lsX6bjA6.jpeg"


def walk_members_payload(walk_id):
    members = WalkMember.objects.filter(walk_id=walk_id, cancel=0, accept=1)
    members_data = []
    for member in members:
        members_data.append({
            'id': member.username.id,
            'username': member.username.username,
            'img': member.username.p_image.url if member.username.p_image else DEFAULT_PROFILE_IMAGE,
            'first_name': member.username.first_name,
            'last_name': member.username.last_name,
            'email': member.username.email,
            'phone': member.username.phone,
            'dob': _age(member.username.dob),
            'gender': member.username.gender,
        })
    return members_data


def walk_request_action(walk_id, username):
    walk = Walk.objects.get(walk_id=walk_id)
    bot = WalkMember.objects.filter(walk_id=walk, username=Owner.objects.get(username=username))
    if len(bot) > 0:
        return True, {"user": bot[0].username.username}, 200
    members = WalkMember.objects.create(username=Owner.objects.get(username=username), walk_id=Walk.objects.get(walk_id=walk_id), cancel=0, accept=0)
    members.save()
    return True, {"message": "Request sent successfully"}, 201


def walk_not_member_payload(walk_id):
    members = WalkMember.objects.filter(walk_id=walk_id, accept=0)
    members_data = []
    for member in members:
        members_data.append({
            'id': member.username.id,
            'username': member.username.username,
            'img': member.username.p_image.url if member.username.p_image else DEFAULT_PROFILE_IMAGE,
            'first_name': member.username.first_name,
            'last_name': member.username.last_name,
            'email': member.username.email,
            'phone': member.username.phone,
            'dob': _age(member.username.dob),
            'gender': member.username.gender,
        })
    return members_data


def handle_walk_member(action, walk_id, user_id):
    user = Owner.objects.get(id=user_id)
    walk = Walk.objects.get(walk_id=walk_id)
    members = WalkMember.objects.filter(walk_id=walk, username=user)
    if len(members) > 0:
        if action == 'confirm':
            members[0].accept = 1
            members[0].save()
        elif action == 'delete':
            members[0].delete()
        return True, {"user": members[0].username.username if action == 'confirm' else user.username}, 200
    return False, {"message": "User not found"}, 404


def event_members_payload(event_id):
    members = JoinEvent.objects.filter(EventID=event_id, cancel=0)
    members_data = []
    for member in members:
        members_data.append({
            'id': member.Member.id,
            'username': member.Member.username,
            'img': member.Member.p_image.url if member.Member.p_image else DEFAULT_PROFILE_IMAGE,
            'first_name': member.Member.first_name,
            'last_name': member.Member.last_name,
            'email': member.Member.email,
            'phone': member.Member.phone,
            'dob': _age(member.Member.dob),
            'gender': member.Member.gender,
        })
    return members_data


def event_not_member_payload(event_id):
    members = JoinEvent.objects.filter(EventID=event_id, Approve=0)
    members_data = []
    for member in members:
        members_data.append({
            'id': member.Member.id,
            'username': member.Member.username,
            'img': member.Member.p_image.url if member.Member.p_image else DEFAULT_PROFILE_IMAGE,
            'first_name': member.Member.first_name,
            'last_name': member.Member.last_name,
            'email': member.Member.email,
            'phone': member.Member.phone,
            'dob': _age(member.Member.dob),
            'gender': member.Member.gender,
        })
    return members_data


def handle_event_member(action, event_id, user_id):
    user = Owner.objects.get(id=user_id)
    event = Event.objects.get(EventID=event_id)
    members = JoinEvent.objects.filter(EventID=event, Member=user)
    if len(members) > 0:
        if action == 'confirm':
            members[0].Approve = 1
            members[0].save()
        elif action == 'delete':
            members[0].delete()
        return True, {"user": members[0].Member.username if action == 'confirm' else user.username}, 200
    return False, {"message": "User not found"}, 404


def event_request_action(event_id, username):
    event = Event.objects.get(EventID=event_id)
    bot = JoinEvent.objects.filter(EventID=event, Member=Owner.objects.get(username=username))
    if len(bot) > 0:
        return True, {"user": bot[0].Member.username}, 200
    members = JoinEvent.objects.create(Member=Owner.objects.get(username=username), EventID=Event.objects.get(EventID=event_id), cancel=0, Approve=1)
    members.save()
    return True, {"message": "Request sent successfully"}, 201


def trip_members_payload(trip_id):
    members = TripMember.objects.filter(TripID=trip_id, cancel=0, Approve=1)
    members_data = []
    for member in members:
        members_data.append({
            'id': member.member.id,
            'trip': member.TripID.TripID,
            'username': member.member.username,
            'img': member.member.p_image.url if member.member.p_image else DEFAULT_PROFILE_IMAGE,
            'first_name': member.member.first_name,
            'last_name': member.member.last_name,
            'email': member.member.email,
            'phone': member.member.phone,
            'dob': _age(member.member.dob),
            'gender': member.member.gender,
        })
    return members_data


def trip_request_action(trip_id, username):
    trip = Trip.objects.get(TripID=trip_id)
    bot = TripMember.objects.filter(TripID=trip, member=Owner.objects.get(username=username))
    if len(bot) > 0:
        return True, {"user": bot[0].member.username}, 200
    members = TripMember.objects.create(member=Owner.objects.get(username=username), TripID=Trip.objects.get(TripID=trip_id), cancel=0, Approve=0)
    members.save()
    return True, {"message": "Request sent successfully"}, 201


def trip_not_member_payload(trip_id):
    members = TripMember.objects.filter(TripID=trip_id, Approve=0, cancel=0)
    members_data = []
    for member in members:
        members_data.append({
            'id': member.member.id,
            'username': member.member.username,
            'img': member.member.p_image.url if member.member.p_image else DEFAULT_PROFILE_IMAGE,
            'first_name': member.member.first_name,
            'last_name': member.member.last_name,
            'email': member.member.email,
            'phone': member.member.phone,
            'dob': _age(member.member.dob),
            'gender': member.member.gender,
        })
    return members_data


def handle_trip_member(action, trip_id, user_id):
    user = Owner.objects.get(id=user_id)
    trip = Trip.objects.get(TripID=trip_id)
    members = TripMember.objects.filter(TripID=trip, member=user)
    if len(members) > 0:
        if action == 'confirm':
            members[0].Approve = 1
            members[0].save()
        elif action == 'delete':
            members[0].delete()
        return True, {"user": members[0].member.username if action == 'confirm' else user.username}, 200
    return False, {"message": "User not found"}, 404


def trip_update_action(data):
    trip = Trip.objects.get(TripID=data['id'])
    if data['type'] == 'Delete':
        trip.delete()
        return True, {"message": "Trip deleted successfully"}, 201
    if data['type'] == 'Update':
        trip.name = data['trip_name']
        trip.Location = data['address']
        trip.start_date = data['start_date']
        trip.propose_date = data['propose_date']
        trip.end_date = data['end_date']
        trip.Privacy = data['privacy']
        trip.Thana = Thana.objects.get(thana=data['thana'])
        trip.guide = data['guide']
        trip.save()
        return True, {"message": "Trip updated successfully"}, 201
    return False, {"message": "Invalid request"}, 400


def medication_list_payload(username):
    user = Owner.objects.get(username=username)
    medications = Medication.objects.filter(user=user)
    medications_data = []
    for med in medications:
        if datetime.now().date() < med.meds_start_date or datetime.now().date() > med.meds_end_date:
            continue
        med_times = []
        if med.morning:
            med_times.append('Morning')
        if med.noon:
            med_times.append('Noon')
        if med.night:
            med_times.append('Night')
        medications_data.append({
            'id': med.medication_id,
            'name': med.med_name,
            'dosage': med.dose,
            'note': med.note,
            'after': med.after,
            'times': med_times,
            'image': med.img.url if med.img else 'media/d.png',
        })
    return medications_data


def medication_create_action(data, image_file):
    user = Owner.objects.get(username=data['user'])
    med = Medication.objects.create(
        user=user,
        img=image_file,
        med_name=data['name'],
        note=data['note'],
        dose=data['dosage'],
        morning=data['morning'],
        noon=data['noon'],
        night=data['night'],
        after=data['after'],
        meds_start_date=data['start_date'],
        meds_end_date=data['end_date'],
    )
    med.save()
    return {"message": "Medication created successfully"}


def done_action(data):
    user = Owner.objects.get(username=data['username'])
    if data['type'] == 'done':
        done = DoneMed.objects.create(user=user, done_date=data['date'], done_time=data['time'])
        done.save()
    else:
        done = DoneMed.objects.filter(user=user, done_date=data['date'], done_time=data['time'])
        if len(done) > 0:
            done[0].delete()
    return {"message": "Done successfully"}


def done_get(username, date, time_value):
    user = Owner.objects.get(username=username)
    done = DoneMed.objects.filter(user=user, done_date=date, done_time=time_value)
    return {"done": "1" if len(done) > 0 else "0"}


def medtime_get(username):
    user = Owner.objects.get(username=username)
    if MedAlert.objects.filter(userid=user).exists():
        time_obj = MedAlert.objects.get(userid=user)
        return {"night": time_obj.night, "morning": time_obj.morning, "noon": time_obj.noon, "gap": time_obj.interval}
    return {"night": "20:00", "morning": "08:00", "noon": "14:00", "gap": "30"}


def medtime_post(data):
    user = Owner.objects.get(username=data['username'])
    if MedAlert.objects.filter(userid=user).exists():
        time_obj = MedAlert.objects.get(userid=user)
        time_obj.night = data['night']
        time_obj.morning = data['morning']
        time_obj.noon = data['noon']
        time_obj.interval = data['gap']
        time_obj.save()
        return {"message": "Time updated successfully"}
    time_obj = MedAlert.objects.create(userid=user, night=data['night'], morning=data['morning'], noon=data['noon'], interval=data['gap'])
    time_obj.save()
    return {"message": "Time created successfully"}


def _age(dob):
    today = datetime.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))