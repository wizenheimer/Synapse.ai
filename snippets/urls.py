from django.urls import path, include
from rest_framework.routers import DefaultRouter
from snippets import views


router = DefaultRouter()
router.register(r"", views.SnippetViewSet, basename="snippet")


urlpatterns = [
    path("", include(router.urls)),
]
