from pydantic import BaseModel ,EmailStr, Field
import datetime as dt

class Utilisateur(BaseModel):
    """
    
    """
    id: int                 #INT NOT NULL AUTO_INCREMENT #PRIMARY KEY(id)
    nom: str                #VARCHAR(50) NOT NULL
    prenom: str             #VARCHAR(50) NOT NULL
    email: EmailStr         #VARCHAR(100) NOT NULL #UNIQUE(email)
    date_creation: dt.datetime = Field(default_factory=dt.date.today, description="Date à la création de l'utilisateur") #DATETIME NOT NULL
    est_actif: bool            = Field(default=True, description="Etat actif du compte")        #LOGICAL NOT NULL


   

user = Utilisateur(id=1, nom="HURBLAIN", prenom="Loïc", email="loic.hurblain@gmail.com")




















