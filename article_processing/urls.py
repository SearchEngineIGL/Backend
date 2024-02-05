from django.urls import path 
from . import views
urlpatterns = [
    path('welcome to Elastic Search/',views.welcomeElasticSearch),
    # path('test/', views.search_view, name='search_view'),

]
