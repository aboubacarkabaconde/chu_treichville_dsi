# apps/urgences/pdf_utils.py

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from io import BytesIO
from django.http import HttpResponse


def generate_urgence_pdf(urgence):
    """Génère le PDF pour un rapport des urgences"""
    
    from .models import FrequentationUrgence, MorbiditeUrgence, CauseDecesUrgence
    
    # Récupérer les données
    frequentations = FrequentationUrgence.objects.filter(urgence=urgence)
    morbidites = MorbiditeUrgence.objects.filter(urgence=urgence)
    causes_deces = CauseDecesUrgence.objects.filter(urgence=urgence)
    
    # Organiser les fréquentations
    freq_dict = {}
    for freq in frequentations:
        key = f"{freq.tranche_age}_{freq.sexe}"
        freq_dict[key] = freq
    
    # Créer le PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=15*mm, leftMargin=15*mm,
                           topMargin=20*mm, bottomMargin=20*mm)
    
    styles = getSampleStyleSheet()
    story = []
    
    # Styles
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=14,
                                  alignment=TA_CENTER, textColor=colors.HexColor('#DC3545'), spaceAfter=10)
    subtitle_style = ParagraphStyle('SubtitleStyle', parent=styles['Normal'], fontSize=10,
                                     alignment=TA_CENTER, spaceAfter=20)
    section_style = ParagraphStyle('SectionStyle', parent=styles['Heading2'], fontSize=11,
                                    textColor=colors.HexColor('#DC3545'), spaceBefore=12, spaceAfter=6)
    normal_style = ParagraphStyle('NormalStyle', parent=styles['Normal'], fontSize=9, alignment=TA_LEFT)
    
    # En-tête
    story.append(Paragraph("CENTRE HOSPITALIER UNIVERSITAIRE DE TREICHVILLE", title_style))
    story.append(Paragraph("Direction Générale | Direction Médicale et Scientifique | Sous-Direction de l'Information Médicale", subtitle_style))
    story.append(Paragraph("RAPPORT MENSUEL DES URGENCES", title_style))
    story.append(Spacer(1, 5))
    story.append(Paragraph(f"<b>Période :</b> {urgence.periode_str}", normal_style))
    story.append(Paragraph(f"<b>Service :</b> {urgence.service_nom}", normal_style))
    story.append(Spacer(1, 15))
    
    # Tableau 1: Capacité d'accueil
    story.append(Paragraph("Tableau 1 : Capacité d'accueil", section_style))
    cap_data = [
        ['Indicateur', 'Valeur'],
        ['Nombre de lits', str(urgence.nb_lits)],
        ['Lits fonctionnels', str(urgence.nb_lits_fonctionnels)],
        ['Journées théoriques', str(urgence.nb_journees_theoriques)],
        ['Journées réalisées', str(urgence.nb_journees_realisees)],
        ['Taux d\'occupation (%)', f"{urgence.taux_occupation:.1f}%"],
        ['Délai moyen de prise en charge (heures)', str(urgence.delai_moyen_pec)],
    ]
    cap_table = Table(cap_data, colWidths=[200, 100])
    cap_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#DC3545')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
    ]))
    story.append(cap_table)
    story.append(Spacer(1, 15))
    
    # Tableau 2: Fréquentation
    story.append(Paragraph("Tableau 2 : Fréquentation par tranche d'âge et sexe", section_style))
    
    freq_table_data = [['Tranche', 'Sexe', 'Admis', 'Observés', 'Référé', 'Retour domicile', 'Décès']]
    tranches = ['0-4', '5-9', '10-14', '15-19', '20-24', '25-49', '50+']
    labels = {'0-4': '0-4 ans', '5-9': '5-9 ans', '10-14': '10-14 ans',
              '15-19': '15-19 ans', '20-24': '20-24 ans', '25-49': '25-49 ans', '50+': '50 ans et plus'}
    
    total_admis = 0
    total_observes = 0
    total_refere = 0
    total_retour = 0
    total_deces = 0
    
    for tranche in tranches:
        for sexe in ['M', 'F']:
            key = f"{tranche}_{sexe}"
            freq = freq_dict.get(key)
            if freq:
                admis = freq.nb_admis
                observes = freq.nb_observes
                refere = freq.nb_refere
                retour = freq.nb_retour_domicile
                deces = freq.nb_deces
            else:
                admis = observes = refere = retour = deces = 0
            
            total_admis += admis
            total_observes += observes
            total_refere += refere
            total_retour += retour
            total_deces += deces
            
            freq_table_data.append([
                labels[tranche], 'Masculin' if sexe == 'M' else 'Féminin',
                str(admis), str(observes), str(refere), str(retour), str(deces)
            ])
    
    freq_table_data.append(['TOTAL', '', str(total_admis), str(total_observes), str(total_refere), str(total_retour), str(total_deces)])
    
    freq_table = Table(freq_table_data, colWidths=[70, 60, 45, 55, 45, 65, 45])
    freq_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#DC3545')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#f8f9fa')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
    ]))
    story.append(freq_table)
    story.append(Spacer(1, 15))
    
    # Assurances
    story.append(Paragraph("Assurances", section_style))
    story.append(Paragraph(f"Patients CMU : {urgence.assurance_cmu}", normal_style))
    story.append(Paragraph(f"Assurance privée : {urgence.assurance_privee}", normal_style))
    story.append(Spacer(1, 15))
    
    # Tableau 3: Morbidité
    if morbidites.exists():
        story.append(Paragraph("Tableau 3 : Morbidité", section_style))
        morbidite_data = [['Pathologie', 'Tranche d\'âge', 'Sexe', 'Nombre']]
        for m in morbidites:
            morbidite_data.append([
                m.pathologie[:40], m.get_tranche_age_display(), m.get_sexe_display(), str(m.nombre)
            ])
        morbidite_table = Table(morbidite_data, colWidths=[120, 80, 60, 50])
        morbidite_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#17A2B8')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
        ]))
        story.append(morbidite_table)
        story.append(Spacer(1, 15))
    
    # Tableau 4: Causes des décès
    if causes_deces.exists():
        story.append(Paragraph("Tableau 4 : Causes des décès", section_style))
        deces_data = [['Cause du décès', 'Tranche d\'âge', 'Sexe', 'Nombre']]
        for d in causes_deces:
            deces_data.append([
                d.cause[:40], d.get_tranche_age_display(), d.get_sexe_display(), str(d.nombre)
            ])
        deces_table = Table(deces_data, colWidths=[120, 80, 60, 50])
        deces_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6C757D')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
        ]))
        story.append(deces_table)
        story.append(Spacer(1, 15))
    
    # Observations
    if urgence.observations:
        story.append(Paragraph("Observations", section_style))
        story.append(Paragraph(urgence.observations, normal_style))
        story.append(Spacer(1, 15))
    
    # Signatures
    story.append(Spacer(1, 30))
    sig_data = [
        ['', '', ''],
        ['Le Coordinateur', 'Le Surveillant Chef', 'Le Chef de Service'],
        [f"{urgence.coordinateur_prenom or ''} {urgence.coordinateur_nom or ''}",
         f"{urgence.surveillant_prenom or ''} {urgence.surveillant_nom or ''}",
         f"{urgence.chef_service_prenom or ''} {urgence.chef_service_nom or ''}"],
        ['_________________', '_________________', '_________________'],
    ]
    sig_table = Table(sig_data, colWidths=[160, 160, 160])
    sig_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
    ]))
    story.append(sig_table)
    
    doc.build(story)
    buffer.seek(0)
    
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="urgences_{urgence.id}.pdf"'
    return response