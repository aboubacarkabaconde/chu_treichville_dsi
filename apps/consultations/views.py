# apps/consultations/views.py - Version complète

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import Consultation, TrancheAgeActivite, MotifConsultation, DiagnosticRetenu
from .pdf_utils import generate_consultation_pdf


@login_required
def consultation_list(request):
    """Liste des rapports de consultation"""
    rapports = Consultation.objects.all().select_related('created_by')
    context = {'rapports': rapports}
    return render(request, 'consultations/list.html', context)


@login_required
def consultation_create_complete(request):
    """Formulaire complet avec saisie des activités"""
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                consultation = Consultation()
                consultation.service = None
                consultation.service_nom = request.POST.get('service_nom', 'Service non spécifié')
                consultation.mois = request.POST.get('mois')
                consultation.annee = request.POST.get('annee')
                consultation.provenance_secondaire = request.POST.get('provenance_secondaire', 0)
                consultation.provenance_tertiaire = request.POST.get('provenance_tertiaire', 0)
                consultation.non_refere = request.POST.get('non_refere', 0)
                consultation.assurance_cmu = request.POST.get('assurance_cmu', 0)
                consultation.assurance_privee = request.POST.get('assurance_privee', 0)
                consultation.coordinateur_nom = request.POST.get('coordinateur_nom', '')
                consultation.coordinateur_prenom = request.POST.get('coordinateur_prenom', '')
                consultation.surveillant_nom = request.POST.get('surveillant_nom', '')
                consultation.surveillant_prenom = request.POST.get('surveillant_prenom', '')
                consultation.chef_service_nom = request.POST.get('chef_service_nom', '')
                consultation.chef_service_prenom = request.POST.get('chef_service_prenom', '')
                consultation.observations = request.POST.get('observations', '')
                consultation.created_by = request.user
                consultation.save()
                
                # Activités par tranche d'âge
                tranches = ['0-4', '5-9', '10-14', '15-19', '20-24', '25-49', '50+']
                for tranche in tranches:
                    for sexe in ['M', 'F']:
                        nombre = request.POST.get(f'activite_{tranche}_{sexe}', 0)
                        if int(nombre) > 0:
                            TrancheAgeActivite.objects.create(
                                consultation=consultation,
                                tranche_age=tranche,
                                sexe=sexe,
                                nombre=nombre
                            )
                
                # Motifs
                for key, value in request.POST.items():
                    if key.startswith('motif_libelle_') and value:
                        suffix = key.replace('motif_libelle_', '')
                        tranche = request.POST.get(f'motif_tranche_{suffix}')
                        sexe = request.POST.get(f'motif_sexe_{suffix}')
                        nombre = request.POST.get(f'motif_nombre_{suffix}', 0)
                        if int(nombre) > 0:
                            MotifConsultation.objects.create(
                                consultation=consultation,
                                tranche_age=tranche,
                                sexe=sexe,
                                libelle_motif=value,
                                nombre=nombre
                            )
                
                # Diagnostics
                for key, value in request.POST.items():
                    if key.startswith('diag_libelle_') and value:
                        suffix = key.replace('diag_libelle_', '')
                        code = request.POST.get(f'diag_code_{suffix}', '')
                        tranche = request.POST.get(f'diag_tranche_{suffix}')
                        sexe = request.POST.get(f'diag_sexe_{suffix}')
                        nombre = request.POST.get(f'diag_nombre_{suffix}', 0)
                        if int(nombre) > 0:
                            DiagnosticRetenu.objects.create(
                                consultation=consultation,
                                tranche_age=tranche,
                                sexe=sexe,
                                code_diagnostic=code,
                                libelle_diagnostic=value,
                                nombre=nombre
                            )
                
                messages.success(request, "Rapport créé avec succès !")
                return redirect('consultations:pdf', pk=consultation.pk)
                
        except Exception as e:
            messages.error(request, f"Erreur : {str(e)}")
            return redirect('consultations:create_complete')
    
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
    context = {'tranches_age': tranches_age}
    return render(request, 'consultations/form_complete.html', context)


@login_required
def consultation_update(request, pk):
    """Modifier un rapport de consultation"""
    consultation = get_object_or_404(Consultation, pk=pk)
    
    if request.method == 'POST':
        consultation.service_nom = request.POST.get('service_nom', consultation.service_nom)
        consultation.mois = request.POST.get('mois')
        consultation.annee = request.POST.get('annee')
        consultation.provenance_secondaire = request.POST.get('provenance_secondaire', 0)
        consultation.provenance_tertiaire = request.POST.get('provenance_tertiaire', 0)
        consultation.non_refere = request.POST.get('non_refere', 0)
        consultation.assurance_cmu = request.POST.get('assurance_cmu', 0)
        consultation.assurance_privee = request.POST.get('assurance_privee', 0)
        consultation.coordinateur_nom = request.POST.get('coordinateur_nom', '')
        consultation.coordinateur_prenom = request.POST.get('coordinateur_prenom', '')
        consultation.surveillant_nom = request.POST.get('surveillant_nom', '')
        consultation.surveillant_prenom = request.POST.get('surveillant_prenom', '')
        consultation.chef_service_nom = request.POST.get('chef_service_nom', '')
        consultation.chef_service_prenom = request.POST.get('chef_service_prenom', '')
        consultation.observations = request.POST.get('observations', '')
        consultation.save()
        
        messages.success(request, "Rapport modifié avec succès")
        return redirect('consultations:detail', pk=consultation.pk)
    
    # GET request - afficher formulaire avec données existantes
    tranches_age = [
        ('0-4', '0-4 ans'),
        ('5-9', '5-9 ans'),
        ('10-14', '10-14 ans'),
        ('15-19', '15-19 ans'),
        ('20-24', '20-24 ans'),
        ('25-49', '25-49 ans'),
        ('50+', '50 ans et plus'),
    ]
    context = {
        'consultation': consultation,
        'tranches_age': tranches_age,
    }
    return render(request, 'consultations/form_complete.html', context)


@login_required
def consultation_detail_full(request, pk):
    """Afficher le rapport complet"""
    consultation = get_object_or_404(Consultation, pk=pk)
    
    activites = TrancheAgeActivite.objects.filter(consultation=consultation)
    motifs = MotifConsultation.objects.filter(consultation=consultation)
    diagnostics = DiagnosticRetenu.objects.filter(consultation=consultation)
    
    activites_dict = {}
    for act in activites:
        if act.tranche_age not in activites_dict:
            activites_dict[act.tranche_age] = {'M': 0, 'F': 0}
        activites_dict[act.tranche_age][act.sexe] = act.nombre
    
    total_m = sum(data['M'] for data in activites_dict.values())
    total_f = sum(data['F'] for data in activites_dict.values())
    
    tranches_list = ['0-4', '5-9', '10-14', '15-19', '20-24', '25-49', '50+']
    tranches_labels = {
        '0-4': '0-4 ans', '5-9': '5-9 ans', '10-14': '10-14 ans',
        '15-19': '15-19 ans', '20-24': '20-24 ans', '25-49': '25-49 ans', '50+': '50 ans et plus'
    }
    
    context = {
        'consultation': consultation,
        'activites_dict': activites_dict,
        'motifs': motifs,
        'diagnostics': diagnostics,
        'total_m': total_m,
        'total_f': total_f,
        'total_general': total_m + total_f,
        'tranches_list': tranches_list,
        'tranches_labels': tranches_labels,
    }
    return render(request, 'consultations/detail_complete.html', context)


@login_required
def consultation_pdf(request, pk):
    """Génère le PDF du rapport"""
    consultation = get_object_or_404(Consultation, pk=pk)
    return generate_consultation_pdf(consultation)


@login_required
def consultation_delete(request, pk):
    """Supprimer un rapport"""
    consultation = get_object_or_404(Consultation, pk=pk)
    consultation.delete()
    messages.success(request, "Rapport supprimé avec succès")
    return redirect('consultations:list')