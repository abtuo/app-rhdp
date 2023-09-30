# myapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search_person, name='search_person'),
]
