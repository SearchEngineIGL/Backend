from django.urls import path 
from . import views
urlpatterns = [
    path('welcomeAdmin/',views.welcomeAdmin),
    path('add-moderator/',views.create_moderator),
    path('moderators/',views.list_of_moderators),
    path('modify-moderator/<int:id>',views.MAJ_moderator),
    path('delete-moderator/<int:id>',views.Delete_moderator),
]
