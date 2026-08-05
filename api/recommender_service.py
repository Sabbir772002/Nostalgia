import logging
import numpy as np
from typing import List, Dict, Any
from django.db.models import Count, Q, F, Sum
from django.utils import timezone
from pgvector.django import CosineDistance

from api.models import Owner, Blog, Friend, CommunityGroup, Walk, Trip, Upvote, Comment
from api.ai_client import AIEmbeddingClient

logger = logging.getLogger(__name__)

                 
WEIGHT_UPVOTE = 3.0
WEIGHT_COMMENT = 2.0
WEIGHT_VIEW_TIME = 0.5
WEIGHT_AI_SIMILARITY = 10.0
WEIGHT_LOCATION_THANA = 0.4
WEIGHT_LOCATION_DISTRICT = 0.2
WEIGHT_WALK_TYPE = 0.3
WEIGHT_AI_FRIEND = 0.5
WEIGHT_GROUP_AI = 0.5
WEIGHT_TRIP_AI = 0.5
DEFAULT_BASE_SCORE = 0.5


def compute_batch_cosine_similarities(user_vec: List[float], candidate_vectors: List[List[float]]) -> List[float]:
    if not user_vec or not candidate_vectors:
        return [0.0] * len(candidate_vectors)

    try:
        u = np.array(user_vec, dtype=np.float32)
        u_norm = np.linalg.norm(u)
        if u_norm == 0:
            return [0.0] * len(candidate_vectors)
        u_normalized = u / u_norm

        P = np.array(candidate_vectors, dtype=np.float32)
        P_norms = np.linalg.norm(P, axis=1)
        P_norms[P_norms == 0] = 1e-9

        sims = np.dot(P, u_normalized) / P_norms
        sims = np.clip(sims, -1.0, 1.0)
        return sims.tolist()
    except Exception as e:
        logger.error(f"Error in compute_batch_cosine_similarities: {e}")
        return [0.0] * len(candidate_vectors)


class DecoupledRecommenderService:
    def __init__(self):
        self.ai_client = AIEmbeddingClient()

    def _get_user_vector(self, user: Owner) -> List[float]:
        if not user:
            return []
        vec = user.get_vector()
        if not vec:
            vec = user.generate_vector()
            if vec and user.pk:
                try:
                    user.save(update_fields=['vector_embedding'])
                except Exception:
                    pass
        return vec or []

    def get_recommended_posts(self, username: str, limit: int = 20) -> List[Dict[str, Any]]:
        try:
            from api.models import BlogView
            user = Owner.objects.filter(username=username).first()
            if not user:
                return []

            user_vec = self._get_user_vector(user)

            if user_vec and len(user_vec) == 384:
                try:
                    blogs = list(Blog.objects.select_related('author', 'author__thana').filter(
                        vector_embedding__isnull=False
                    ).annotate(
                        upvote_count=Count('upvote', distinct=True),
                        comment_count=Count('comment', distinct=True),
                        total_view_time=Sum('views__view_duration'),
                        distance=CosineDistance('vector_embedding', user_vec)
                    ).order_by('distance', '-post_date', '-post_time')[:limit * 2])
                except Exception as ex:
                    logger.warning(f"Native pgvector query fallback to ORM scan: {ex}")
                    blogs = []
            else:
                blogs = []

            if not blogs:
                blogs = list(Blog.objects.select_related('author', 'author__thana').annotate(
                    upvote_count=Count('upvote', distinct=True),
                    comment_count=Count('comment', distinct=True),
                    total_view_time=Sum('views__view_duration')
                ).order_by('-post_date', '-post_time')[:limit * 2])

            if not blogs:
                return []

            scored = []
            for blog in blogs:
                view_time = float(blog.total_view_time or 0.0)
                popularity = (blog.upvote_count * WEIGHT_UPVOTE) + (blog.comment_count * WEIGHT_COMMENT) + (view_time * WEIGHT_VIEW_TIME) + 1.0

                if hasattr(blog, 'distance') and blog.distance is not None:
                    sim_score = max(0.0, 1.0 - float(blog.distance))
                else:
                    blog_vec = blog.get_vector()
                    if user_vec and blog_vec and len(blog_vec) == 384:
                        sim_score = compute_batch_cosine_similarities(user_vec, [blog_vec])[0]
                    else:
                        sim_score = 0.0

                total_score = popularity + (sim_score * WEIGHT_AI_SIMILARITY)

                scored.append({
                    'id': blog.blogid,
                    'blogid': blog.blogid,
                    'content': blog.content,
                    'post_date': str(blog.post_date),
                    'post_time': str(blog.post_time) if blog.post_time else '',
                    'author': blog.author.username,
                    'author_first_name': blog.author.first_name,
                    'author_last_name': blog.author.last_name,
                    'author_img': blog.author.p_image.url if blog.author.p_image else "/media/image/download_lsX6bjA6.jpeg",
                    'blog_img': blog.blog_img.url if blog.blog_img else None,
                    'author_thana': blog.author.thana.thana if blog.author.thana else '',
                    'upvote': blog.upvote_count,
                    'is_upvoted': 1 if Upvote.objects.filter(blogid=blog, Username=user).exists() else 0,
                    'comment_count': blog.comment_count,
                    'recommendation_score': round(total_score, 4),
                    'recommendation_reason': 'AI matched your interests' if sim_score > 0.3 else 'Popular in community'
                })

            scored.sort(key=lambda x: x['recommendation_score'], reverse=True)
            return scored[:limit]

        except Exception as e:
            logger.error(f"Recommended posts error: {e}")
            return []

    def get_recommended_friends(self, username: str, limit: int = 10) -> List[Dict[str, Any]]:
        try:
            user = Owner.objects.filter(username=username).first()
            if not user:
                return []

            friends1 = Friend.objects.filter(user1=user).values_list('user2_id', flat=True)
            friends2 = Friend.objects.filter(user2=user).values_list('user1_id', flat=True)
            excluded = set(friends1) | set(friends2) | {user.id}

            user_vec = self._get_user_vector(user)
            candidates = list(Owner.objects.exclude(id__in=excluded).select_related('thana', 'thana__district')[:50])
            if not candidates:
                return []

            candidate_vectors = [cand.get_vector() or ([0.0] * 384) for cand in candidates]
            sim_scores = compute_batch_cosine_similarities(user_vec, candidate_vectors)

            scored = []
            for cand, sim in zip(candidates, sim_scores):
                score = 0.0
                if user.thana and cand.thana:
                    if cand.thana.id == user.thana.id:
                        score += WEIGHT_LOCATION_THANA
                    elif cand.thana.district_id == user.thana.district_id:
                        score += WEIGHT_LOCATION_DISTRICT

                if user.walk_type and cand.walk_type and cand.walk_type == user.walk_type:
                    score += WEIGHT_WALK_TYPE

                score += sim * WEIGHT_AI_FRIEND

                scored.append({
                    'id': cand.id,
                    'username': cand.username,
                    'first_name': cand.first_name,
                    'last_name': cand.last_name,
                    'thana': cand.thana.thana if cand.thana else '',
                    'district': cand.thana.district.district if (cand.thana and cand.thana.district) else '',
                    'walk_type': cand.walk_type or '',
                    'gender': cand.gender or '',
                    'p_image': cand.p_image.url if cand.p_image else '/media/image/download_lX6bjA6.jpeg',
                    'pp': cand.p_image.url if cand.p_image else '/media/image/download_lX6bjA6.jpeg',
                    'score': round(score, 4),
                    'reason': 'Matched location & AI profile' if score > 0.3 else 'Suggested based on common interests'
                })

            scored.sort(key=lambda x: x['score'], reverse=True)
            return scored[:limit]

        except Exception as e:
            logger.error(f"Friend recommendations error: {e}")
            return []

    def get_recommended_groups(self, username: str, limit: int = 10) -> List[Dict[str, Any]]:
        try:
            user = Owner.objects.filter(username=username).first()
            if not user:
                return []

            user_vec = self._get_user_vector(user)
            groups = list(CommunityGroup.objects.all()[:50])
            if not groups:
                return []

            group_vectors = [g.get_vector() or ([0.0] * 384) for g in groups]
            sim_scores = compute_batch_cosine_similarities(user_vec, group_vectors)

            scored = []
            for g, sim in zip(groups, sim_scores):
                base_score = DEFAULT_BASE_SCORE + (sim * WEIGHT_GROUP_AI)
                scored.append({
                    'id': g.G_username,
                    'name': g.G_name,
                    'username': g.G_username,
                    'topic': g.Topic,
                    'privacy': g.Privacy,
                    'img': g.img.url if g.img else '/media/image/download_lX6bjA6.jpeg',
                    'score': round(base_score, 4),
                    'reason': 'Matches your interests' if base_score > 0.6 else 'Popular group'
                })

            scored.sort(key=lambda x: x['score'], reverse=True)
            return scored[:limit]

        except Exception as e:
            logger.error(f"Group recommendations error: {e}")
            return []

    def get_recommended_trips(self, username: str, limit: int = 10) -> List[Dict[str, Any]]:
        try:
            user = Owner.objects.filter(username=username).first()
            if not user:
                return []

            user_vec = self._get_user_vector(user)
            trips = list(Trip.objects.select_related('Creator').all()[:50])
            if not trips:
                return []

            trip_vectors = [t.get_vector() or ([0.0] * 384) for t in trips]
            sim_scores = compute_batch_cosine_similarities(user_vec, trip_vectors)

            scored = []
            for t, sim in zip(trips, sim_scores):
                base_score = DEFAULT_BASE_SCORE + (sim * WEIGHT_TRIP_AI)
                scored.append({
                    'id': t.TripID,
                    'name': t.name,
                    'location': t.Location,
                    'creator': t.Creator.username if t.Creator else '',
                    'start_date': str(t.start_date) if t.start_date else '',
                    'score': round(base_score, 4),
                    'reason': 'AI matched your style' if base_score > 0.6 else 'Popular trip'
                })

            scored.sort(key=lambda x: x['score'], reverse=True)
            return scored[:limit]

        except Exception as e:
            logger.error(f"Trip recommendations error: {e}")
            return []

    def get_recommended_walks(self, username: str, limit: int = 10) -> List[Dict[str, Any]]:
        try:
            user = Owner.objects.filter(username=username).first()
            if not user:
                return []

            user_vec = self._get_user_vector(user)
            walks = list(Walk.objects.select_related('w_creator').all()[:50])
            if not walks:
                return []

            walk_vectors = [w.get_vector() or ([0.0] * 384) for w in walks]
            sim_scores = compute_batch_cosine_similarities(user_vec, walk_vectors)

            scored = []
            for w, sim in zip(walks, sim_scores):
                base_score = DEFAULT_BASE_SCORE + (sim * WEIGHT_TRIP_AI)
                scored.append({
                    'id': w.walk_id,
                    'name': w.walk_name,
                    'location': w.address,
                    'creator': w.w_creator.username if w.w_creator else '',
                    'date': str(w.walk_date) if w.walk_date else '',
                    'score': round(base_score, 4),
                    'reason': 'AI matched your interests' if base_score > 0.6 else 'Popular walk'
                })

            scored.sort(key=lambda x: x['score'], reverse=True)
            return scored[:limit]

        except Exception as e:
            logger.error(f"Walk recommendations error: {e}")
            return []


decoupled_recommender = DecoupledRecommenderService()