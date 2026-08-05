

import logging
from typing import List, Dict, Any
from django.db import connection
from django.db.models import Count, Q
from django.utils import timezone
from api.models import Owner, Blog, Friend, CommunityGroup, Walk, Trip, Upvote, Comment
from api.ai_client import AIEmbeddingClient

logger = logging.getLogger(__name__)


class NostalgiaRecommenderEngine:
    """PostgreSQL Recommendation Engine for Nostalgia Platform"""

    def __init__(self):
        self.ai_client = AIEmbeddingClient()

    def get_recommended_feed(self, username: str, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Rank user feed posts using PostgreSQL time-decay scoring, interaction counts,
        and vector similarity if AI microservice is active.
        """
        try:
            from api.models import User
            user = Owner.objects.filter(username=username).first() or User.objects.filter(username=username).first()
            if not user:
                return self._get_fallback_feed(limit)

                                                              
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        b.blogid,
                        b.content,
                        b.post_date,
                        b.post_time,
                        b.author_id,
                        COUNT(DISTINCT u.id) as upvote_count,
                        COUNT(DISTINCT c.cmnt_id) as comment_count,
                        EXP(-0.03 * GREATEST(0, EXTRACT(EPOCH FROM (NOW() - (b.post_date + COALESCE(b.post_time, '00:00:00'::time)))) / 86400.0)) as time_decay_score
                    FROM api_blog b
                    LEFT JOIN api_upvote u ON u.blogid_id = b.blogid
                    LEFT JOIN api_comment c ON c.blogid_id = b.blogid
                    GROUP BY b.blogid, b.content, b.post_date, b.post_time, b.author_id
                    ORDER BY ( (COUNT(DISTINCT u.id) * 3.0 + COUNT(DISTINCT c.cmnt_id) * 2.0 + 1.0) * 
                               EXP(-0.03 * GREATEST(0, EXTRACT(EPOCH FROM (NOW() - (b.post_date + COALESCE(b.post_time, '00:00:00'::time)))) / 86400.0)) ) DESC
                    LIMIT %s
                """, [limit])
                rows = cursor.fetchall()

            post_ids = [r[0] for r in rows]
            blogs = Blog.objects.filter(blogid__in=post_ids).select_related('author', 'author__thana')

            result = []
            for blog in blogs:
                row_data = next((r for r in rows if r[0] == blog.blogid), None)
                score = float(row_data[7]) if row_data else 1.0
                upvote_count = row_data[5] if row_data else 0
                is_upvoted = 1 if Upvote.objects.filter(blogid=blog, Username__username=username).exists() else 0

                result.append({
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
                    'upvote': upvote_count,
                    'is_upvoted': is_upvoted,
                    'comment_count': row_data[6] if row_data else 0,
                    'recommendation_score': round(score, 4),
                    'recommendation_reason': 'Trending in your network'
                })

            return result

        except Exception as e:
            logger.error(f"Error computing recommended feed: {e}")
            return self._get_fallback_feed(limit)

    def get_recommended_friends(self, username: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Recommend friends / walking buddies based on:
        1. Same Thana / District location
        2. Walk style matching (Morning / Evening walk)
        3. Vector similarity via AI Microservice
        """
        try:
            from api.models import User
            user = Owner.objects.filter(username=username).first() or User.objects.filter(username=username).first()
            if not user:
                return []

                                                                   
            friends1 = Friend.objects.filter(user1=user).values_list('user2_id', flat=True)
            friends2 = Friend.objects.filter(user2=user).values_list('user1_id', flat=True)
            excluded_ids = set(friends1).union(set(friends2)).union({user.id})

                                                                         
            candidates = Owner.objects.exclude(id__in=excluded_ids).select_related('thana', 'thana__district')[:30]

                                                                       
            target_user_vec = []
            if self.ai_client.is_service_available():
                target_user_vec = self.ai_client.get_user_embedding({
                    'username': user.username,
                    'thana': user.thana.thana if user.thana else '',
                    'walk_type': user.walk_type,
                    'gender': user.gender
                })

            scored_candidates = []
            for candidate in candidates:
                base_score = 0.0

                                      
                if user.thana and candidate.thana and candidate.thana.id == user.thana.id:
                    base_score += 0.4
                elif user.thana and candidate.thana and candidate.thana.district_id == user.thana.district_id:
                    base_score += 0.2

                                        
                if user.walk_type and candidate.walk_type and candidate.walk_type == user.walk_type:
                    base_score += 0.3

                                         
                if target_user_vec and self.ai_client.is_service_available():
                    cand_vec = self.ai_client.get_user_embedding({
                        'username': candidate.username,
                        'thana': candidate.thana.thana if candidate.thana else '',
                        'walk_type': candidate.walk_type,
                        'gender': candidate.gender
                    })
                    vec_sim = self.ai_client.compute_similarity(target_user_vec, cand_vec)
                    base_score += float(vec_sim) * 0.3

                scored_candidates.append((candidate, base_score))

                                                  
            scored_candidates.sort(key=lambda x: x[1], reverse=True)

            return [
                {
                    'id': cand.id,
                    'username': cand.username,
                    'first_name': cand.first_name,
                    'last_name': cand.last_name,
                    'thana': cand.thana.thana if cand.thana else '',
                    'district': cand.thana.district.district if cand.thana and cand.thana.district else '',
                    'walk_type': cand.walk_type,
                    'gender': cand.gender,
                    'p_image': cand.p_image.url if cand.p_image else '/media/image/download_lX6bjA6.jpeg',
                    'pp': cand.p_image.url if cand.p_image else '/media/image/download_lX6bjA6.jpeg',
                    'score': round(score, 4),
                    'reason': 'Matches location & walking preferences' if score > 0.4 else 'Suggested senior friend'
                }
                for cand, score in scored_candidates[:limit]
            ]

        except Exception as e:
            logger.error(f"Error in friend recommendations: {e}")
            return []

    def _get_fallback_feed(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Fallback timeline feed if raw SQL query fails."""
        blogs = Blog.objects.select_related('author', 'author__thana').order_by('-post_date', '-post_time')[:limit]
        return [
            {
                'id': b.blogid,
                'blogid': b.blogid,
                'content': b.content,
                'post_date': str(b.post_date),
                'post_time': str(b.post_time) if b.post_time else '',
                'author': b.author.username,
                'author_first_name': b.author.first_name,
                'author_last_name': b.author.last_name,
                'author_img': b.author.p_image.url if b.author.p_image else "/media/image/download_lsX6bjA6.jpeg",
                'blog_img': b.blog_img.url if b.blog_img else None,
                'author_thana': b.author.thana.thana if b.author.thana else '',
                'upvote': 0,
                'is_upvoted': 0,
                'comment_count': 0,
                'recommendation_score': 1.0,
                'recommendation_reason': 'Recent post'
            }
            for b in blogs
        ]


                           
recommender_engine = NostalgiaRecommenderEngine()
