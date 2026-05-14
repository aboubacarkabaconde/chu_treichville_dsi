# apps/urgences/urls.py

from django.urls import path
from . import views

app_name = 'urgences'

urlpatterns = [
    path('', views.urgence_list, name='list'),
    path('creer/', views.urgence_create_complete, name='create_complete'),
    path('<int:pk>/pdf/', views.urgence_pdf, name='pdf'),
    path('<int:pk>/supprimer/', views.urgence_delete, name='delete'),
]