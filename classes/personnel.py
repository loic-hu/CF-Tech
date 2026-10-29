"""Modèle Personnel (table SQL + objet Python) du projet CF-Tech.
 
Ce module définit :
    - NiveauEtude : l'énumération des niveaux d'études possibles ;
    - Personnel   : la table « personnel », reliée à la table « utilisateur »
                    par une relation 1-1 (id_utilisateur).
 
Un membre du Personnel ne contient pas nom, prénom ni email : ces données sont dans
l'utilisateur associé, accessible via la relation `personnel.utilisateur`.
"""

from sqlmodel import Field, Relationship, Session, SQLModel, col, create_engine, func, or_, select, Column, JSON
from sqlalchemy.orm import joinedload

from classes.utilisateur  import Utilisateur

import tabulate
import pydantic   as pyd
import datetime   as dt

class Personnel(SQLModel, table=True):
    """Profil d'un membre du Personnel de la plateforme (table « personnel »).
 
   Chaque membre du Personnel est relié à un unique Utilisateur (relation 1-1) qui
   porte les informations communes : nom, prénom, email, etc.
 
   Attributs:
        id: Clé primaire auto-incrémentée (None tant que non inséré en base).
        poste: Intitulé du poste (50 caractères maximum), ex. « Responsable pédagogique ».
        date_prise_fonction: Date de prise de fonction.
        responsabilites: Liste de responsabilités, stockée en base au format JSON (liste vide par défaut).
        id_utilisateur: Clé étrangère vers utilisateur.id, unique (1 profil personnel au maximum par utilisateur).
        utilisateur: Objet Utilisateur lié, chargé via la relation.
   """
    # validate_assignment : revalide un champ à chaque affectation (p.poste = ...)
    model_config = pyd.ConfigDict(validate_assignment=True)
    # --- Colonnes de la table ---
    id: int | None                  = Field(default=None, primary_key=True)
    poste: str                      = Field(max_length=50)                 
    date_prise_fonction: dt.date    = Field(default_factory=lambda: dt.date.now(dt.timezone.utc), description="Date de prise de fonction du personnel")
    responsabilites: list[str]      = Field(default=[], sa_column=Column(JSON))
    id_utilisateur: int             = Field(unique=True, foreign_key="utilisateur.id")

    utilisateur: Utilisateur        = Relationship()

    def ajouter_personnel(engine, personnels):
        """Insère une liste de membres du personnel (et leurs utilisateurs liés) en base.

        Appel : Personnel.ajouter_personnel(engine, liste)

        Args:
            engine: Moteur SQLAlchemy connecté à la base.
            personnels: Liste d'objets Personnel, chacun avec son Utilisateur associé via `utilisateur=...`.

        Note:
            L'Utilisateur lié est ajouté automatiquement avec le Personnel.
        """
        with Session(engine) as session:
            session.add_all(personnels)       # 1. on confie l'objet à la session (rien n'est encore écrit)
            session.commit()        # 2. la session envoie l'INSERT et valide la transaction
            for personnel in personnels:
                session.refresh(personnel)   # 3. on recharge l'objet depuis la base, pour récupérer son id



    def afficher_personnel(engine):
        """Affiche tout le personnel dans un tableau aligné (console).
 
        Appel : Personnel.afficher_personnel(engine)

        Le tableau fusionne les colonnes de l'Utilisateur (id, nom, prénom, email, date de création, état actif) 
        et celles du Personnel (poste, date de prise de fonction, responsabilités).

        Args:
            engine: Moteur SQLAlchemy connecté à la base.
        """

        with Session(engine) as session:

            print(f"\nPersonnel : ")
            a_exclure_du_role = ["responsabilites"] # Colonne(s) spécifique au role à retirer du résultat
            
            a_exclure = {"utilisateur", "id", "id_utilisateur"} | set(a_exclure_du_role)

            requete = select(__class__).options(joinedload(__class__.utilisateur))
            personnes = session.exec(requete).all()

            if not personnes:
                print("Aucune donnée.")
                return

            # Extraction et filtrage des colonnes du role
            cols_personne = list(type(personnes[0]).model_fields)
            cols_personne = [colonne for colonne in cols_personne if colonne not in a_exclure]
            
            # Extraction des colonnes de l'Utilisateur lié
            cols_utilisateur = list(type(personnes[0].utilisateur).model_fields)
            
            # En-têtes complets (convertis en majuscules pour le style)
            en_tetes = [colonne.upper() for colonne in (cols_utilisateur + cols_personne)]
            # Extraction et formatage des données
            lignes = []
            for personne in personnes:
                ligne = []
                
                # Données de l'utilisateur
                for colonne in cols_utilisateur:
                    valeur = getattr(personne.utilisateur, colonne, "N/A") if personne.utilisateur else "N/A"
                    if isinstance(valeur, (dt.date, dt.datetime)):
                        valeur = valeur.strftime("%Y-%m-%d")
                    ligne.append(valeur)
                
                # Données spécifiques au role
                for colonne in cols_personne:
                    valeur = getattr(personne, colonne, "N/A")
                    if isinstance(valeur, (dt.date, dt.datetime)):
                        valeur = valeur.strftime("%Y-%m-%d")
                    ligne.append(valeur)
                    
                lignes.append(ligne)

            # Affichage propre avec tabulate
            print("\n" + tabulate.tabulate(lignes, headers=en_tetes, tablefmt="rounded", missingval="N/A"))