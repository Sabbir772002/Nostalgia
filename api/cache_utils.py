import logging
from django.core.cache import cache

logger = logging.getLogger(__name__)

DEFAULT_CACHE_TIMEOUT = 60  # 60 seconds

def get_cached_or_set(key, fetch_function, timeout=DEFAULT_CACHE_TIMEOUT):
    """
    Attempts to retrieve a value from Redis cache by key.
    On cache miss, executes fetch_function, stores result in cache, and returns it.
    """
    try:
        cached_val = cache.get(key)
        if cached_val is not None:
            logger.debug(f"[CACHE HIT] {key}")
            return cached_val
    except Exception as e:
        logger.warning(f"[CACHE READ ERROR] {key}: {e}")

    # Cache miss or error
    logger.debug(f"[CACHE MISS] {key}")
    fresh_val = fetch_function()
    if fresh_val is not None:
        try:
            cache.set(key, fresh_val, timeout=timeout)
        except Exception as e:
            logger.warning(f"[CACHE WRITE ERROR] {key}: {e}")
    return fresh_val

def clear_cache_pattern(pattern):
    """
    Clears cache keys matching pattern if supported by backend, or clears all default cache.
    """
    try:
        if hasattr(cache, 'delete_pattern'):
            cache.delete_pattern(pattern)
        else:
            cache.clear()
        logger.info(f"[CACHE CLEAR] Pattern: {pattern}")
    except Exception as e:
        logger.warning(f"[CACHE CLEAR ERROR] Pattern {pattern}: {e}")
        try:
            cache.clear()
        except Exception:
            pass

def invalidate_feed_cache():
    """
    Invalidates all timeline, feed, and friend suggestion caches.
    """
    clear_cache_pattern("*htimeline*")
    clear_cache_pattern("*feed*")
    clear_cache_pattern("*friend_sugg*")

def invalidate_post_cache(post_id=None):
    """
    Invalidates caches associated with a specific post or all feeds.
    """
    if post_id:
        clear_cache_pattern(f"*blog_detail_{post_id}*")
        clear_cache_pattern(f"*comments_{post_id}*")
    invalidate_feed_cache()
