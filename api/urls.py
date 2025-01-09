from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
import os

urlpatterns = [
    path('', views.generate_video_link),
]
