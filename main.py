from classes.utilisateur import Utilisateur
from classes.admin       import Admin
from classes.formateur   import Formateur
from classes.apprenant import Apprenant
from classes.personnel import Personnel
from classes.equipement import Equipement
from classes.salle import Salle
from classes.session import SessionFormation
from classes.inscription import Inscription

from decimal             import Decimal
import datetime as dt

import db.init_db as db





admins_a_ajouter = [
    Admin(niveau_acces="SUPERADMIN",date_promotion=dt.date(2000, 2, 20),
        utilisateur=Utilisateur(nom="MY", prenom="Isadmin", email="myadmin.myadmin@mail.fr")),
    Admin(niveau_acces="ADMIN",date_promotion=dt.date(2019, 1, 12),
        utilisateur=Utilisateur(nom="AN", prenom="Nadmin", email="andamin.andamin@mail.fr")),
]

formateurs_a_ajouter = [
    Formateur(specialite="Développement Web (Python/FastAPI)",taux_horaire=Decimal("50.00"),bio="Développeur passionné par les architectures de microservices et le clean code.",
        utilisateur=Utilisateur(nom="Mercier", prenom="Thomas", email="thomas.mercier@mail.fr")),
    Formateur(specialite="Data Science & Machine Learning",taux_horaire=Decimal("62.50"),bio="Ancien ingénieur de recherche, expert sur l'écosystème PyData.",
        utilisateur=Utilisateur(nom="Benali", prenom="Nadia", email="nadia.benali@mail.fr")),
    Formateur(specialite="DevOps & Cloud Computing",taux_horaire=Decimal("75.00"),bio="Architecte Cloud certifié AWS et Kubernetes, formateur depuis 5 ans.",
        utilisateur=Utilisateur(nom="Leclerc", prenom="Julien", email="julien.leclerc@mail.fr")),
    Formateur(specialite="Méthodes Agiles & Scrum",taux_horaire=Decimal("45.00"),bio=None,
        utilisateur=Utilisateur(nom="Gérard", prenom="Sophie", email="sophie.gerard@mail.fr")),
]

apprenants = [
    Apprenant(date_naissance=dt.date(1998, 7, 23), niveau_etude="Bac+5", telephone="0622334455", certification_obtenue="AWS Cloud Practitioner",
              utilisateur=Utilisateur(nom="Roux", prenom="Antoine", email="antoine.roux@mail.fr")),
    Apprenant(date_naissance=dt.date(2005, 11, 3), niveau_etude="Bac+2", telephone="0633445566",
              utilisateur=Utilisateur(nom="Fournier", prenom="Inès", email="ines.fournier@mail.fr")),
    Apprenant(date_naissance=dt.date(1995, 4, 30), niveau_etude="Bac+2", telephone="0644556677",
              utilisateur=Utilisateur(nom="Girard", prenom="Maxime", email="maxime.girard@mail.fr")),
    Apprenant(date_naissance=dt.date(2002, 9, 18), niveau_etude="Bac+3", telephone="0655667788", certification_obtenue="PCAP Python",
              utilisateur=Utilisateur(nom="Bonnet", prenom="Clara", email="clara.bonnet@mail.fr")),
    Apprenant(date_naissance=dt.date(2007, 1, 9), niveau_etude="Bac", telephone="0666778899",
              utilisateur=Utilisateur(nom="Dupuis", prenom="Enzo", email="enzo.dupuis@mail.fr")),
    Apprenant(date_naissance=dt.date(1999, 6, 27), niveau_etude="Bac+5", telephone="0677889900",
              utilisateur=Utilisateur(nom="Lefebvre", prenom="Manon", email="manon.lefebvre@mail.fr")),
    Apprenant(date_naissance=dt.date(2000, 12, 5), niveau_etude="Bac+2", telephone="0688990011",
              utilisateur=Utilisateur(nom="Mercier", prenom="Théo", email="theo.mercier@mail.fr")),
    Apprenant(date_naissance=dt.date(2004, 3, 21), niveau_etude="Bac", telephone="0699001122",
              utilisateur=Utilisateur(nom="Blanc", prenom="Jade", email="jade.blanc@mail.fr")),
    Apprenant(date_naissance=dt.date(1993, 8, 15), niveau_etude="Bac+3", telephone="0600112233", certification_obtenue="Scrum Master",
              utilisateur=Utilisateur(nom="Guerin", prenom="Louis", email="louis.guerin@mail.fr")),
    Apprenant(date_naissance=dt.date(2003, 5, 11), niveau_etude="Bac+2", telephone="0711223344",
              utilisateur=Utilisateur(nom="Muller", prenom="Zoé", email="zoe.muller@mail.fr")),
    Apprenant(date_naissance=dt.date(1997, 10, 2), niveau_etude="Bac+5", telephone="0722334455", certification_obtenue="Azure Fundamentals",
              utilisateur=Utilisateur(nom="Faure", prenom="Alexandre", email="alexandre.faure@mail.fr")),
    Apprenant(date_naissance=dt.date(2006, 2, 28), niveau_etude="Bac", telephone="0733445566",
              utilisateur=Utilisateur(nom="Andre", prenom="Océane", email="oceane.andre@mail.fr")),
    Apprenant(date_naissance=dt.date(2001, 7, 7), niveau_etude="Bac+3", telephone="0744556677",
              utilisateur=Utilisateur(nom="Rousseau", prenom="Baptiste", email="baptiste.rousseau@mail.fr")),
    Apprenant(date_naissance=dt.date(2008, 4, 16), niveau_etude="Bac", telephone="0755667788",
              utilisateur=Utilisateur(nom="Vincent", prenom="Lola", email="lola.vincent@mail.fr")),
    Apprenant(date_naissance=dt.date(1994, 12, 19), niveau_etude="Bac+2", telephone="0766778899", certification_obtenue="Cisco CCNA",
              utilisateur=Utilisateur(nom="Morel", prenom="Romain", email="romain.morel@mail.fr")),
    Apprenant(date_naissance=dt.date(2000, 9, 1), niveau_etude="Bac+5", telephone="0777889900",
              utilisateur=Utilisateur(nom="Fontaine", prenom="Eva", email="eva.fontaine@mail.fr")),
    Apprenant(date_naissance=dt.date(1996, 1, 25), niveau_etude="Bac+3", telephone="0788990011",
              utilisateur=Utilisateur(nom="Chevalier", prenom="Quentin", email="quentin.chevalier@mail.fr")),
    Apprenant(date_naissance=dt.date(2002, 6, 13), niveau_etude="Bac+2", telephone="0799001122", certification_obtenue="Google Data Analytics",
              utilisateur=Utilisateur(nom="Robin", prenom="Anaïs", email="anais.robin@mail.fr")),
    Apprenant(date_naissance=dt.date(1992, 11, 8), niveau_etude="Bac+5", telephone="0700112233",
              utilisateur=Utilisateur(nom="Masson", prenom="Paul", email="paul.masson@mail.fr")),
]

personnel = [
    Personnel(poste="Responsable pédagogique", date_prise_fonction=dt.date(2025, 6, 13), responsabilites=["Accueil des apprenants", "Suivi des présences"],
              utilisateur=Utilisateur(nom="Lambert", prenom="Sophie", email="sophie.lambert@mail.fr")),
    Personnel(poste="Responsable pédagogique", date_prise_fonction=dt.date(2021, 9, 1), responsabilites=["Pilotage des programmes", "Recrutement des formateurs", "Suivi qualité"],
              utilisateur=Utilisateur(nom="Perrin", prenom="Camille", email="camille.perrin@mail.fr")),
    Personnel(poste="Coordinateur de formation", date_prise_fonction=dt.date(2022, 3, 14), responsabilites=["Planning des sessions", "Gestion des salles"],
              utilisateur=Utilisateur(nom="Lemaire", prenom="Nicolas", email="nicolas.lemaire@mail.fr")),
    Personnel(poste="Chargée de projet", date_prise_fonction=dt.date(2023, 1, 9), responsabilites=["Partenariats entreprises", "Suivi des stages"],
              utilisateur=Utilisateur(nom="Colin", prenom="Élodie", email="elodie.colin@mail.fr")),
    Personnel(poste="Responsable qualité", date_prise_fonction=dt.date(2024, 5, 21), responsabilites=["Audits internes", "Enquêtes de satisfaction", "Certification Qualiopi"],
              utilisateur=Utilisateur(nom="Renard", prenom="Julien", email="julien.renard@mail.fr")),
    Personnel(poste="Assistante pédagogique", date_prise_fonction=dt.date(2025, 6, 13), responsabilites=["Accueil des apprenants", "Suivi des présences"],
              utilisateur=Utilisateur(nom="Boyer", prenom="Charlotte", email="charlotte.boyer@mail.fr")),

]

equipement = [
    Equipement(nom="Vidéoprojecteur 4K", description="Modèle Epson pour la salle principale", salle_id=1),
    Equipement(nom="PC Portable Dell Latitude", description="Poste dédié au formateur", salle_id=3),
    Equipement(nom="Tableau Blanc Interactif", description="Écran tactile 75 pouces", salle_id=3),
    Equipement(nom="Routeur Cisco Catalyst", description="Matériel réseau pour les TP DevOps", salle_id=1),
]

salles_a_ajouter = [
    Salle(nom="Salle Alpha", capacite=30, localisation="Bâtiment A - 1er étage"),
    Salle(nom="Salle Beta", capacite=20, localisation="Bâtiment A - Rez-de-chaussée"),
    Salle(nom="Labo Informatique", capacite=20, localisation="Bâtiment B - 2ème étage"),
    Salle(nom="Amphithéâtre", capacite=100, localisation="Bâtiment Principal"),
]

# Timezone de Paris
tz_utc = dt.timezone(dt.timedelta(hours=0))

sessions_a_ajouter = [
    SessionFormation(
        titre="Fondamentaux de Python & SQLModel",
        description="Apprendre les bases du langage Python et la modélisation avec SQLModel.",
        date_debut=dt.datetime(2020, 11, 2, 9, 0, tzinfo=tz_utc),
        date_fin=dt.datetime(2020, 11, 6, 17, 0, tzinfo=tz_utc),
        capacite_max=12,
        statut="ARCHIVEE",
        id_formateur=1,
        id_salle=1
    ),
    SessionFormation(
        titre="Architecture API avec FastAPI",
        description="Créer des API REST robustes, performantes et documentées.",
        date_debut=dt.datetime(2026, 11, 16, 9, 30, tzinfo=tz_utc),
        date_fin=dt.datetime(2026, 11, 20, 18, 0, tzinfo=tz_utc),
        capacite_max=15,
        statut="OUVERTE",
        id_formateur=2,
        id_salle=2
    ),
    SessionFormation(
        titre="Data Science et Visualisation de Données",
        description="Maîtriser Pandas, NumPy et la création de graphiques avancés.",
        date_debut=dt.datetime(2026, 12, 7, 9, 0, tzinfo=tz_utc),
        date_fin=dt.datetime(2026, 12, 11, 17, 0, tzinfo=tz_utc),
        capacite_max=8,
        statut="OUVERTE",
        id_formateur=1,
        id_salle=3
    ),
    SessionFormation(
        titre="Docker & Déploiement Continu (CI/CD)",
        description="Conteneuriser ses applications Python et automatiser les déploiements.",
        date_debut=dt.datetime(2026, 12, 14, 8, 30, tzinfo=tz_utc),
        date_fin=dt.datetime(2026, 12, 16, 16, 30, tzinfo=tz_utc),
        capacite_max=10,
        statut="OUVERTE",
        id_formateur=3,
        id_salle=1
    ),
    SessionFormation(
        titre="Deep Learning avec PyTorch",
        description="Introduction aux réseaux de neurones artificiels et à la vision par ordinateur.",
        date_debut=dt.datetime(2027, 1, 11, 9, 0, tzinfo=tz_utc),
        date_fin=dt.datetime(2027, 1, 15, 17, 0, tzinfo=tz_utc),
        capacite_max=20,
        statut="OUVERTE",
        id_formateur=2,
        id_salle=2
    )
]

inscriptions_a_ajouter = [
    Inscription(
        date_inscription=dt.datetime(2026, 10, 15, 14, 30, tzinfo=dt.timezone.utc),
        statut_inscription="ENREGISTRE",
        presence=True,
        id_apprenant=1,   # Clé étrangère vers l'apprenant ID 1
        id_sessionformation=1      # Clé étrangère vers la session ID 1
    ),
    Inscription(
        date_inscription=dt.datetime(2026, 10, 16, 9, 15, tzinfo=dt.timezone.utc),
        statut_inscription="ENREGISTRE",
        presence=True,
        id_apprenant=2,   # Clé étrangère vers l'apprenant ID 2
        id_sessionformation=1      # Clé étrangère vers la session ID 1
    ),
    Inscription(
        date_inscription=dt.datetime(2026, 10, 18, 11, 0, tzinfo=dt.timezone.utc),
        statut_inscription="EN_ATTENTE",
        presence=None,    # Pas encore statué car la session n'a pas commencé
        id_apprenant=3,   # Clé étrangère vers l'apprenant ID 3
        id_sessionformation=2      # Clé étrangère vers la session ID 2
    ),
    Inscription(
        date_inscription=dt.datetime(2026, 10, 20, 16, 45, tzinfo=dt.timezone.utc),
        statut_inscription="ENREGISTRE",
        presence=False,   # Absent à la formation
        id_apprenant=1,   # Le même apprenant ID 1 sur une autre session
        id_sessionformation=3      # Clé étrangère vers la session ID 3
    ),
    Inscription(
        date_inscription=dt.datetime(2026, 10, 22, 10, 0, tzinfo=dt.timezone.utc),
        statut_inscription="DESINSCRIT",
        presence=None,    # Inscription annulée à l'avance
        id_apprenant=4,   # Clé étrangère vers l'apprenant ID 4
        id_sessionformation=2      # Clé étrangère vers la session ID 2
    )
]

Admin.ajouter_admins(db.engine, admins_a_ajouter)
Admin.afficher_admins(db.engine)

Formateur.ajouter_formateurs(db.engine, formateurs_a_ajouter)
Formateur.afficher_formateurs(db.engine)

Apprenant.ajouter_apprenant(db.engine,apprenants)
Apprenant.afficher(db.engine)

Personnel.ajouter_personnel(db.engine, personnel)
Personnel.afficher_personnel(db.engine)

Salle.ajouter_salles(db.engine, salles_a_ajouter)

Equipement.ajouter_equipement(db.engine, equipement)
Equipement.afficher_equipement(db.engine)

SessionFormation.ajouter_sessions(db.engine, sessions_a_ajouter)
SessionFormation.afficher_sessions(db.engine)

Inscription.ajouter_inscriptions(db.engine, inscriptions_a_ajouter)
Inscription.afficher_inscription(db.engine)


# except Exception as e:
#     print("Erreur :",e)

