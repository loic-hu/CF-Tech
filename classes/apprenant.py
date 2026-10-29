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

from decimal              import Decimal
from classes.utilisateur  import Utilisateur

import pydantic   as pyd
import datetime   as dt

from enum import Enum

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
         # joinedload : charge l'utilisateur dans la même requête (JOIN),
         # ce qui évite une requête supplémentaire par apprenant
         requete = (
            select(Apprenant)
            .options(joinedload(Apprenant.utilisateur))
         ) 
         apprenants = session.exec(requete).all()

         # Rien à afficher si la table est vide
         if not apprenants:
            print("Aucune donnée.")
            return

         # 1. On récupère les colonnes du apprenant ET de l'utilisateur lié
         cols_apprenant = list(type(apprenants[0]).model_fields)

         # On exclut 'utilisateur' (qui est la relation) et 'id_utilisateur' pour éviter les doublons d'affichage
         if "utilisateur" in cols_apprenant: cols_apprenant.remove("utilisateur")
         if "id" in cols_apprenant: cols_apprenant.remove("id")
         if "id_utilisateur" in cols_apprenant: cols_apprenant.remove("id_utilisateur")
                  
         # Colonnes de l'utilisateur (id inclus : c'est l'id affiché en première colonne)
         cols_utilisateur = list(type(apprenants[0].utilisateur).model_fields)
         
         # En-tête complet du tableau : colonnes utilisateur d'abord, puis apprenant
         colonnes = cols_utilisateur + cols_apprenant

         # 2. Extraction des valeurs pour chaque ligne
         lignes = []
         for f in apprenants:
            ligne = []
            # Valeurs de l'utilisateur lié (via la Relationship)
            for c in cols_utilisateur:
                  # "N/A" si l'apprenant n'a pas d'utilisateur lié
                  valeur = getattr(f.utilisateur, c, "N/A") if hasattr(f, "utilisateur") and f.utilisateur else "N/A"
                  # Formatage propre si c'est une date ou un datetime
                  if isinstance(valeur, (dt.date, dt.datetime)):
                     valeur = valeur.strftime("%Y-%m-%d")
                  ligne.append(str(valeur))
            
            # Valeurs spécifiques au Apprenant
            for c in cols_apprenant:
                  valeur = getattr(f, c)
                  if isinstance(valeur, (dt.date, dt.datetime)):
                     valeur = valeur.strftime("%Y-%m-%d")
                  ligne.append(str(valeur))
            lignes.append(ligne)

         # 3. Calcul de la largeur de chaque colonne : valeur la plus longue, titre inclus
         largeurs = [max(len(c), *(len(l[i]) for l in lignes))
                     for i, c in enumerate(colonnes)]

         # 4. Affichage à l'écran
         print("\n" + "  ".join(c.upper().ljust(w) for c, w in zip(colonnes, largeurs)))
         print("-" * (sum(largeurs) + (len(largeurs) * 2))) # Ligne de séparation
         for l in lignes:
            print("  ".join(v.ljust(w) for v, w in zip(l, largeurs)))
      