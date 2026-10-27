from pydantic import BaseModel ,EmailStr, Field
import datetime as dt
from enum import Enum


class StatutInscription(str, Enum):
    ENREGISTRE = 'ENREGISTRE'
    DESINSCRIT = 'DESINSCRIT'
    EN_ATTENTE = 'EN_ATTENTE'


class Inscription(BaseModel):
    """
    
    """
    id: int                               #INT NOT NULL AUTO_INCREMENT,
    date_inscription: dt.datetime         #DATETIME NOT NULL,
    statut_inscription: StatutInscription #ENUM (ENREGISTRE, 'DESINSCRIT', 'EN_ATTENTE') NOT NULL,
    presence: bool                        #LOGICAL,
    id_apprenant: int                     #INT NOT NULL AUTO_INCREMENT NOT NULL,
    id_session: int                       #INT NOT NULL AUTO_INCREMENT NOT NULL,
    # PRIMARY KEY(id),
    # FOREIGN KEY(id_apprenant) REFERENCES Apprenant(id),
    # FOREIGN KEY(id_session) REFERENCES Session(id)
