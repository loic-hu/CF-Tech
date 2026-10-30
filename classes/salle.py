"""Modèle Salle (table SQL + objet Python) du projet CF-Tech.
 
Ce module définit la classe Salle : une salle de formation avec son nom, sa
capacité et sa localisation. Les sessions de formation y sont planifiées
(voir SessionFormation) et les équipements y sont rattachés (voir Equipement).
"""

from sqlmodel import Field, Relationship, Session, SQLModel, col, create_engine, func, or_, select, Column, JSON
from sqlalchemy.orm import joinedload


import pydantic   as pyd
import datetime   as dt

class Salle(SQLModel, table=True):
   """Salle de formation (table « salle »).
 
   Attributs:
      id: Clé primaire auto-incrémentée (None tant que non inséré en base).
      nom: Nom de la salle (50 caractères maximum), unique, ex. « Salle A101 ».
      capacite: Nombre maximal de places, strictement positif.
      localisation: Emplacement de la salle (100 caractères maximum), ex.
         « Bâtiment Nord, 1er étage ».
   """
   # validate_assignment : revalide un champ à chaque affectation (s.capacite = ...)
   # Attention : un modèle table=True ne valide pas les données à la création
   # de l'objet ; cette validation se fait dans les schémas Pydantic.
   model_config = pyd.ConfigDict(validate_assignment=True)

   id: int | None       = Field(default=None, primary_key=True)
   nom: str             = Field(max_length=50, unique=True, description="Nom de la salle")
   capacite: int        = Field(gt=0, description="Capacité maximale (doit être > 0)")
   localisation: str    = Field(max_length=100, description="Localisation de la salle")

   def ajouter_salles(engine, salles):
      """Insère une liste de salles en base.
 
      Appel : Salle.ajouter_salles(engine, liste)
 
      Args:
         engine: Moteur SQLAlchemy connecté à la base.
         salles: Liste d'objets Salle à insérer.
 
      Raises:
         sqlalchemy.exc.IntegrityError: si un nom de salle existe déjà
            (contrainte d'unicité sur `nom`).
      """
      # Insertion des salles en base
      with Session(engine) as session:
         session.add_all(salles)
         session.commit()
         for salle in salles:
            session.refresh(salle)
