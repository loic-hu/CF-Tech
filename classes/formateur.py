"""Modèle Formateur (table SQL + objet Python) du projet CF-Tech.
 
Ce module définit la classe Formateur, reliée à la table « utilisateur » par
une relation 1-1 (id_utilisateur). Les informations communes (nom, prénom,
email...) sont dans l'Utilisateur associé, accessible via `formateur.utilisateur`.
"""

from sqlmodel             import Field, Relationship, Session, SQLModel, col, create_engine, func, or_, select, Column, JSON
from sqlalchemy.orm       import joinedload

from tabulate             import tabulate
from decimal              import Decimal

from classes.utilisateur  import Utilisateur

import pydantic   as pyd
import datetime   as dt


class Formateur(SQLModel, table=True):
   """Profil formateur de la plateforme (table « formateur »).
 
   Cette classe n'hérite pas de Utilisateur en Python : elle a sa propre table,
   reliée à celle de l'utilisateur par la clé étrangère `id_utilisateur`
   (relation 1-1).
 
   Attributs:
      id: Clé primaire auto-incrémentée (None tant que non inséré en base).
      specialite: Spécialité du formateur (50 caractères maximum), ex.
         « Data Science ». Unique : deux formateurs ne peuvent pas avoir la
         même spécialité.
      date_embauche: Date d'embauche (aujourd'hui par défaut). Ne peut pas être
         dans le futur.
      taux_horaire: Taux horaire en euros, positif ou nul (10 chiffres au
         maximum, dont 2 décimales).
      bio: Biographie facultative (255 caractères maximum).
      id_utilisateur: Clé étrangère vers utilisateur.id, unique (1 profil
         formateur au maximum par utilisateur).
      utilisateur: Objet Utilisateur lié, chargé via la relation.
   """
   # validate_assignment : revalide un champ à chaque affectation (f.taux_horaire = ...)
   # use_enum_values     : stocke la valeur d'un Enum (sans effet ici : aucun champ Enum)
   # Attention : un modèle table=True ne valide pas les données à la création
   # de l'objet ; cette validation se fait dans les schémas Pydantic.
   model_config = pyd.ConfigDict(validate_assignment=True, use_enum_values=True)

   # --- Colonnes de la table ---
   id: int | None              = Field(default=None, primary_key=True, description="")            
   specialite: str             = Field(unique=True, max_length=50, description="")
   date_embauche: dt.date      = Field(default_factory=dt.date.today, description="Date d'embauche du formateur (doit être passée ou présente)")
   taux_horaire: Decimal       = Field(max_digits=10, decimal_places=2, ge=0, description="")
   bio: str | None             = Field(default=None, max_length=255, description="Biographie optionnelle")
   # Clé étrangère (colonne en base) : une valeur unique = relation 1-1
   id_utilisateur: int         = Field(unique=True, foreign_key="utilisateur.id", description="Identifiant unique de l'utilisateur")
   # Relation (pas une colonne) : donne accès à l'objet Utilisateur complet
   utilisateur: Utilisateur    = Relationship()


   @pyd.field_validator("date_embauche")
   @classmethod
   def valider_date_pas_dans_le_futur(cls, valeur: dt.date) -> dt.date:
      """Vérifie que la date d'embauche n'est pas dans le futur.
 
      Args:
         valeur: Date d'embauche à contrôler.
 
      Returns:
         La date inchangée si elle est valide.
 
      Raises:
         ValueError: si la date est postérieure à aujourd'hui.
 
      Note:
         Sur ce modèle table=True, le validator s'exécute à l'affectation d'un
         champ, pas à la création de l'objet. Pour bloquer une mauvaise date
         avant l'insertion, il faut aussi le placer dans un schéma Pydantic.
      """
      if valeur > dt.date.today():
         raise ValueError("La date d'embauche ne peut pas être dans le futur.")
      return valeur

   
   def ajouter_formateurs(engine, personnes:list):
      """
      Ajouter un ou des formateur(s) à partir d'une liste d'instance(s)
 
      Appel : Formateur.ajouter_formateurs(engine, liste)
 
      Args:
         engine: Moteur SQLAlchemy connecté à la base.
         personnes: Liste d'objets Formateur, chacun avec son Utilisateur
            associé via `utilisateur=...` (ajouté automatiquement avec le Formateur).
      """
      with Session(engine) as session:
         session.add_all(personnes)         # On confie l'objet à la session (rien n'est encore écrit)
         session.commit()                   # La session envoie l'INSERT et valide la transaction
         for personne in personnes:
               session.refresh(personne)    # On recharge l'objet depuis la base, pour récupérer son id


   def afficher_formateurs(engine):
      """
      Affiche une liste de formateurs et leurs données utilisateur 
      sous forme de tableau propre avec tabulate.
 
      Appel : Formateur.afficher_formateurs(engine)
 
      Le tableau fusionne les colonnes de l'Utilisateur (en premier) et celles
      du Formateur (spécialité, date d'embauche, taux horaire). La biographie
      est masquée.
 
      Args:
         engine: Moteur SQLAlchemy connecté à la base.
      """
      with Session(engine) as session:

         print(f"\nFormateurs : ")
         a_exclure_du_role = ["bio"] # Colonne(s) spécifique au role à retirer du résultat

         # Colonnes masquées : la relation, les deux id (doublons d'affichage) et la bio
         a_exclure = {"utilisateur", "id", "id_utilisateur"} | set(a_exclure_du_role)

         # joinedload : charge l'utilisateur dans la même requête (JOIN),
         # ce qui évite une requête supplémentaire par formateur
         requete = select(__class__).options(joinedload(__class__.utilisateur))
         personnes = session.exec(requete).all()

         # Rien à afficher si la table est vide
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
