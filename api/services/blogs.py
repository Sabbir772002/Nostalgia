from datetime import datetime

from django.utils import timezone

from api.cache_utils import get_cached_or_set, invalidate_feed_cache, invalidate_post_cache
from api.models import Blog, BlogView, Comment, Owner, Upvote


DEFAULT_PROFILE_IMAGE = "/media/image/download_lsX6bjA6.jpeg"


def list_blogs(username, page=1, page_size=10):
    user = Owner.objects.filter(username=username).first() if username else None
    queryset = Blog.objects.all().select_related('author').order_by('-post_date', '-post_time')
    total_count = queryset.count()
    start = (page - 1) * page_size
    end = start + page_size
    blogs_slice = queryset[start:end]

    blogs_data = []
    for blog in blogs_slice:
        author_user = blog.author
        is_upvoted = 1 if user and Upvote.objects.filter(blogid=blog, Username=user).exists() else 0
        blogs_data.append({
            'id': blog.blogid,
            'blogid': blog.blogid,
            'author': author_user.username,
            'author_first_name': author_user.first_name,
            'author_last_name': author_user.last_name,
            'author_img': author_user.p_image.url if author_user.p_image else DEFAULT_PROFILE_IMAGE,
            'content': blog.content,
            'post_date': str(blog.post_date),
            'post_time': str(blog.post_time) if blog.post_time else '',
            'blog_img': blog.blog_img.url if blog.blog_img else None,
            'upvote': Upvote.objects.filter(blogid=blog).count(),
            'is_upvoted': is_upvoted,
        })

    return {
        "posts": blogs_data,
        "has_more": end < total_count,
        "page": page,
        "page_size": page_size,
        "total": total_count,
    }


def timeline_posts(username, page=1, page_size=10):
    user = Owner.objects.filter(username=username).first()
    try:
        from api.recommender_service import DecoupledRecommenderService

        recommender = DecoupledRecommenderService()
        rec_blogs = recommender.get_recommended_posts(username=username, limit=100)
    except Exception:
        rec_blogs = []

    if rec_blogs:
        all_posts = rec_blogs
    else:
        queryset = Blog.objects.all().select_related('author').order_by('-post_date', '-post_time')
        all_posts = []
        for blog in queryset:
            upvote_count = Upvote.objects.filter(blogid=blog).count()
            is_upvoted = 1 if user and Upvote.objects.filter(blogid=blog, Username=user).exists() else 0
            all_posts.append({
                'id': blog.blogid,
                'blogid': blog.blogid,
                'author': blog.author.username,
                'author_first_name': blog.author.first_name,
                'author_last_name': blog.author.last_name,
                'author_img': blog.author.p_image.url if blog.author.p_image else DEFAULT_PROFILE_IMAGE,
                'content': blog.content,
                'post_date': str(blog.post_date),
                'post_time': str(blog.post_time) if blog.post_time else '',
                'blog_img': blog.blog_img.url if blog.blog_img else None,
                'upvote': upvote_count,
                'is_upvoted': is_upvoted,
            })

    total_count = len(all_posts)
    start = (page - 1) * page_size
    end = start + page_size
    page_posts = all_posts[start:end]

    return {
        "posts": page_posts,
        "has_more": end < total_count,
        "page": page,
        "page_size": page_size,
        "total": total_count,
    }


def toggle_upvote(blog_id, username):
    blog = Blog.objects.get(blogid=blog_id)
    owner = Owner.objects.get(username=username)

    existing_upvotes = Upvote.objects.filter(Username=owner, blogid=blog)
    if existing_upvotes.exists():
        existing_upvotes.delete()
        is_upvoted = 0
    else:
        Upvote.objects.create(Username=owner, blogid=blog)
        is_upvoted = 1

    upvote_count = Upvote.objects.filter(blogid=blog).count()
    invalidate_post_cache(blog.blogid)

    return {
        'id': blog.blogid,
        'blogid': blog.blogid,
        'author': owner.username,
        'author_img': owner.p_image.url if owner.p_image else DEFAULT_PROFILE_IMAGE,
        'content': blog.content,
        'post_date': str(blog.post_date),
        'post_time': str(blog.post_time) if blog.post_time else '',
        'blog_img': blog.blog_img.url if blog.blog_img else None,
        'upvote': upvote_count,
        'is_upvoted': is_upvoted,
    }


def single_user_blogs(username):
    queryset = Blog.objects.filter(author=Owner.objects.get(username=username).id).order_by('-post_date', '-post_time')
    blogs_data = []
    for blog in queryset:
        blog_data = {
            'id': blog.blogid,
            'author': Owner.objects.get(username=blog.author).username,
            'author_img': Owner.objects.get(username=blog.author).p_image.url if Owner.objects.get(username=blog.author).p_image else DEFAULT_PROFILE_IMAGE,
            'content': blog.content,
            'post_date': blog.post_date,
            'post_time': blog.post_time,
            'blog_img': blog.blog_img.url if blog.blog_img else None,
        }
        blogs_data.append(blog_data)
    return blogs_data


def create_blog(username, data):
    user = Owner.objects.get(username=username)
    blog_img = data.get('blog_img')
    if blog_img is not None:
        blog = Blog.objects.create(author=user, content=data['content'], post_date=datetime.now().date(), post_time=datetime.now().time(), blog_img=blog_img)
    else:
        blog = Blog.objects.create(author=user, content=data['content'], post_date=data['post_date'], post_time=data['post_time'])

    invalidate_feed_cache()
    return blog


def record_blog_view(username, blog_id, view_duration):
    user = Owner.objects.filter(username=username).first()
    blog = Blog.objects.filter(blogid=blog_id).first()
    if not user or not blog:
        return None, None

    bv = BlogView.objects.create(
        user=user,
        blog=blog,
        view_duration=view_duration,
        created_at=timezone.now(),
    )

    if view_duration >= 3.0:
        try:
            user.generate_vector_async()
        except Exception:
            pass

    return bv, blog


def blog_detail(username, blog_id):
    blog = Blog.objects.filter(blogid=blog_id).select_related('author', 'author__thana').first()
    if not blog:
        return None

    user = Owner.objects.filter(username=username).first() if username else None
    upvote_count = Upvote.objects.filter(blogid=blog).count()
    is_upvoted = 1 if user and Upvote.objects.filter(blogid=blog, Username=user).exists() else 0

    comments_qs = Comment.objects.filter(blogid=blog).select_related('username').order_by('time')
    comments_list = []
    for c in comments_qs:
        author_img = c.username.p_image.url if c.username.p_image else DEFAULT_PROFILE_IMAGE
        comments_list.append({
            'id': c.cmnt_id,
            'author': c.username.username,
            'author_first_name': c.username.first_name,
            'author_last_name': c.username.last_name,
            'author_img': author_img,
            'content': c.comment,
            'time': c.time.strftime('%b %d, %Y %H:%M') if hasattr(c.time, 'strftime') else str(c.time),
        })

    author_img = blog.author.p_image.url if blog.author.p_image else DEFAULT_PROFILE_IMAGE
    return {
        'id': blog.blogid,
        'blogid': blog.blogid,
        'content': blog.content,
        'post_date': str(blog.post_date),
        'post_time': str(blog.post_time) if blog.post_time else '',
        'author': blog.author.username,
        'author_first_name': blog.author.first_name,
        'author_last_name': blog.author.last_name,
        'author_img': author_img,
        'blog_img': blog.blog_img.url if blog.blog_img else None,
        'author_thana': blog.author.thana.thana if blog.author.thana else '',
        'upvote': upvote_count,
        'is_upvoted': is_upvoted,
        'comment_count': len(comments_list),
        'comments': comments_list,
    }


def list_comments(blog_id):
    blog = Blog.objects.get(blogid=blog_id)
    queryset = Comment.objects.filter(blogid=blog).order_by('-time')
    blogs_data = []
    for comment in queryset:
        blog_data = {
            'id': comment.cmnt_id,
            'author': comment.username.username,
            'author_img': comment.username.p_image.url if comment.username.p_image else DEFAULT_PROFILE_IMAGE,
            'content': comment.comment,
            'time': "in " + comment.time.strftime('%d-%m-%Y') + " at " + comment.time.strftime('%H:%M'),
            'blog': comment.blogid.blogid,
        }
        blogs_data.append(blog_data)
    return blogs_data


def create_comment(author_username, blog_id, content):
    user = Owner.objects.get(username=author_username)
    blog = Blog.objects.get(blogid=blog_id)
    comment = Comment.objects.create(
        blogid=blog,
        username=user,
        comment=content,
        time=timezone.now(),
    )
    invalidate_post_cache(blog.blogid)
    author_img = user.p_image.url if user.p_image else DEFAULT_PROFILE_IMAGE
    return comment, {
        "message": "Comment created successfully",
        "id": comment.cmnt_id,
        "author": user.username,
        "author_first_name": user.first_name,
        "author_last_name": user.last_name,
        "author_img": author_img,
        "content": comment.comment,
        "time": "Just now",
    }