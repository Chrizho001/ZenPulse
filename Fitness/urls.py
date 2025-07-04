from django.urls import path
from .views import FitnessBlogDetailView, FitnessBlogListView, SessionCreateView

urlpatterns = [
    path("blog", FitnessBlogListView.as_view(), name="blog-list"),
    path("blog/<slug:slug>", FitnessBlogDetailView.as_view(), name='blog-detail'),
    path("sessions/", SessionCreateView.as_view(), name="create-session")
]