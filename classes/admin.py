from sqlmodel             import Field, Relationship, Session, SQLModel, col, create_engine, func, or_, select, Column, JSON
from sqlalchemy.orm       import joinedload

from tabulate             import tabulate
from decimal              import Decimal

from classes.utilisateur  import Utilisateur

import pydantic   as pyd
import datetime   as dt

from enum import Enum


class AccesAdmin(str, Enum):
    SUPERADMIN = 'SUPERADMIN'
    ADMIN      = 'ADMIN'

    def __str__(self):
        return self.value


class Admin(SQLModel, table=True):
   """

   """
   # FORCE la validation stricte de Pydantic v2 dès la création de l'objet
   model_config = pyd.ConfigDict(validate_assignment=True, use_enum_values=True)

   id: int | None              = Field(default=None, primary_key=True)
   niveau_acces: AccesAdmin    = Field(description="Quel niveau de droits a cet admin")
   date_promotion: dt.date     = Field(description="")     #DATE NOT NULL
   id_utilisateur: int         = Field(unique=True, foreign_key="utilisateur.id", description="Identifiant unique de l'utilisateur")
   utilisateur: Utilisateur    = Relationship()

   
   def ajouter_admins(engine, personnes):
      """
      Ajouter un ou des admin(s) à partir d'une liste d'instance(s)
      """
      with Session(engine) as session:
         session.add_all(personnes)         # 1. on confie l'objet à la session (rien n'est encore écrit)
         session.commit()                   # 2. la session envoie l'INSERT et valide la transaction
         for personne in personnes:
               session.refresh(personne)    # 3. on recharge l'objet depuis la base, pour récupérer son id


   def afficher_admins(engine):
      """
      Affiche la liste des admins et leurs données utilisateur 
      sous forme de tableau propre avec tabulate.
      """
      with Session(engine) as session:
         print(f"\nAdmins :")

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