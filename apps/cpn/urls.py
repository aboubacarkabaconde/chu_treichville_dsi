from django.urls import path
from . import views

app_name = 'cpn'

urlpatterns = [
    path('', views.cpn_list, name='list'),
    path('creer/', views.cpn_create, name='create'),
    path('<int:pk>/', views.cpn_detail, name='detail'),
    path('<int:pk>/pdf/', views.cpn_pdf, name='pdf'),
    path('<int:pk>/modifier/', views.cpn_update, name='update'),
    path('<int:pk>/supprimer/', views.cpn_delete, name='delete'),
]
