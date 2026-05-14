# apps/core/urls.py

from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('rapports/', views.rapports_list, name='rapports_list'),
    path('update-statut/<int:pk>/<str:type_rapport>/', views.update_rapport_statut, name='update_statut'),
]