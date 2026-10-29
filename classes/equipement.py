from sqlmodel import Field, Relationship, Session, SQLModel, select
from sqlalchemy.orm import joinedload
from classes.salle import Salle

import pydantic as pyd
import datetime as dt


class Equipement(SQLModel, table=True):
   model_config = pyd.ConfigDict(validate_assignment=True)
   
   id: int | None          = Field(default=None, primary_key=True)
   nom: str                = Field(max_length=50)
   description: str | None = Field(default=None, max_length=255, description="Description optionnelle")
   salle_id: int | None    = Field(default=None, foreign_key="salle.id")

   salle: Salle | None     = Relationship()

   def ajouter_equipement(engine, equipements):
       """Insère une liste d'équipements en base."""
       with Session(engine) as session:
           session.add_all(equipements)
           session.commit()
           for equipement in equipements:
               session.refresh(equipement)

   def afficher_equipement(engine):
       """Affiche tout l'équipement dans un tableau aligné (console)."""
       with Session(engine) as session:
           requete = (
               select(Equipement)
               .options(joinedload(Equipement.salle))
           ) 
           equipements = session.exec(requete).all()

       if not equipements:
           print("Aucune donnée.")
           return
       
       # 1. On récupère les colonnes de l'Equipement
       cols_equipement = list(type(equipements[0]).model_fields)
       if "salle" in cols_equipement: cols_equipement.remove("salle")
       if "id" in cols_equipement: cols_equipement.remove("id")
       if "salle_id" in cols_equipement: cols_equipement.remove("salle_id")
                       
       # Colonnes de la salle récupérées directement depuis la classe Salle (évite le NoneType)
       cols_salle = list(Salle.model_fields)
               
       colonnes = cols_salle + cols_equipement
       
       # 2. Extraction des valeurs pour chaque ligne
       lignes = []
       for f in equipements:  # Correction : on parcourt bien les objets de la liste
           ligne = []
           # Valeurs de la salle liée (si elle existe)
           for c in cols_salle:
               valeur = getattr(f.salle, c, "N/A") if f.salle else "N/A"
               if isinstance(valeur, (dt.date, dt.datetime)):
                   valeur = valeur.strftime("%Y-%m-%d")
               ligne.append(str(valeur))
                   
           # Valeurs spécifiques à l'équipement
           for c in cols_equipement:
               valeur = getattr(f, c)
               if isinstance(valeur, (dt.date, dt.datetime)):
                   valeur = valeur.strftime("%Y-%m-%d")
               ligne.append(str(valeur))
                       
           lignes.append(ligne)
       
       # 3. Calcul de la largeur de chaque colonne
       largeurs = [max(len(c), *(len(l[i]) for l in lignes))
                   for i, c in enumerate(colonnes)]
       
       # 4. Affichage à l'écran
       print("\n" + "  ".join(c.upper().ljust(w) for c, w in zip(colonnes, largeurs)))
       print("-" * (sum(largeurs) + (len(largeurs) * 2)))
       for l in lignes:
           print("  ".join(v.ljust(w) for v, w in zip(l, largeurs)))