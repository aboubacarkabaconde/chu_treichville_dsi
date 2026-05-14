# scripts/insert_services.py

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chu_treichville.settings')
django.setup()

from apps.core.models import CategorieService, Service

def create_categories():
    categories = [
        ('MEDICAL', 'Services Médicaux', 1),
        ('TECHNIQUE', 'Services Techniques', 2),
        ('URGENCES', 'Services des Urgences', 3),
        ('MATERNITE', 'Maternité et Pédiatrie', 4),
    ]
    
    for code, nom, ordre in categories:
        CategorieService.objects.get_or_create(
            code=code,
            defaults={'nom': nom, 'ordre': ordre}
        )
    print("Catégories créées")

def create_services():
    services = [
        # Services Médicaux
        ('Anesthésie-réanimation', 'ANESTH', 'consultation', 'MEDICAL'),
        ('Cabinet dentaire', 'DENT', 'consultation', 'MEDICAL'),
        ('Cancérologie', 'CANCER', 'consultation', 'MEDICAL'),
        ('Proctologie', 'PROCTO', 'consultation', 'MEDICAL'),
        ('Endocrinologie', 'ENDO', 'consultation', 'MEDICAL'),
        ('Chirurgie pédiatrique', 'CHIRPED', 'consultation', 'MEDICAL'),
        ('Chirurgie plastique', 'CHIRPLAST', 'consultation', 'MEDICAL'),
        ('Dermatologie', 'DERMA', 'consultation', 'MEDICAL'),
        ('Gynécologie-obstétrique', 'GYNO', 'accouchement', 'MEDICAL'),
        ('Maladies infectieuses', 'INFECT', 'consultation', 'MEDICAL'),
        ('Médecine interne', 'MEDINT', 'consultation', 'MEDICAL'),
        ('Urologie', 'URO', 'consultation', 'MEDICAL'),
        ('Néphrologie', 'NEPHRO', 'consultation', 'MEDICAL'),
        ('Diabétologie', 'DIAB', 'consultation', 'MEDICAL'),
        ('Rééducation fonctionnelle', 'REEDUC', 'consultation', 'MEDICAL'),
        ('Médecine du travail', 'TRAVAIL', 'consultation', 'MEDICAL'),
        ('Psychiatrie', 'PSY', 'consultation', 'MEDICAL'),
        ('Neurologie', 'NEURO', 'consultation', 'MEDICAL'),
        ('Ophtalmologie', 'OPHTA', 'consultation', 'MEDICAL'),
        ('ORL', 'ORL', 'consultation', 'MEDICAL'),
        ('Pneumo-PHtisiologie', 'PPH', 'consultation', 'MEDICAL'),
        ('Pédiatrie', 'PED', 'nutrition_vaccination', 'MEDICAL'),
        ('Stomatologie', 'STOMATO', 'consultation', 'MEDICAL'),
        ('Traumatologique', 'TRAUMA', 'consultation', 'MEDICAL'),
        
        # Services Techniques
        ('Anatomie-pathologie', 'ANAPATH', 'anatomopathologie', 'TECHNIQUE'),
        ('Laboratoire centrale', 'LABO', 'biologie', 'TECHNIQUE'),
        ('CeDReS', 'CEDRES', 'biologie', 'TECHNIQUE'),
        ('Radiodiagnostic', 'RADIO', 'imagerie', 'TECHNIQUE'),
        ('Imagerie médicale', 'IMAGERIE', 'imagerie', 'TECHNIQUE'),
        ('Pharmacie', 'PHARMA', 'consultation', 'TECHNIQUE'),
        
        # Urgences
        ('Urgences Gynécologiques', 'URGGYNO', 'urgence', 'URGENCES'),
        ('Urgences Pédiatriques', 'URGPED', 'urgence', 'URGENCES'),
        ('Urgences Médicales', 'URGMED', 'urgence', 'URGENCES'),
        ('Urgences Chirurgicales', 'URGCHIR', 'urgence', 'URGENCES'),
        
        # Maternité et Pédiatrie
        ('Néonatalogie', 'NEONAT', 'neonatologie', 'MATERNITE'),
        ('Méthode Mère Kangourou', 'KMC', 'kmc', 'MATERNITE'),
        ('CPN', 'CPN', 'cpn', 'MATERNITE'),
        ('Planning Familial', 'PF', 'planning_familial', 'MATERNITE'),
    ]
    
    medical_cat = CategorieService.objects.get(code='MEDICAL')
    technique_cat = CategorieService.objects.get(code='TECHNIQUE')
    urgences_cat = CategorieService.objects.get(code='URGENCES')
    maternite_cat = CategorieService.objects.get(code='MATERNITE')
    
    cat_map = {
        'MEDICAL': medical_cat,
        'TECHNIQUE': technique_cat,
        'URGENCES': urgences_cat,
        'MATERNITE': maternite_cat,
    }
    
    for i, (nom, code, type_rapport, cat_code) in enumerate(services):
        Service.objects.get_or_create(
            code=code,
            defaults={
                'nom': nom,
                'categorie': cat_map[cat_code],
                'type_rapport': type_rapport,
                'actif': True,
                'ordre': i
            }
        )
    
    print(f"{len(services)} services créés")

if __name__ == '__main__':
    create_categories()
    create_services()
    print("Insertion terminée !")