# apps/rapports/pdf_generator.py

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO
from django.http import HttpResponse
from datetime import datetime
import os

class ConsultationPDFGenerator:
    def __init__(self, consultation):
        self.consultation = consultation
        self.buffer = BytesIO()
        self.doc = SimpleDocTemplate(
            self.buffer,
            pagesize=A4,
            rightMargin=20*mm,
            leftMargin=20*mm,
            topMargin=20*mm,
            bottomMargin=20*mm
        )
        self.styles = getSampleStyleSheet()
        self.elements = []
        
    def get_style(self):
        # Style pour le titre principal
        self.styles.add(ParagraphStyle(
            name='MainTitle',
            parent=self.styles['Heading1'],
            fontSize=16,
            alignment=TA_CENTER,
            spaceAfter=20,
            textColor=colors.HexColor('#0066CC')
        ))
        
        # Style pour les sous-titres
        self.styles.add(ParagraphStyle(
            name='SubTitle',
            parent=self.styles['Heading2'],
            fontSize=12,
            alignment=TA_CENTER,
            spaceAfter=10
        ))
        
        # Style pour les titres de sections
        self.styles.add(ParagraphStyle(
            name='SectionTitle',
            parent=self.styles['Heading3'],
            fontSize=11,
            textColor=colors.HexColor('#004C99'),
            spaceAfter=8,
            spaceBefore=12
        ))
        
        # Style pour le texte normal
        self.styles.add(ParagraphStyle(
            name='NormalText',
            parent=self.styles['Normal'],
            fontSize=9,
            alignment=TA_LEFT
        ))
        
        return self.styles
    
    def add_header(self):
        """Ajoute l'en-tête du document"""
        header_data = [
            [Paragraph("CENTRE HOSPITALIER UNIVERSITAIRE DE TREICHVILLE", self.styles['MainTitle'])],
            [Paragraph("Direction Générale | Direction Médicale et Scientifique | Sous-Direction de l'Information Médicale", 
                      self.styles['SubTitle'])],
            [Spacer(1, 10)],
            [Paragraph("RAPPORT MENSUEL DE CONSULTATION", self.styles['MainTitle'])],
            [Spacer(1, 5)],
            [Paragraph(f"<b>Période :</b> {self.consultation.periode_str}", self.styles['NormalText'])],
            [Paragraph(f"<b>Service :</b> {self.consultation.service.nom}", self.styles['NormalText'])],
            [Spacer(1, 15)],
        ]
        
        for row in header_data:
            self.elements.extend(row)
    
    def add_activite_table(self):
        """Tableau 1: Activité par tranche d'âge"""
        self.elements.append(Paragraph("Tableau 1 : Activité par tranche d'âge et sexe", self.styles['SectionTitle']))
        
        # Récupérer les données
        activites = self.consultation.activites.all()
        activites_dict = {}
        for act in activites:
            if act.tranche_age not in activites_dict:
                activites_dict[act.tranche_age] = {'M': 0, 'F': 0}
            activites_dict[act.tranche_age][act.sexe] = act.nombre
        
        tranches = ['0-4', '5-9', '10-14', '15-19', '20-24', '25-49', '50+']
        labels = {
            '0-4': '0-4 ans', '5-9': '5-9 ans', '10-14': '10-14 ans',
            '15-19': '15-19 ans', '20-24': '20-24 ans', '25-49': '25-49 ans', '50+': '50 ans et plus'
        }
        
        # Construction du tableau
        data = [['Tranche d\'âge', 'Masculin (M)', 'Féminin (F)', 'Total']]
        total_m = 0
        total_f = 0
        
        for tranche in tranches:
            m_val = activites_dict.get(tranche, {}).get('M', 0)
            f_val = activites_dict.get(tranche, {}).get('F', 0)
            total = m_val + f_val
            total_m += m_val
            total_f += f_val
            data.append([labels[tranche], str(m_val), str(f_val), str(total)])
        
        data.append(['TOTAL GÉNÉRAL', str(total_m), str(total_f), str(total_m + total_f)])
        
        # Créer le tableau
        table = Table(data, colWidths=[80, 70, 70, 70])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0066CC')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -2), colors.white),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#E6F0FF')),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ]))
        
        self.elements.append(table)
        self.elements.append(Spacer(1, 10))
    
    def add_provenance_assurance(self):
        """Ajoute les informations de provenance et assurances"""
        # Provenance
        self.elements.append(Paragraph("Provenance des patients", self.styles['SectionTitle']))
        provenance_data = [
            [f"<b>Structure secondaire :</b> {self.consultation.provenance_secondaire}"],
            [f"<b>Structure tertiaire :</b> {self.consultation.provenance_tertiaire}"],
            [f"<b>Non référé :</b> {self.consultation.non_refere}"],
        ]
        
        for row in provenance_data:
            self.elements.append(Paragraph(row[0], self.styles['NormalText']))
        
        self.elements.append(Spacer(1, 10))
        
        # Assurances
        self.elements.append(Paragraph("Assurances", self.styles['SectionTitle']))
        assurance_data = [
            [f"<b>Patients CMU :</b> {self.consultation.assurance_cmu}"],
            [f"<b>Assurance privée :</b> {self.consultation.assurance_privee}"],
        ]
        
        for row in assurance_data:
            self.elements.append(Paragraph(row[0], self.styles['NormalText']))
        
        self.elements.append(Spacer(1, 10))
    
    def add_motifs_table(self):
        """Tableau 2: Motifs de consultation"""
        motifs = self.consultation.motifs.all()
        if motifs.exists():
            self.elements.append(Paragraph("Tableau 2 : Motifs de consultation", self.styles['SectionTitle']))
            
            data = [['Motif', 'Tranche d\'âge', 'Sexe', 'Nombre']]
            for motif in motifs:
                data.append([
                    motif.libelle_motif,
                    motif.get_tranche_age_display(),
                    motif.get_sexe_display(),
                    str(motif.nombre)
                ])
            
            table = Table(data, colWidths=[120, 70, 50, 50])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#00A86B')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
            ]))
            
            self.elements.append(table)
            self.elements.append(Spacer(1, 10))
    
    def add_diagnostics_table(self):
        """Tableau 3: Diagnostics retenus"""
        diagnostics = self.consultation.diagnostics.all()
        if diagnostics.exists():
            self.elements.append(Paragraph("Tableau 3 : Diagnostics retenus", self.styles['SectionTitle']))
            
            data = [['Code', 'Diagnostic', 'Tranche d\'âge', 'Sexe', 'Nombre']]
            for diag in diagnostics:
                data.append([
                    diag.code_diagnostic or '-',
                    diag.libelle_diagnostic,
                    diag.get_tranche_age_display(),
                    diag.get_sexe_display(),
                    str(diag.nombre)
                ])
            
            table = Table(data, colWidths=[50, 100, 70, 50, 50])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#FFC107')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
            ]))
            
            self.elements.append(table)
            self.elements.append(Spacer(1, 10))
    
    def add_observations(self):
        """Ajoute les observations"""
        if self.consultation.observations:
            self.elements.append(Paragraph("Observations", self.styles['SectionTitle']))
            self.elements.append(Paragraph(self.consultation.observations, self.styles['NormalText']))
            self.elements.append(Spacer(1, 10))
    
    def add_signatures(self):
        """Ajoute les signatures"""
        self.elements.append(Spacer(1, 30))
        self.elements.append(Paragraph("Signatures", self.styles['SectionTitle']))
        
        # Tableau des signatures
        signature_data = [
            ['', '', ''],
            ['<b>Le Coordinateur</b>', '<b>Le Surveillant Chef</b>', '<b>Le Chef de Service</b>'],
            [f"{self.consultation.coordinateur_prenom or ''} {self.consultation.coordinateur_nom or ''}",
             f"{self.consultation.surveillant_prenom or ''} {self.consultation.surveillant_nom or ''}",
             f"{self.consultation.chef_service_prenom or ''} {self.consultation.chef_service_nom or ''}"],
            ['_____________________', '_____________________', '_____________________'],
            [f"Date: {datetime.now().strftime('%d/%m/%Y')}", "Date: ___________", "Date: ___________"]
        ]
        
        table = Table(signature_data, colWidths=[160, 160, 160])
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
        ]))
        
        self.elements.append(table)
    
    def generate(self):
        """Génère le PDF complet"""
        self.get_style()
        self.add_header()
        self.add_activite_table()
        self.add_provenance_assurance()
        self.add_motifs_table()
        self.add_diagnostics_table()
        self.add_observations()
        self.add_signatures()
        
        # Construire le PDF
        self.doc.build(self.elements)
        
        # Retourner le buffer
        self.buffer.seek(0)
        return self.buffer


def generate_consultation_pdf(consultation):
    """Fonction utilitaire pour générer un PDF de consultation"""
    generator = ConsultationPDFGenerator(consultation)
    buffer = generator.generate()
    
    # Créer la réponse HTTP
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="consultation_{consultation.service.nom}_{consultation.periode_str}.pdf"'
    
    return response