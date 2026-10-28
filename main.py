
from classes.utilisateur import Utilisateur
from classes.formateur   import Formateur

from decimal             import Decimal

import db.init_db as db



# try:
formateurs_a_ajouter = [
    Formateur(
        specialite="Développement Web (Python/FastAPI)",
        taux_horaire=Decimal("50.00"),
        bio="Développeur passionné par les architectures de microservices et le clean code.",
        utilisateur=Utilisateur(
            nom="Mercier", prenom="Thomas", email="thomas.mercier@mail.fr"
        ),
    ),
    Formateur(
        specialite="Data Science & Machine Learning",
        taux_horaire=Decimal("62.50"),
        bio="Ancien ingénieur de recherche, expert sur l'écosystème PyData.",
        utilisateur=Utilisateur(
            nom="Benali", prenom="Nadia", email="nadia.benali@mail.fr"
        ),
    ),
    Formateur(
        specialite="DevOps & Cloud Computing",
        taux_horaire=Decimal("75.00"),
        bio="Architecte Cloud certifié AWS et Kubernetes, formateur depuis 5 ans.",
        utilisateur=Utilisateur(
            nom="Leclerc", prenom="Julien", email="julien.leclerc@mail.fr"
        ),
    ),
    Formateur(
        specialite="Méthodes Agiles & Scrum",
        taux_horaire=Decimal("45.00"),
        bio=None,
        utilisateur=Utilisateur(
            nom="Gérard", prenom="Sophie", email="sophie.gerard@mail.fr"
        ),
    ),
]

Formateur.ajouter_formateurs(db.engine, formateurs_a_ajouter)
Formateur.afficher_formateurs(db.engine)

# except Exception as e:
#     print("Erreur :",e)

