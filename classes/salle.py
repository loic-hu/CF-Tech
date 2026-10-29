from sqlmodel import Field, Relationship, Session, SQLModel, col, create_engine, func, or_, select, Column, JSON
from sqlalchemy.orm import joinedload


import pydantic   as pyd
import datetime   as dt

class Salle(SQLModel, table=True):
   """
   
   """
   model_config = pyd.ConfigDict(validate_assignment=True)

   id: int | None       = Field(default=None, primary_key=True)
   nom: str             = Field(max_length=50, unique=True, description="Nom de la salle")
   capacite: int        = Field(gt=0, description="Capacité maximale (doit être > 0)")
   localisation: str    = Field(max_length=100, description="Localisation de la salle")

   def ajouter_salles(engine, salles):
      # Insertion des salles en base
      with Session(engine) as session:
         session.add_all(salles)
         session.commit()
         for salle in salles:
            session.refresh(salle)
