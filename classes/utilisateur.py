import pydantic as pyd
from sqlalchemy.schema import CreateTable
import sqlmodel
from sqlmodel import Field, Relationship, Session, SQLModel, col, create_engine, func, or_, select
# from init_db import 

#from pydantic import BaseModel ,EmailStr, Field
import datetime as dt
from pathlib import Path

# from __init__ import *

class Utilisateur(SQLModel, table=True):
    """
    
    """
    # FORCE la validation stricte de Pydantic v2 dès la création de l'objet
    model_config = pyd.ConfigDict(validate_assignment=True)
    
    id: int | None             = Field(default=None, primary_key=True) #INT NOT NULL AUTO_INCREMENT #PRIMARY KEY(id)
    nom: str                   = Field(max_length=50) #VARCHAR(50) NOT NULL
    prenom: str                = Field(max_length=50) #VARCHAR(50) NOT NULL
    email: pyd.EmailStr        = Field(unique=True, max_length=100) #VARCHAR(100) NOT NULL #UNIQUE(email)
    date_creation: dt.datetime = Field(default_factory=lambda: dt.datetime.now(dt.timezone.utc), description="Date à la création de l'utilisateur") #DATETIME NOT NULL
    est_actif: bool            = Field(default=True, description="Etat actif du compte")        #LOGICAL NOT NULL


    def afficher(utilisateurs):
        """
        
        """
        for p in utilisateurs:
            print(f"{p.id:>3} | {p.nom:<10} | {p.prenom:<10} | {p.email}")


    def ajouter_utilisateurs(utilisateurs, engine):
        """
        
        """
        with Session(engine) as session:
            session.add_all(utilisateurs)       # 1. on confie l'objet à la session (rien n'est encore écrit)
            session.commit()        # 2. la session envoie l'INSERT et valide la transaction
            for utilisateur in utilisateurs:
                session.refresh(utilisateur)   # 3. on recharge l'objet depuis la base, pour récupérer son id
            requete = select(Utilisateur)
            utilisateurs = session.exec(requete).all()






# for utili in utilisateurs: 
#     print("Après l'enregistrement : Utilisateur.id =", utili.id)
#     print(repr(utili))


#user = Utilisateur(id=1, nom="HURBLAIN", prenom="Loïc", email="loic.hurblain@gmail.com")

# print("Modèle Pydantic ?  ", issubclass(Utilisateur, pyd.BaseModel))
# print("Champs Pydantic   :", list(Utilisateur.model_fields))
# print("Table SQLAlchemy  :", Utilisateur.__table__.name)
# print("Colonnes de table :", list(Utilisateur.__table__.columns.keys()))


# Si vous utilisez Python 3.10 ou une version plus récente,
# vous pouvez vous passer complètement de Optional et utiliser
# le nouvel opérateur | (pipe),
# qui est plus propre et ne nécessite aucun import :
# id: Optional[int] = Field(
#     default=None, 
#     primary_key=True, 
#     sa_column_kwargs={"autoincrement": True}
# )









