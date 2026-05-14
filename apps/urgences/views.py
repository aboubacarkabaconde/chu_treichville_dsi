# apps/urgences/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import Urgence, FrequentationUrgence, MorbiditeUrgence, CauseDecesUrgence
from .pdf_utils import generate_urgence_pdf


@login_required
def urgence_list(request):
    """Liste des rapports des urgences"""
    rapports = Urgence.objects.all().select_related('created_by')
    context = {'rapports': rapports}
    return render(request, 'urgences/list.html', context)


@login_required
def urgence_create_complete(request):
    """Formulaire complet des urgences"""
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                urgence = Urgence()
                urgence.service = None
                urgence.service_nom = request.POST.get('service_nom', 'Service des Urgences')
                urgence.mois = int(request.POST.get('mois', 1))
                urgence.annee = int(request.POST.get('annee', 2025))
                
                # Capacité d'accueil - Convertir en int
                urgence.nb_lits = int(request.POST.get('nb_lits', 0))
                urgence.nb_lits_fonctionnels = int(request.POST.get('nb_lits_fonctionnels', 0))
                urgence.nb_journees_theoriques = int(request.POST.get('nb_journees_theoriques', 0))
                urgence.nb_journees_realisees = int(request.POST.get('nb_journees_realisees', 0))
                urgence.delai_moyen_pec = float(request.POST.get('delai_moyen_pec', 0))
                
                # Assurances - Convertir en int
                urgence.assurance_cmu = int(request.POST.get('assurance_cmu', 0))
                urgence.assurance_privee = int(request.POST.get('assurance_privee', 0))
                
                # Signatures
                urgence.coordinateur_nom = request.POST.get('coordinateur_nom', '')
                urgence.coordinateur_prenom = request.POST.get('coordinateur_prenom', '')
                urgence.surveillant_nom = request.POST.get('surveillant_nom', '')
                urgence.surveillant_prenom = request.POST.get('surveillant_prenom', '')
                urgence.chef_service_nom = request.POST.get('chef_service_nom', '')
                urgence.chef_service_prenom = request.POST.get('chef_service_prenom', '')
                urgence.observations = request.POST.get('observations', '')
                urgence.created_by = request.user
                urgence.save()
                
                # Fréquentations - Convertir en int
                tranches = ['0-4', '5-9', '10-14', '15-19', '20-24', '25-49', '50+']
                sexes = ['M', 'F']
                
                for tranche in tranches:
                    for sexe in sexes:
                        try:
                            admis = int(request.POST.get(f'freq_{tranche}_{sexe}_admis', 0) or 0)
                            observes = int(request.POST.get(f'freq_{tranche}_{sexe}_observes', 0) or 0)
                            refere = int(request.POST.get(f'freq_{tranche}_{sexe}_refere', 0) or 0)
                            retour = int(request.POST.get(f'freq_{tranche}_{sexe}_retour', 0) or 0)
                            deces = int(request.POST.get(f'freq_{tranche}_{sexe}_deces', 0) or 0)
                        except ValueError:
                            admis = observes = refere = retour = deces = 0
                        
                        if admis > 0 or observes > 0 or refere > 0 or retour > 0 or deces > 0:
                            FrequentationUrgence.objects.create(
                                urgence=urgence,
                                tranche_age=tranche,
                                sexe=sexe,
                                nb_admis=admis,
                                nb_observes=observes,
                                nb_refere=refere,
                                nb_retour_domicile=retour,
                                nb_deces=deces
                            )
                
                # Morbidités
                for key, value in request.POST.items():
                    if key.startswith('morbidite_pathologie_') and value:
                        suffix = key.replace('morbidite_pathologie_', '')
                        tranche = request.POST.get(f'morbidite_tranche_{suffix}')
                        sexe = request.POST.get(f'morbidite_sexe_{suffix}')
                        try:
                            nombre = int(request.POST.get(f'morbidite_nombre_{suffix}', 0) or 0)
                        except ValueError:
                            nombre = 0
                        if nombre > 0:
                            MorbiditeUrgence.objects.create(
                                urgence=urgence,
                                tranche_age=tranche,
                                sexe=sexe,
                                pathologie=value,
                                nombre=nombre
                            )
                
                # Causes de décès
                for key, value in request.POST.items():
                    if key.startswith('deces_cause_') and value:
                        suffix = key.replace('deces_cause_', '')
                        tranche = request.POST.get(f'deces_tranche_{suffix}')
                        sexe = request.POST.get(f'deces_sexe_{suffix}')
                        try:
                            nombre = int(request.POST.get(f'deces_nombre_{suffix}', 0) or 0)
                        except ValueError:
                            nombre = 0
                        if nombre > 0:
                            CauseDecesUrgence.objects.create(
                                urgence=urgence,
                                tranche_age=tranche,
                                sexe=sexe,
                                cause=value,
                                nombre=nombre
                            )
                
                messages.success(request, "Rapport des urgences créé avec succès !")
                return redirect('urgences:pdf', pk=urgence.pk)
                
        except Exception as e:
            messages.error(request, f"Erreur : {str(e)}")
            return redirect('urgences:create_complete')
    
    # GET request
    tranches_age = [
        ('0-4', '0-4 ans'),
        ('5-9', '5-9 ans'),
        ('10-14', '10-14 ans'),
        ('15-19', '15-19 ans'),
        ('20-24', '20-24 ans'),
        ('25-49', '25-49 ans'),
        ('50+', '50 ans et plus'),
    ]
    sexes = [('M', 'Masculin'), ('F', 'Féminin')]
    
    context = {
        'tranches_age': tranches_age,
        'sexes': sexes,
    }
    return render(request, 'urgences/form_complete.html', context)


@login_required
def urgence_pdf(request, pk):
    """Génère le PDF du rapport des urgences"""
    urgence = get_object_or_404(Urgence, pk=pk)
    return generate_urgence_pdf(urgence)


@login_required
def urgence_delete(request, pk):
    """Supprimer un rapport"""
    urgence = get_object_or_404(Urgence, pk=pk)
    urgence.delete()
    messages.success(request, "Rapport supprimé avec succès")
    return redirect('urgences:list')