from pydantic import BaseModel ,EmailStr, Field
import datetime as dt
from enum import Enum


class StatutInscription(str, Enum):
    SUPERADMIN = 'SUPERADMIN'
    ADMIN      = 'ADMIN'


class Admin(BaseModel):
   """

   """
   id: int                          #INT NOT NULL AUTO_INCREMENT
   niveau_acces: StatutInscription  #ENUM ('SUPERADMIN', 'ADMIN') NOT NULL
   date_promotion: dt.date          #DATE NOT NULL
   id_utilisateur: int              #INT NOT NULL AUTO_INCREMENT NOT NULL
   # FOREIGN KEY(id_utilisateur) REFERENCES Utilisateur(id),
   # PRIMARY KEY(id),
   # UNIQUE(id_utilisateur)
