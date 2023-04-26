from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accounts import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r"accounts", views.ProfileViewSet, basename="profile_view_set")
router.register(r"team", views.TeamViewSet, basename="team_view_set")

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path("", include(router.urls)),
]
