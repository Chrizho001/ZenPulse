"""
URL configuration for GymFreak project.
"""

import os
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# ✅ Auto-create superuser only in production and only once
if os.environ.get("CREATE_SUPERUSER", "false").lower() == "true":
    from django.contrib.auth import get_user_model

    User = get_user_model()
    if not User.objects.filter(email="chrisfriday033@gmail.com").exists():
        User.objects.create_superuser(
            email="chrisfriday033@gmail.com",
            password="christopher",
            first_name="Chris",
            last_name="Friday",
        )

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("accounts.urls")),
    path("api/", include("Fitness.urls")),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

# ✅ Serve static and media files in production
if settings.DEBUG is False:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
