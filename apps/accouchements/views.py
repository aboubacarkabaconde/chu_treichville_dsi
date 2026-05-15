# apps/accouchements/views.py - Ajoute la fonction pdf

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponse
from .models import Accouchement
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from io import BytesIO


@login_required
def accouchement_list(request):
    """Liste des rapports d'accouchements"""
    rapports = Accouchement.objects.all().select_related('created_by')
    return render(request, 'accouchements/list.html', {'rapports': rapports})


@login_required
def accouchement_create(request):
    """Créer un nouveau rapport d'accouchements"""
    if request.method == 'POST':
        try:
            with transaction.atomic():
                accouchement = Accouchement()
                accouchement.service = None
                accouchement.service_nom = request.POST.get('service_nom', 'Service de Gynécologie-Obstétrique')
                accouchement.mois = int(request.POST.get('mois', 1))
                accouchement.annee = int(request.POST.get('annee', 2025))
                accouchement.accouchements_domicile = int(request.POST.get('accouchements_domicile', 0))
                accouchement.accouchements_normal = int(request.POST.get('accouchements_normal', 0))
                accouchement.accouchements_cesarienne = int(request.POST.get('accouchements_cesarienne', 0))
                accouchement.autres_accouchements = int(request.POST.get('autres_accouchements', 0))
                accouchement.mort_nes = int(request.POST.get('mort_nes', 0))
                accouchement.naissances_vivantes = int(request.POST.get('naissances_vivantes', 0))
                accouchement.hypotrophie = int(request.POST.get('hypotrophie', 0))
                accouchement.deces_maternel = int(request.POST.get('deces_maternel', 0))
                accouchement.deces_neonatal = int(request.POST.get('deces_neonatal', 0))
                accouchement.coordinateur_nom = request.POST.get('coordinateur_nom', '')
                accouchement.coordinateur_prenom = request.POST.get('coordinateur_prenom', '')
                accouchement.surveillant_nom = request.POST.get('surveillant_nom', '')
                accouchement.surveillant_prenom = request.POST.get('surveillant_prenom', '')
                accouchement.chef_service_nom = request.POST.get('chef_service_nom', '')
                accouchement.chef_service_prenom = request.POST.get('chef_service_prenom', '')
                accouchement.observations = request.POST.get('observations', '')
                accouchement.created_by = request.user
                accouchement.save()
                messages.success(request, "Rapport d'accouchements créé avec succès !")
                return redirect('accouchements:pdf', pk=accouchement.pk)
        except Exception as e:
            messages.error(request, f"Erreur : {str(e)}")
            return redirect('accouchements:create')
    return render(request, 'accouchements/form.html')


@login_required
def accouchement_detail(request, pk):
    accouchement = get_object_or_404(Accouchement, pk=pk)
    return render(request, 'accouchements/detail.html', {'accouchement': accouchement})


@login_required
def accouchement_pdf(request, pk):
    """Génère le PDF du rapport d'accouchements"""
    accouchement = get_object_or_404(Accouchement, pk=pk)
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=15*mm, leftMargin=15*mm,
                           topMargin=20*mm, bottomMargin=20*mm)
    
    styles = getSampleStyleSheet()
    story = []
    
    # Styles
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=14,
                                  alignment=TA_CENTER, textColor=colors.HexColor('#0066CC'), spaceAfter=10)
    subtitle_style = ParagraphStyle('SubtitleStyle', parent=styles['Normal'], fontSize=10,
                                     alignment=TA_CENTER, spaceAfter=20)
    section_style = ParagraphStyle('SectionStyle', parent=styles['Heading2'], fontSize=11,
                                    textColor=colors.HexColor('#004C99'), spaceBefore=12, spaceAfter=6)
    normal_style = ParagraphStyle('NormalStyle', parent=styles['Normal'], fontSize=9, alignment=TA_LEFT)
    
    # En-tête
    story.append(Paragraph("CENTRE HOSPITALIER UNIVERSITAIRE DE TREICHVILLE", title_style))
    story.append(Paragraph("Direction Générale | Direction Médicale et Scientifique | Sous-Direction de l'Information Médicale", subtitle_style))
    story.append(Paragraph("RAPPORT DES ACCOUCHEMENTS", title_style))
    story.append(Spacer(1, 5))
    story.append(Paragraph(f"<b>Période :</b> {accouchement.periode_str}", normal_style))
    story.append(Paragraph(f"<b>Service :</b> {accouchement.service_nom}", normal_style))
    story.append(Spacer(1, 15))
    
    # Types d'accouchements
    story.append(Paragraph("Types d'accouchements", section_style))
    table_data = [
        ['Type', 'Nombre'],
        ['Accouchements à domicile', str(accouchement.accouchements_domicile)],
        ['Accouchement normal (voie basse)', str(accouchement.accouchements_normal)],
        ['Accouchement par césarienne', str(accouchement.accouchements_cesarienne)],
        ['Autres types', str(accouchement.autres_accouchements)],
        ['Total établissement', str(accouchement.total_accouchements)],
        ['Total général', str(accouchement.total_accouchements_global)],
    ]
    table = Table(table_data, colWidths=[200, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0066CC')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    story.append(table)
    story.append(Spacer(1, 15))
    
    # Issues
    story.append(Paragraph("Issues", section_style))
    issues_data = [
        ['Indicateur', 'Nombre'],
        ['Mort-nés', str(accouchement.mort_nes)],
        ['Naissances vivantes', str(accouchement.naissances_vivantes)],
        ['Hypotrophie (poids < 2500g)', str(accouchement.hypotrophie)],
        ['Décès maternel', str(accouchement.deces_maternel)],
        ['Décès néonatal', str(accouchement.deces_neonatal)],
    ]
    issues_table = Table(issues_data, colWidths=[200, 100])
    issues_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#00A86B')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    story.append(issues_table)
    story.append(Spacer(1, 15))
    
    # Observations
    if accouchement.observations:
        story.append(Paragraph("Observations", section_style))
        story.append(Paragraph(accouchement.observations, normal_style))
        story.append(Spacer(1, 15))
    
    # Signatures
    story.append(Spacer(1, 30))
    sig_data = [
        ['', '', ''],
        ['Le Coordinateur', 'Le Surveillant Chef', 'Le Chef de Service'],
        [f"{accouchement.coordinateur_prenom or ''} {accouchement.coordinateur_nom or ''}",
         f"{accouchement.surveillant_prenom or ''} {accouchement.surveillant_nom or ''}",
         f"{accouchement.chef_service_prenom or ''} {accouchement.chef_service_nom or ''}"],
        ['_________________', '_________________', '_________________'],
    ]
    sig_table = Table(sig_data, colWidths=[160, 160, 160])
    sig_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(sig_table)
    
    doc.build(story)
    buffer.seek(0)
    
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="accouchements_{accouchement.id}.pdf"'
    return response


@login_required
def accouchement_update(request, pk):
    accouchement = get_object_or_404(Accouchement, pk=pk)
    if request.method == 'POST':
        accouchement.service_nom = request.POST.get('service_nom', accouchement.service_nom)
        accouchement.mois = int(request.POST.get('mois', accouchement.mois))
        accouchement.annee = int(request.POST.get('annee', accouchement.annee))
        accouchement.accouchements_domicile = int(request.POST.get('accouchements_domicile', 0))
        accouchement.accouchements_normal = int(request.POST.get('accouchements_normal', 0))
        accouchement.accouchements_cesarienne = int(request.POST.get('accouchements_cesarienne', 0))
        accouchement.autres_accouchements = int(request.POST.get('autres_accouchements', 0))
        accouchement.mort_nes = int(request.POST.get('mort_nes', 0))
        accouchement.naissances_vivantes = int(request.POST.get('naissances_vivantes', 0))
        accouchement.hypotrophie = int(request.POST.get('hypotrophie', 0))
        accouchement.deces_maternel = int(request.POST.get('deces_maternel', 0))
        accouchement.deces_neonatal = int(request.POST.get('deces_neonatal', 0))
        accouchement.save()
        messages.success(request, "Rapport modifié avec succès")
        return redirect('accouchements:detail', pk=accouchement.pk)
    return render(request, 'accouchements/form.html', {'accouchement': accouchement})


@login_required
def accouchement_delete(request, pk):
    accouchement = get_object_or_404(Accouchement, pk=pk)
    accouchement.delete()
    messages.success(request, "Rapport supprimé avec succès")
    return redirect('accouchements:list')