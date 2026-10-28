from sqlmodel import Field, Relationship, Session, SQLModel, col, create_engine, func, or_, select
from sqlalchemy.orm import joinedload

from decimal              import Decimal
from classes.utilisateur  import Utilisateur

import pydantic   as pyd
import datetime   as dt

from enum import Enum

class NiveauEtude(str, Enum):
   BAC   = "Bac"
   BAC_2 = "Bac+2"
   BAC_3 = "Bac+3"
   BAC_5 = "Bac+5"

   def __str__(self):
        return self.value

class Apprenant(SQLModel, table=True):
   """

   """
   model_config = pyd.ConfigDict(validate_assignment=True, use_enum_values=True)

   id: int | None                            = Field(default=None, primary_key=True)
   date_naissance: dt.date                   = Field(description="Date de naissance (≥ 16 ans)")  
   niveau_etude: NiveauEtude | None          = Field(default=None, description="Bac, Bac+2, ...")
   telephone: str | None                     = Field(default=None, min_length=10, max_length=10, description="Numéro à 10 chiffres")
   date_inscription_plateforme: dt.datetime  = Field(default_factory=lambda: dt.datetime.now(dt.timezone.utc), description="Date à la création de l'utilisateur")
   certification_obtenue: str | None         = Field(default=None, max_length=100, description="Certification obtenue")
   id_utilisateur: int                       = Field(foreign_key="utilisateur.id", unique=True, description="Lien vers id de Utilisateur") 
   utilisateur: Utilisateur                  = Relationship()

   def afficher(engine):
      """
      
      """
      with Session(engine) as session:
         requete = (
            select(Apprenant)
            .options(joinedload(Apprenant.utilisateur))
         ) 
         apprenants = session.exec(requete).all()

         if not apprenants:
            print("Aucune donnée.")
            return

         # 1. On récupère les colonnes du Apprenant ET de l'Utilisateur lié
         cols_apprenant = list(type(apprenants[0]).model_fields)
         # On exclut 'utilisateur' (qui est la relation) et 'id_utilisateur' pour éviter les doublons d'affichage
         if "utilisateur" in cols_apprenant: cols_apprenant.remove("utilisateur")
         if "id" in cols_apprenant: cols_apprenant.remove("id")
         if "id_utilisateur" in cols_apprenant: cols_apprenant.remove("id_utilisateur")
                  
         # On ajoute les colonnes de l'utilisateur (en excluant son id)
         cols_utilisateur = list(type(apprenants[0].utilisateur).model_fields)
         
         # En-tête complet du tableau
         colonnes = cols_utilisateur + cols_apprenant

         # 2. Extraction des valeurs pour chaque ligne
         lignes = []
         for f in apprenants:
            ligne = []
            # Valeurs de l'utilisateur lié (via la Relationship)
            for c in cols_utilisateur:
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

         # 3. Calcul de la largeur de chaque colonne (votre logique d'origine conservée)
         largeurs = [max(len(c), *(len(l[i]) for l in lignes))
                     for i, c in enumerate(colonnes)]

         # 4. Affichage à l'écran
         print("\n" + "  ".join(c.upper().ljust(w) for c, w in zip(colonnes, largeurs)))
         print("-" * (sum(largeurs) + (len(largeurs) * 2))) # Ligne de séparation
         for l in lignes:
            print("  ".join(v.ljust(w) for v, w in zip(l, largeurs)))
      

   def ajouter_apprenant(apprenants, engine):
      """

      """
      with Session(engine) as session:
         session.add_all(apprenants)         # 1. on confie l'objet à la session (rien n'est encore écrit)
         session.commit()                    # 2. la session envoie l'INSERT et valide la transaction
         for apprenant in apprenants:
               session.refresh(apprenant)    # 3. on recharge l'objet depuis la base, pour récupérer son id
         requete = select(Apprenant).options(joinedload(Apprenant.utilisateur))
         apprenant = session.exec(requete).all()