from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("blog/", include("blog.urls")),
    path("melon/", include("melon.urls")),
    path("health/", include("health.urls")),
    path("diary/", include("diary.urls")),
    path("api-auth/", include("rest_framework.urls")),
]
