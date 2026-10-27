from pydantic import BaseModel ,EmailStr, Field
import datetime as dt


class Personnel(BaseModel):
    """"
    
    """
    id: int                         #NOT NULL AUTO_INCREMENT
    poste: str                      #NOT NULL
    date_prise_fonction: dt.date    #NOT NULL
    responsabilites: str            #JSON
    # PRIMARY KEY(id),
    # UNIQUE(id_utilisateur),
    # FOREIGN KEY(id_utilisateur) REFERENCES Utilisateur(id)