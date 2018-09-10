from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from core import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'ngo', views.NgoViewSet)
router.register(r'ngo_verification', views.Ngo_VerificationViewSet)
router.register(r'ngo_detail', views.Ngo_DetailViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    url(r'^', include(router.urls))
]