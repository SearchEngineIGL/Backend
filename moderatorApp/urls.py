from django.urls import path 
from . import views
urlpatterns = [
    path('welcomeModerator/',views.welcomeModerator),
    path('settings/',views.ModeratorSettings),
<<<<<<< HEAD
    path('articles/',views.display_articles_for_correction),
    path('article/<int:article_id>',views.CorrectionArticle),
=======
    path('Articles/',views.display_articles_for_correction),
    path('correction/',views.CorrectionArticle)
   
>>>>>>> e132ab81cb8060977185c1230e154597a0019696
 ]
