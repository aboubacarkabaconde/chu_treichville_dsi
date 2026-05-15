# apps/accouchements/urls.py

from django.urls import path
from . import views

app_name = 'accouchements'

urlpatterns = [
    path('', views.accouchement_list, name='list'),
    path('creer/', views.accouchement_create, name='create'),  # ← 'create' pas 'create_complete'
    path('<int:pk>/', views.accouchement_detail, name='detail'),
    path('<int:pk>/pdf/', views.accouchement_pdf, name='pdf'),
    path('<int:pk>/modifier/', views.accouchement_update, name='update'),
    path('<int:pk>/supprimer/', views.accouchement_delete, name='delete'),
]