# myapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search_person, name='search_person'),
    path('add/', views.add_person, name='add_person'),
    path('all/', views.view_all_persons, name='view_all_persons'),
]