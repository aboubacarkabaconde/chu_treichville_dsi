# chu_treichville/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('consultations/', include('apps.consultations.urls')),  # ← Ajoute cette ligne
    path('urgences/', include('apps.urgences.urls')),            # ← Ajoute cette ligne
    path('accouchements/', include('apps.accouchements.urls')),  # ← Ajouter cette ligne
    path('cpn/', include('apps.cpn.urls')),  # ← Ajoute cette ligne
]