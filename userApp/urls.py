from django.urls import path
from . import views
urlpatterns = [
    path('welcomeUser/',views.welcomeUser),
    path('search/query=<str:query>', views.search_view, name='search_view'),
]