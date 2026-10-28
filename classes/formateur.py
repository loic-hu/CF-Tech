
from sqlmodel import Field, Relationship, Session, SQLModel, col, create_engine, func, or_, select
from sqlalchemy.orm import joinedload

from decimal              import Decimal
from classes.utilisateur  import Utilisateur

import pydantic   as pyd
import datetime   as dt


class Formateur(SQLModel, table=True):
   """
   Formateur est une classe enfant de Utilisateur
   """
   # FORCE la validation stricte de Pydantic v2 dès la création de l'objet
   model_config = pyd.ConfigDict(validate_assignment=True)

   id: int | None              = Field(default=None, primary_key=True)             #INT NOT NULL AUTO_INCREMENT, PRIMARY KEY(id), UNIQUE(id_utilisateur),
   specialite: str             = Field(unique=True, max_length=50)                 #VARCHAR(50) NOT NULL, UNIQUE(specialite),
   date_embauche: dt.date      = Field(default_factory=lambda: dt.date.today())    #DATE NOT NULL -- (<= date du jour).,
   taux_horaire: Decimal       = Field(max_digits=10, decimal_places=2, ge=0)      #DECIMAL(10,2) NOT NULL CHECK(taux_horaire >= 0),
   bio: str | None             = Field(default=None, max_length=255)               #VARCHAR(255),
   id_utilisateur: int         = Field(unique=True, foreign_key="utilisateur.id")  #INT NOT NULL AUTO_INCREMENT NOT NULL, FOREIGN KEY(id_utilisateur) REFERENCES Utilisateur(id)

   utilisateur: Utilisateur    = Relationship()

   
   def ajouter_formateurs(engine, formateurs):
      """
      
      """
      with Session(engine) as session:
         session.add_all(formateurs)         # 1. on confie l'objet à la session (rien n'est encore écrit)
         session.commit()                    # 2. la session envoie l'INSERT et valide la transaction
         for formateur in formateurs:
               session.refresh(formateur)    # 3. on recharge l'objet depuis la base, pour récupérer son id

         requete = select(Formateur).options(joinedload(Formateur.utilisateur))
         
         formateur = session.exec(requete).all()


   def afficher_formateurs(engine):
      """
      Affiche une liste de formateurs et leurs données utilisateur 
      sous forme de tableau aligné.
      """
      with Session(engine) as session:
         requete = (
            select(Formateur)
            .options(joinedload(Formateur.utilisateur))
         ) 

         formateurs = session.exec(requete).all()


         if not formateurs:
            print("Aucune donnée.")
            return

         # 1. On récupère les colonnes du Formateur ET de l'Utilisateur lié
         cols_formateur = list(type(formateurs[0]).model_fields)
         # On exclut 'utilisateur' (qui est la relation) et 'id_utilisateur' pour éviter les doublons d'affichage
         if "utilisateur" in cols_formateur: cols_formateur.remove("utilisateur")
         if "id" in cols_formateur: cols_formateur.remove("id")
         if "id_utilisateur" in cols_formateur: cols_formateur.remove("id_utilisateur")
         if "bio" in cols_formateur: cols_formateur.remove("bio")
                  
         
         # On ajoute les colonnes de l'utilisateur (en excluant son id)
         cols_utilisateur = ["id", "nom", "prenom", "email", "date_creation", "est_actif"]
         
         # En-tête complet du tableau
         colonnes = cols_utilisateur + cols_formateur

         # 2. Extraction des valeurs pour chaque ligne
         lignes = []
         for f in formateurs:
            ligne = []
            # Valeurs de l'utilisateur lié (via la Relationship)
            for c in cols_utilisateur:
                  valeur = getattr(f.utilisateur, c, "N/A") if hasattr(f, "utilisateur") and f.utilisateur else "N/A"
                  # Formatage propre si c'est une date ou un datetime
                  if isinstance(valeur, (dt.date, dt.datetime)):
                     valeur = valeur.strftime("%Y-%m-%d")
                  ligne.append(str(valeur))
            
            # Valeurs spécifiques au formateur
            for c in cols_formateur:
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