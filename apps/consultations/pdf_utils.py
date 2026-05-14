# apps/consultations/pdf_utils.py

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from io import BytesIO
from django.http import HttpResponse


def generate_consultation_pdf(consultation):
    """Génère le PDF pour un rapport de consultation"""
    
    from .models import TrancheAgeActivite, MotifConsultation, DiagnosticRetenu
    
    # Récupérer les données
    activites = TrancheAgeActivite.objects.filter(consultation=consultation)
    motifs = MotifConsultation.objects.filter(consultation=consultation)
    diagnostics = DiagnosticRetenu.objects.filter(consultation=consultation)
    
    # Organiser les activités
    activites_dict = {}
    for act in activites:
        if act.tranche_age not in activites_dict:
            activites_dict[act.tranche_age] = {'M': 0, 'F': 0}
        activites_dict[act.tranche_age][act.sexe] = act.nombre
    
    total_m = sum(data['M'] for data in activites_dict.values())
    total_f = sum(data['F'] for data in activites_dict.values())
    
    # Créer le PDF
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
    story.append(Paragraph("RAPPORT MENSUEL DE CONSULTATION", title_style))
    story.append(Spacer(1, 5))
    story.append(Paragraph(f"<b>Période :</b> {consultation.periode_str}", normal_style))
    story.append(Paragraph(f"<b>Service :</b> {consultation.service_nom}", normal_style))
    story.append(Spacer(1, 15))
    
    # Tableau 1: Activité
    story.append(Paragraph("Tableau 1 : Activité par tranche d'âge et sexe", section_style))
    table_data = [['Tranche d\'âge', 'Masculin (M)', 'Féminin (F)', 'Total']]
    tranches = ['0-4', '5-9', '10-14', '15-19', '20-24', '25-49', '50+']
    labels = {'0-4': '0-4 ans', '5-9': '5-9 ans', '10-14': '10-14 ans',
              '15-19': '15-19 ans', '20-24': '20-24 ans', '25-49': '25-49 ans', '50+': '50 ans et plus'}
    
    for tranche in tranches:
        m = activites_dict.get(tranche, {}).get('M', 0)
        f = activites_dict.get(tranche, {}).get('F', 0)
        table_data.append([labels[tranche], str(m), str(f), str(m + f)])
    table_data.append(['TOTAL GÉNÉRAL', str(total_m), str(total_f), str(total_m + total_f)])
    
    table = Table(table_data, colWidths=[80, 70, 70, 70])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0066CC')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    story.append(table)
    story.append(Spacer(1, 15))
    
    # Provenance
    story.append(Paragraph("Provenance des patients", section_style))
    story.append(Paragraph(f"Structure secondaire : {consultation.provenance_secondaire}", normal_style))
    story.append(Paragraph(f"Structure tertiaire : {consultation.provenance_tertiaire}", normal_style))
    story.append(Paragraph(f"Non référé : {consultation.non_refere}", normal_style))
    story.append(Spacer(1, 10))
    
    # Assurances
    story.append(Paragraph("Assurances", section_style))
    story.append(Paragraph(f"Patients CMU : {consultation.assurance_cmu}", normal_style))
    story.append(Paragraph(f"Assurance privée : {consultation.assurance_privee}", normal_style))
    story.append(Spacer(1, 15))
    
    # Tableau 2: Motifs
    if motifs.exists():
        story.append(Paragraph("Tableau 2 : Motifs de consultation", section_style))
        motif_data = [['Motif', 'Tranche d\'âge', 'Sexe', 'Nombre']]
        for motif in motifs:
            motif_data.append([
                motif.libelle_motif[:40],
                motif.get_tranche_age_display(),
                motif.get_sexe_display(),
                str(motif.nombre)
            ])
        
        motif_table = Table(motif_data, colWidths=[120, 80, 60, 50])
        motif_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#00A86B')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
        ]))
        story.append(motif_table)
        story.append(Spacer(1, 15))
    else:
        story.append(Paragraph("Tableau 2 : Motifs de consultation", section_style))
        story.append(Paragraph("<i>Aucun motif enregistré</i>", normal_style))
        story.append(Spacer(1, 10))
    
    # Tableau 3: Diagnostics
    if diagnostics.exists():
        story.append(Paragraph("Tableau 3 : Diagnostics retenus", section_style))
        diag_data = [['Code', 'Diagnostic', 'Tranche d\'âge', 'Sexe', 'Nombre']]
        for diag in diagnostics:
            diag_data.append([
                diag.code_diagnostic or '-',
                diag.libelle_diagnostic[:35],
                diag.get_tranche_age_display(),
                diag.get_sexe_display(),
                str(diag.nombre)
            ])
        
        diag_table = Table(diag_data, colWidths=[50, 100, 70, 50, 50])
        diag_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#FFC107')),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
        ]))
        story.append(diag_table)
        story.append(Spacer(1, 15))
    else:
        story.append(Paragraph("Tableau 3 : Diagnostics retenus", section_style))
        story.append(Paragraph("<i>Aucun diagnostic enregistré</i>", normal_style))
        story.append(Spacer(1, 10))
    
    # Observations
    if consultation.observations:
        story.append(Paragraph("Observations", section_style))
        story.append(Paragraph(consultation.observations, normal_style))
        story.append(Spacer(1, 15))
    
    # Signatures
    story.append(Spacer(1, 30))
    sig_data = [
        ['', '', ''],
        ['Le Coordinateur', 'Le Surveillant Chef', 'Le Chef de Service'],
        [f"{consultation.coordinateur_prenom or ''} {consultation.coordinateur_nom or ''}",
         f"{consultation.surveillant_prenom or ''} {consultation.surveillant_nom or ''}",
         f"{consultation.chef_service_prenom or ''} {consultation.chef_service_nom or ''}"],
        ['_________________', '_________________', '_________________'],
        ['Date: ___________', 'Date: ___________', 'Date: ___________']
    ]
    sig_table = Table(sig_data, colWidths=[160, 160, 160])
    sig_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
    ]))
    story.append(sig_table)
    
    # Générer le PDF
    doc.build(story)
    buffer.seek(0)
    
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="consultation_{consultation.id}.pdf"'
    return response