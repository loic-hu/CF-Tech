from sqlmodel import Field, Relationship, Session, SQLModel, col, create_engine, func, or_, select, Column, JSON
from sqlalchemy.orm import joinedload

from decimal              import Decimal
from classes.utilisateur  import Utilisateur

import pydantic   as pyd
import datetime   as dt


class Formateur(SQLModel, table=True):
   """
   
   """
   # FORCE la validation stricte de Pydantic v2 dès la création de l'objet
   model_config = pyd.ConfigDict(validate_assignment=True, use_enum_values=True)

   id: int | None              = Field(default=None, primary_key=True, description="")             #INT NOT NULL AUTO_INCREMENT, PRIMARY KEY(id), UNIQUE(id_utilisateur),
   specialite: str             = Field(unique=True, max_length=50, description="")                 #VARCHAR(50) NOT NULL, UNIQUE(specialite),
   date_embauche: dt.date      = Field(default_factory=lambda: dt.date.today(), description="")    #DATE NOT NULL -- (<= date du jour).,
   taux_horaire: Decimal       = Field(max_digits=10, decimal_places=2, ge=0, description="")      #DECIMAL(10,2) NOT NULL CHECK(taux_horaire >= 0),
   bio: str | None             = Field(default=None, max_length=255, description="Biographie optionnelle")
   id_utilisateur: int         = Field(unique=True, foreign_key="utilisateur.id", description="Identifiant unique de l'utilisateur")
   utilisateur: Utilisateur    = Relationship()

   
   def ajouter_formateurs(engine, personnes:list):
      """
      Ajouter un ou des formateur(s) à partir d'une liste d'instance(s)
      """
      with Session(engine) as session:
         session.add_all(personnes)         # 1. on confie l'objet à la session (rien n'est encore écrit)
         session.commit()                    # 2. la session envoie l'INSERT et valide la transaction
         for personne in personnes:
               session.refresh(personne)    # 3. on recharge l'objet depuis la base, pour récupérer son id


   def afficher_formateurs(engine):
      """
      Affiche une liste de formateurs et leurs données utilisateur 
      sous forme de tableau aligné.
      """
      with Session(engine) as session:

         requete = (
            select(__class__)
            .options(joinedload(__class__.utilisateur))
         ) 

         personnes = session.exec(requete).all()

         if not personnes:
            print("Aucune donnée.")
            return

         # 1. On récupère les colonnes du Formateur ET de l'Utilisateur lié
         cols_personne = list(type(personnes[0]).model_fields)
         # On exclut 'utilisateur' (qui est la relation) et 'id_utilisateur' pour éviter les doublons d'affichage
         if "utilisateur" in cols_personne: cols_personne.remove("utilisateur")
         if "id" in cols_personne: cols_personne.remove("id")
         if "id_utilisateur" in cols_personne: cols_personne.remove("id_utilisateur")
         if "bio" in cols_personne: cols_personne.remove("bio")
                  
         # On ajoute les colonnes de l'utilisateur (en excluant son id)
         #cols_utilisateur = ["id", "nom", "prenom", "email", "date_creation", "est_actif"]
         cols_utilisateur = list(type(personnes[0].utilisateur).model_fields)
         
         # En-tête complet du tableau
         colonnes = cols_utilisateur + cols_personne

         # 2. Extraction des valeurs pour chaque ligne
         lignes = []
         for f in personnes:
            ligne = []
            # Valeurs de l'utilisateur lié (via la Relationship)
            for c in cols_utilisateur:
                  valeur = getattr(f.utilisateur, c, "N/A") if hasattr(f, "utilisateur") and f.utilisateur else "N/A"
                  # Formatage propre si c'est une date ou un datetime
                  if isinstance(valeur, (dt.date, dt.datetime)):
                     valeur = valeur.strftime("%Y-%m-%d")
                  ligne.append(str(valeur))
            
            # Valeurs spécifiques au formateur
            for c in cols_personne:
                  valeur = getattr(f, c)
                  if isinstance(valeur, (dt.date, dt.datetime)):
                     valeur = valeur.strftime("%Y-%m-%d")
                  ligne.append(str(valeur))
                  
            lignes.append(ligne)

         # 3. Calcul de la largeur de chaque colonne (votre logique d'origine conservée)
         largeurs = [max(len(c), *(len(l[i]) for l in lignes))
                     for i, c in enumerate(colonnes)]

         # 4. Affichage à l'écran
         print("\n" + "  ".join(c.upper().ljust(w) for c, w in zip(colonnes, largeurs)))
         print("-" * (sum(largeurs) + (len(largeurs) * 2))) # Ligne de séparation
         for l in lignes:
            print("  ".join(v.ljust(w) for v, w in zip(l, largeurs)))