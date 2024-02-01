from django.urls import path 
from . import views
urlpatterns = [
    path('welcomeModerator/',views.welcomeModerator),
    path('settings/',views.ModeratorSettings),

    path('articles/',views.display_articles_for_correction),
    path('article/<int:article_id>',views.CorrectionArticle),

    path('delete/<int:article_id>',views.deleteArticle),
    


 ]
