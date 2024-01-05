from django.urls import path 
from . import views
urlpatterns = [
    path('welcome to Elastic Search/',views.welcomeElasticSearch),
]
