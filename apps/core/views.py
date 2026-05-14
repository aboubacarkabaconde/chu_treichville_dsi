# apps/core/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from apps.consultations.models import Consultation
from apps.urgences.models import Urgence


def login_view(request):
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user:
            login(request, user)
            return redirect('core:dashboard')
        else:
            messages.error(request, "Identifiants incorrects")
    
    return render(request, 'core/login.html')


def logout_view(request):
    logout(request)
    return redirect('core:login')


@login_required
def dashboard(request):
    """Tableau de bord principal"""
    from apps.consultations.models import Consultation
    from apps.urgences.models import Urgence
    
    # Statistiques
    consultations = Consultation.objects.all()
    urgences = Urgence.objects.all()
    
    total_consultations = consultations.count()
    total_urgences = urgences.count()
    total_rapports = total_consultations + total_urgences
    
    # Derniers rapports (10 derniers)
    derniers_rapports = []
    
    for c in consultations.order_by('-created_at')[:5]:
        c.type_rapport = 'consultation'
        c.type_label = 'Consultation'
        c.type_icon = 'fa-notes-medical'
        c.type_color = 'primary'
        c.service_display = c.service_nom
        derniers_rapports.append(c)
    
    for u in urgences.order_by('-created_at')[:5]:
        u.type_rapport = 'urgence'
        u.type_label = 'Urgences'
        u.type_icon = 'fa-ambulance'
        u.type_color = 'danger'
        u.service_display = u.service_nom
        derniers_rapports.append(u)
    
    # Trier par date de création (plus récent en premier)
    derniers_rapports.sort(key=lambda x: x.created_at, reverse=True)
    derniers_rapports = derniers_rapports[:10]
    
    context = {
        'total_rapports': total_rapports,
        'total_consultations': total_consultations,
        'total_urgences': total_urgences,
        'total_services': 33,
        'derniers_rapports': derniers_rapports,
    }
    return render(request, 'core/dashboard.html', context)


@login_required
def rapports_list(request):
    """Liste de tous les rapports"""
    from apps.consultations.models import Consultation
    from apps.urgences.models import Urgence
    
    consultations = Consultation.objects.all().order_by('-created_at')
    urgences = Urgence.objects.all().order_by('-created_at')
    
    context = {
        'consultations': consultations,
        'urgences': urgences,
    }
    return render(request, 'core/rapports_list.html', context)


@login_required
def update_rapport_statut(request, pk, type_rapport):
    """Mettre à jour le statut d'un rapport"""
    if type_rapport == 'consultation':
        rapport = Consultation.objects.get(pk=pk)
    else:
        rapport = Urgence.objects.get(pk=pk)
    
    if request.method == 'POST':
        nouveau_statut = request.POST.get('statut')
        if nouveau_statut in dict(rapport.STATUT_CHOICES):
            rapport.statut = nouveau_statut
            rapport.save()
            messages.success(request, f"Statut mis à jour : {rapport.get_statut_display()}")
    
    return redirect('core:dashboard')