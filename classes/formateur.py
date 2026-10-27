from pydantic import BaseModel
from decimal import Decimal
import datetime     as dt
import utilisateur  as u

class Formateur(u.Utilisateur):
   """
   
   """
   id: int                 #NOT NULL AUTO_INCREMENT
   nom: str                #NOT NULL
   specialite: str         #NOT NULL
   date_embauche: dt.date  #NOT NULL
   taux_horaire: Decimal   #NOT NULL CHECK (taux_horaie > 0)
