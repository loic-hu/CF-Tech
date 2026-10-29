"""Modèle Apprenant (table SQL + objet Python) du projet CF-Tech.
 
Ce module définit :
    - NiveauEtude : l'énumération des niveaux d'études possibles ;
    - Apprenant   : la table « apprenant », reliée à la table « utilisateur »
                    par une relation 1-1 (id_utilisateur).
 
Un Apprenant ne contient pas nom, prénom ni email : ces données sont dans
l'utilisateur associé, accessible via la relation `apprenant.utilisateur`.
"""

from sqlmodel import Field, Relationship, Session, SQLModel, col, create_engine, func, or_, select
from sqlalchemy.orm import joinedload

from classes.utilisateur  import Utilisateur

import pydantic   as pyd
import datetime   as dt

from enum import Enum
from tabulate import tabulate

class NiveauEtude(str, Enum):
   """Niveaux d'études possibles pour un apprenant.
 
   Hérite de `str` pour pouvoir être comparé et affiché comme une chaîne.
   Le nom du membre (ex. BAC_3) sert dans le code, la valeur (ex. "Bac+3")
   est ce qui s'affiche.
   """
   BAC   = "Bac"
   BAC_2 = "Bac+2"
   BAC_3 = "Bac+3"
   BAC_5 = "Bac+5"

   def __str__(self):
      """Retourne la valeur (ex. "Bac+3") plutôt que "NiveauEtude.BAC_3"."""
      return self.value

class Apprenant(SQLModel, table=True):
   """Profil d'un apprenant de la plateforme (table « apprenant »).
 
   Chaque apprenant est relié à un unique Utilisateur (relation 1-1) qui
   porte les informations communes : nom, prénom, email, etc.
 
   Attributs:
      id: Clé primaire auto-incrémentée (None tant que non inséré en base).
      date_naissance: Date de naissance. L'âge minimal de 16 ans est vérifié dans le schéma Pydantic, pas dans cette table. ###
      niveau_etude: Niveau d'études (énumération NiveauEtude), facultatif.
      telephone: Numéro à 10 chiffres, facultatif. Le format exact (regex) est vérifié dans le schéma Pydantic. ###
      date_inscription_plateforme: Date et heure d'inscription (UTC), remplie automatiquement à la création de l'objet.
      certification_obtenue: Certification obtenue, facultatif.
      id_utilisateur: Clé étrangère vers utilisateur.id, unique (1 profil apprenant au maximum par utilisateur).
      utilisateur: Objet Utilisateur lié, chargé via la relation.
   """
   # validate_assignment : revalide un champ à chaque affectation (a.telephone = ...)
   # use_enum_values     : stocke la valeur de l'Enum (ex. "Bac+3") et non le membre
   model_config = pyd.ConfigDict(validate_assignment=True, use_enum_values=True)

   # --- Colonnes de la table ---
   id: int | None                            = Field(default=None, primary_key=True)
   date_naissance: dt.date                   = Field(description="Date de naissance (≥ 16 ans)")  
   niveau_etude: NiveauEtude | None          = Field(default=None, description="Bac, Bac+2, ...")
   telephone: str | None                     = Field(default=None, min_length=10, max_length=10, description="Numéro à 10 chiffres")
   date_inscription_plateforme: dt.datetime  = Field(default_factory=lambda: dt.datetime.now(dt.timezone.utc), description="Date à la création de l'utilisateur")
   certification_obtenue: str | None         = Field(default=None, max_length=100, description="Certification obtenue")
   # --- Lien avec la table utilisateur ---
   # Clé étrangère (colonne en base) : une valeur unique = relation 1-1
   id_utilisateur: int                       = Field(foreign_key="utilisateur.id", unique=True, description="Lien vers id de Utilisateur") 
   # Relation (pas une colonne) : donne accès à l'objet Utilisateur complet
   utilisateur: Utilisateur                  = Relationship()

   @pyd.field_validator("date_naissance")
   @classmethod
   def verif_date_naissance(cls, v: dt.date) -> dt.date:
      """Vérifie que l'apprenant a au moins 16 ans."""
      aujourdhui = dt.date.today()
      # age = différence des années, moins 1 si l'anniversaire n'est pas encore passé cette année
      age = aujourdhui.year - v.year - ((aujourdhui.month, aujourdhui.day) < (v.month, v.day))
      if age < 16:
         raise ValueError("L'apprenant doit avoir au moins 16 ans")
      return v
   
   def ajouter_apprenant(engine,apprenants):
      """Insère une liste d'apprenants (et leurs utilisateurs liés) en base.
 
      Appel : Apprenant.ajouter_apprenant(liste, engine)
 
      Args:
         apprenants: Liste d'objets Apprenant, 
            chacun avec son Utilisateur associé via `utilisateur=...`.
         engine: Moteur SQLAlchemy connecté à la base.
 
      Note:
         L'utilisateur lié est ajouté automatiquement avec l'Apprenant.
      """
      with Session(engine) as session:
         session.add_all(apprenants)         # on confie l'objet à la session (rien n'est encore écrit)
         session.commit()                    # la session envoie l'INSERT et valide la transaction
         for apprenant in apprenants:
            session.refresh(apprenant)    # on recharge l'objet depuis la base, pour récupérer son id
               
   def afficher(engine):
      """Affiche tous les apprenants dans un tableau aligné (console).
 
      Appel : Apprenant.afficher(engine)
 
      Le tableau fusionne les colonnes de l'utilisateur (id, nom, prénom,email, date de création, état actif) 
         et celles de l'apprenant (date de naissance, niveau d'études, téléphone, etc.).
 
      Args:
         engine: Moteur SQLAlchemy connecté à la base.
      """
      with Session(engine) as session:

         print(f"\nApprenants : ")
         a_exclure_du_role = [] # Colonne(s) spécifique au role à retirer du résultat
         
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
         print("\n" + tabulate(lignes, headers=en_tetes, tablefmt="rounded", missingval="N/A"))
