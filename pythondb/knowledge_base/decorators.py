from functools import wraps

from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from knowledge_base.models import Post


def author_required(view_func):
    @wraps(view_func)
    def _wrapped_view(self_or_request, *args, **kwargs):
        if isinstance(self_or_request, type) or hasattr(
            self_or_request, "user"
        ):
            request = self_or_request
        else:
            request = self_or_request.request

        post_id = kwargs.get("pk", kwargs.get("post_id"))
        post = get_object_or_404(Post, id=post_id)

        if request.user != post.author and not request.user.is_superuser:
            raise PermissionDenied(
                "You do not have permission to edit or delete this post."
            )

        return view_func(self_or_request, *args, **kwargs)

    return _wrapped_view
