from django.urls import path 
from . import views
urlpatterns = [
    path('welcomeModerator/',views.welcomeModerator),
]