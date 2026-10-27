from pydantic import BaseModel, EmailStr, Field
import datetime as dt


class Apprenant(BaseModel):
   """

   """
   id: int                                #INT NOT NULL AUTO_INCREMENT
   poste: str                             #VARCHAR(50) NOT NULL
   date_naissance: dt.date                #DATE NOT NULL CHECK(date_naissance >= 16)
   niveau_etude: str                      #VARCHAR(50)
   telephone: str                         #CHAR(10)
   date_inscription_plateforme: dt.date   #DATETIME NOT NULL
   certification_obtenue: str             #VARCHAR(100)
   id_utilisateur: int                    #INT NOT NULL AUTO_INCREMENT NOT NULL
   # PRIMARY KEY(id),
   # UNIQUE(id_utilisateur),
   # UNIQUE(poste),
   # FOREIGN KEY(id_utilisateur) REFERENCES Utilisateur(id)
