from django.contrib.auth.views import LogoutView
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path, include


router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),

    
]
