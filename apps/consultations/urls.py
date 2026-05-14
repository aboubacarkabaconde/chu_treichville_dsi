# apps/consultations/urls.py

from django.urls import path
from . import views

app_name = 'consultations'

urlpatterns = [
    path('', views.consultation_list, name='list'),
    path('creer/', views.consultation_create_complete, name='create_complete'),
    path('<int:pk>/', views.consultation_detail_full, name='detail'),
    path('<int:pk>/pdf/', views.consultation_pdf, name='pdf'),
    path('<int:pk>/modifier/', views.consultation_update, name='update'),
    path('<int:pk>/supprimer/', views.consultation_delete, name='delete'),
]