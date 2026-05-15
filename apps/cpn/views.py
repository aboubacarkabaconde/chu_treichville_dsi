from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import ConsultationPrenatale


@login_required
def cpn_list(request):
    rapports = ConsultationPrenatale.objects.all().select_related('created_by')
    return render(request, 'cpn/list.html', {'rapports': rapports})


@login_required
def cpn_create(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                cpn = ConsultationPrenatale()
                cpn.service = None
                cpn.service_nom = request.POST.get('service_nom', '')
                cpn.mois = int(request.POST.get('mois', 1))
                cpn.annee = int(request.POST.get('annee', 2025))
                cpn.cpn1 = int(request.POST.get('cpn1', 0))
                cpn.cpn2 = int(request.POST.get('cpn2', 0))
                cpn.cpn3 = int(request.POST.get('cpn3', 0))
                cpn.cpn4 = int(request.POST.get('cpn4', 0))
                cpn.cpn5_plus = int(request.POST.get('cpn5_plus', 0))
                cpn.consultations_postnatales = int(request.POST.get('consultations_postnatales', 0))
                cpn.coordinateur_nom = request.POST.get('coordinateur_nom', '')
                cpn.coordinateur_prenom = request.POST.get('coordinateur_prenom', '')
                cpn.surveillant_nom = request.POST.get('surveillant_nom', '')
                cpn.surveillant_prenom = request.POST.get('surveillant_prenom', '')
                cpn.chef_service_nom = request.POST.get('chef_service_nom', '')
                cpn.chef_service_prenom = request.POST.get('chef_service_prenom', '')
                cpn.observations = request.POST.get('observations', '')
                cpn.created_by = request.user
                cpn.save()
                messages.success(request, 'Rapport CPN cree avec succes !')
                return redirect('cpn:pdf', pk=cpn.pk)
        except Exception as e:
            messages.error(request, f'Erreur : {str(e)}')
            return redirect('cpn:create')
    return render(request, 'cpn/form.html')


@login_required
def cpn_detail(request, pk):
    cpn = get_object_or_404(ConsultationPrenatale, pk=pk)
    return render(request, 'cpn/detail.html', {'cpn': cpn})


@login_required
def cpn_pdf(request, pk):
    from django.http import HttpResponse
    return HttpResponse('PDF en developpement', content_type='application/pdf')


@login_required
def cpn_update(request, pk):
    cpn = get_object_or_404(ConsultationPrenatale, pk=pk)
    if request.method == 'POST':
        cpn.service_nom = request.POST.get('service_nom', cpn.service_nom)
        cpn.mois = int(request.POST.get('mois', cpn.mois))
        cpn.annee = int(request.POST.get('annee', cpn.annee))
        cpn.cpn1 = int(request.POST.get('cpn1', 0))
        cpn.cpn2 = int(request.POST.get('cpn2', 0))
        cpn.cpn3 = int(request.POST.get('cpn3', 0))
        cpn.cpn4 = int(request.POST.get('cpn4', 0))
        cpn.cpn5_plus = int(request.POST.get('cpn5_plus', 0))
        cpn.consultations_postnatales = int(request.POST.get('consultations_postnatales', 0))
        cpn.save()
        messages.success(request, 'Rapport modifie')
        return redirect('cpn:detail', pk=cpn.pk)
    return render(request, 'cpn/form.html', {'cpn': cpn})


@login_required
def cpn_delete(request, pk):
    cpn = get_object_or_404(ConsultationPrenatale, pk=pk)
    cpn.delete()
    messages.success(request, 'Rapport supprime')
    return redirect('cpn:list')
