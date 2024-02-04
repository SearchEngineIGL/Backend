from django.urls import path
from . import views
urlpatterns = [
    path('welcomeUser/',views.welcomeUser),
    path('search/query=<str:query>', views.search_view, name='search_view'),
    path('article/<int:article_id>', views.ViewArticle),
    path('settings/',views.UserSettings),
    path('addfv/',views.addFav),
    path('rmfv/',views.rmvFav),
    path('favors/',views.getFavs),
    path('isfv/',views.isFav),
    path('homeArticles/',views.homeArticles),
]
