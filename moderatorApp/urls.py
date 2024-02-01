from django.urls import path 
from . import views
urlpatterns = [
    path('welcomeModerator/',views.welcomeModerator),
    path('settings/',views.ModeratorSettings),


    path('Articles/',views.display_articles_for_correction),
    path('correction/',views.CorrectionArticle)
   

 ]
