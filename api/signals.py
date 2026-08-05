import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from api.models import (
    Upvote, Comment, Friend, WalkMember, TripMember, JoinEvent, Notification
)

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Upvote)
def create_upvote_notification(sender, instance, created, **kwargs):
    if created and instance.blogid and instance.Username:
        author = instance.blogid.author
        sender_user = instance.Username
        if author and sender_user and author.username != sender_user.username:
            try:
                Notification.objects.create(
                    noti_type="Upvote",
                    noti_msg="upvoted your blog",
                    noti_sender=sender_user,
                    noti_receiver=author,
                    noti_status="0",
                    noti_date=timezone.now().date(),
                    noti_time=timezone.now()
                )
            except Exception as e:
                logger.warning(f"Error creating upvote notification signal: {e}")


@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    if created and instance.blogid and instance.username:
        author = instance.blogid.author
        sender_user = instance.username
        if author and sender_user and author.username != sender_user.username:
            try:
                Notification.objects.create(
                    noti_type="Comment",
                    noti_msg="commented on your blog",
                    noti_sender=sender_user,
                    noti_receiver=author,
                    noti_status="0",
                    noti_date=timezone.now().date(),
                    noti_time=timezone.now()
                )
            except Exception as e:
                logger.warning(f"Error creating comment notification signal: {e}")


@receiver(post_save, sender=Friend)
def create_friend_notification(sender, instance, created, **kwargs):
    if created and instance.user1 and instance.user2 and instance.is_fnf == 0:
        try:
            Notification.objects.create(
                noti_type="Bondhu",
                noti_msg="sent you a friend request",
                noti_sender=instance.user1,
                noti_receiver=instance.user2,
                noti_status="0",
                noti_date=timezone.now().date(),
                noti_time=timezone.now()
            )
        except Exception as e:
            logger.warning(f"Error creating friend notification signal: {e}")


@receiver(post_save, sender=WalkMember)
def create_walk_member_notification(sender, instance, created, **kwargs):
    if created and instance.walk_id and instance.username:
        creator = instance.walk_id.w_creator
        sender_user = instance.username
        if creator and sender_user and creator.username != sender_user.username:
            try:
                Notification.objects.create(
                    noti_type="Walk",
                    noti_msg=f"requested to join your walk '{instance.walk_id.walk_name}'",
                    noti_sender=sender_user,
                    noti_receiver=creator,
                    noti_status="0",
                    noti_date=timezone.now().date(),
                    noti_time=timezone.now()
                )
            except Exception as e:
                logger.warning(f"Error creating walk notification signal: {e}")


@receiver(post_save, sender=TripMember)
def create_trip_member_notification(sender, instance, created, **kwargs):
    if created and instance.TripID and instance.member:
        creator = instance.TripID.Creator
        sender_user = instance.member
        if creator and sender_user and creator.username != sender_user.username:
            try:
                Notification.objects.create(
                    noti_type="Trip",
                    noti_msg=f"requested to join your trip '{instance.TripID.name}'",
                    noti_sender=sender_user,
                    noti_receiver=creator,
                    noti_status="0",
                    noti_date=timezone.now().date(),
                    noti_time=timezone.now()
                )
            except Exception as e:
                logger.warning(f"Error creating trip notification signal: {e}")


@receiver(post_save, sender=JoinEvent)
def create_join_event_notification(sender, instance, created, **kwargs):
    if created and instance.EventID and instance.Member:
        creator = instance.EventID.E_creator
        sender_user = instance.Member
        if creator and sender_user and creator.username != sender_user.username:
            try:
                Notification.objects.create(
                    noti_type="Event",
                    noti_msg=f"requested to join your event '{instance.EventID.Event_title}'",
                    noti_sender=sender_user,
                    noti_receiver=creator,
                    noti_status="0",
                    noti_date=timezone.now().date(),
                    noti_time=timezone.now()
                )
            except Exception as e:
                logger.warning(f"Error creating event notification signal: {e}")
