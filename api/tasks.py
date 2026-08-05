from django_tasks import task
from django.core.mail import send_mail
from django.db import transaction
import logging

logger = logging.getLogger(__name__)


@task(queue_name="emails")
def send_welcome_email(user_id: int):
    """Send welcome email to a newly registered user."""
    from api.models import Owner
    try:
        user = Owner.objects.get(id=user_id)
        if user.email:
            send_mail(
                subject="Welcome to Nostalgia!",
                message="Thanks for joining our community.",
                from_email=None,
                recipient_list=[user.email],
                fail_silently=True,
            )
            return f"Email sent to {user.email}"
    except Exception as e:
        logger.error(f"Error sending welcome email to user {user_id}: {e}")
    return f"Failed to send email to user {user_id}"


@task(queue_name="ai_processing")
def generate_user_vector_task(user_id: int):
    """Generate and save 384-d embedding vector for a user profile."""
    from api.models import Owner
    try:
        user = Owner.objects.get(id=user_id)
        vec = user.generate_vector()
        if vec:
            user.save(update_fields=['vector_embedding'])
            return f"User vector generated for user {user_id}"
    except Exception as e:
        logger.error(f"Error in generate_user_vector_task for user {user_id}: {e}")
    return f"Failed user vector task for {user_id}"


@task(queue_name="ai_processing")
def generate_post_vector_task(post_id: int):
    """Generate and save 384-d embedding vector for a blog post."""
    from api.models import Blog
    try:
        blog = Blog.objects.get(blogid=post_id)
        vec = blog.generate_vector()
        if vec:
            blog.save(update_fields=['vector_embedding'])
            return f"Post vector generated for blog {post_id}"
    except Exception as e:
        logger.error(f"Error in generate_post_vector_task for blog {post_id}: {e}")
    return f"Failed post vector task for {post_id}"


@task(queue_name="ai_processing")
def generate_group_vector_task(group_username: str):
    """Generate and save 384-d embedding vector for a CommunityGroup."""
    from api.models import CommunityGroup
    try:
        group = CommunityGroup.objects.get(G_username=group_username)
        vec = group.generate_vector()
        if vec:
            group.save(update_fields=['vector_embedding'])
            return f"Group vector generated for {group_username}"
    except Exception as e:
        logger.error(f"Error in generate_group_vector_task for group {group_username}: {e}")
    return f"Failed group vector task for {group_username}"


@task(queue_name="ai_processing")
def generate_trip_vector_task(trip_id: int):
    """Generate and save 384-d embedding vector for a Trip."""
    from api.models import Trip
    try:
        trip = Trip.objects.get(TripID=trip_id)
        vec = trip.generate_vector()
        if vec:
            trip.save(update_fields=['vector_embedding'])
            return f"Trip vector generated for trip {trip_id}"
    except Exception as e:
        logger.error(f"Error in generate_trip_vector_task for trip {trip_id}: {e}")
    return f"Failed trip vector task for {trip_id}"


@task(queue_name="ai_processing")
def generate_walk_vector_task(walk_id: int):
    """Generate and save 384-d embedding vector for a Walk."""
    from api.models import Walk
    try:
        walk = Walk.objects.get(walk_id=walk_id)
        vec = walk.generate_vector()
        if vec:
            walk.save(update_fields=['vector_embedding'])
            return f"Walk vector generated for walk {walk_id}"
    except Exception as e:
        logger.error(f"Error in generate_walk_vector_task for walk {walk_id}: {e}")
    return f"Failed walk vector task for {walk_id}"
