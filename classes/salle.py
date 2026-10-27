from pydantic import BaseModel

class Salle(BaseModel):
   id: int              #NOT NULL AUTO_INCREMENT
   nom: str             #NOT NULL
   capacite: int        #NOT NULL CHECK(capacite > 0)
   localisation: str    #NOT NULL
   equipements: str
   # PRIMARY KEY(id),
   # UNIQUE(nom)
