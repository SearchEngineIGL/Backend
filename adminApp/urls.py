from django.urls import path 
from . import views
from .views import *
urlpatterns = [
    path('welcomeAdmin/',views.welcomeAdmin),
    path('add-moderator/',views.create_moderator,name='create_moderator'),
    path('moderators/',views.list_of_moderators),
    path('modify-moderator/<int:id>',views.MAJ_moderator),
    path('delete-moderator/<int:id>',views.Delete_moderator),
    path('settings/',views.AdminSettings),
    path('articles/',views.get_articles,name='get_articles'),
   
]