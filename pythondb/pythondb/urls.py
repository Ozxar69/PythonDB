from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path("auth/", include("users.urls")),
    path("auth/", include("django.contrib.auth.urls")),
    path("chat/", include("gpt.urls")),
    path("", include("knowledge_base.urls")),
    path("api/", include("djoser.urls")),
    path("api/", include("djoser.urls.jwt")),
]
