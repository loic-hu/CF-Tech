from pydantic import BaseModel ,EmailStr, Field
import datetime as dt
from enum import Enum

class StatutSession(str, Enum):
    OUVERTE  = 'OUVERTE'
    FERMEE   = 'FERMEE'
    ARCHIVEE = 'ARCHIVEE'

class Session(BaseModel):
   
    id: int                                        #INT NOT NULL AUTO_INCREMENT,
    titre: str                                     #VARCHAR(100) NOT NULL,
    description: str                               #VARCHAR(255),
    date_debut: dt.datetime                        #DATETIME NOT NULL,
    date_fin: dt.datetime                          #DATETIME NOT NULL CHECK(date_debut < date_fin),
    capacite_max: str                              #VARCHAR(50) NOT NULL /*CHECK(<=salle.capacite)*/,
    statut: StatutSession = StatutSession.OUVERTE  #ENUM ('OUVERTE', 'FERMEE', 'ARCHIVEE') DEFAULT 'OUVERTE' NOT NULL,
    id_formateur: int                              #INT NOT NULL AUTO_INCREMENT NOT NULL,
    id_salle: int                                  #INT NOT NULL AUTO_INCREMENT NOT NULL,
    # PRIMARY KEY(id),
    # FOREIGN KEY(id_formateur) REFERENCES Formateur(id),
    # FOREIGN KEY(id_salle) REFERENCES Salle(id)
