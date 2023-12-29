from django.urls import path 
from . import views
urlpatterns = [
    path('welcomeUser/',views.welcomeUser),
    path('settings/',views.UserSettings),
]
