from functools import wraps

from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from knowledge_base.models import Post


def author_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        post_id = kwargs.get("post_id")
        post = get_object_or_404(Post, id=post_id)

        if request.user != post.author and not request.user.is_superuser:
            raise PermissionDenied

        return view_func(request, *args, **kwargs)

    return _wrapped_view
