"""Modèle Utilisateur (table SQL + objet Python) du projet CF-Tech.
 
Ce module définit la classe Utilisateur, qui regroupe les champs communs à
tous les profils de la plateforme (nom, prénom, email, etc.). Les profils
spécifiques (Apprenant, Formateur, Personnel...) y sont reliés par une clé
étrangère `id_utilisateur`.
"""

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
    """Utilisateur de la plateforme (table « utilisateur »).
 
    Cette classe est à la fois une table SQL et un objet Python. Elle porte
    les informations communes à tous les profils ; les données propres à un
    profil sont stockées dans la table de ce profil (ex. Apprenant).
 
    Attributs:
        id: Clé primaire auto-incrémentée (None tant que non inséré en base).
        nom: Nom de famille (50 caractères maximum).
        prenom: Prénom (50 caractères maximum).
        email: Adresse email valide (EmailStr), unique, 100 caractères maximum.
        date_creation: Date et heure de création du compte (UTC), remplie automatiquement.
        est_actif: Indique si le compte est actif (True par défaut).
    """
    # validate_assignment : revalide un champ à chaque affectation (u.email = ...)
    # Attention : un modèle table=True ne valide pas les données à la création
    # de l'objet ; cette validation se fait dans les schémas Pydantic.    model_config = pyd.ConfigDict(validate_assignment=True)
    
    id: int | None             = Field(default=None, primary_key=True)
    nom: str                   = Field(max_length=50)
    prenom: str                = Field(max_length=50)
    email: pyd.EmailStr        = Field(unique=True, max_length=100)
    date_creation: dt.datetime = Field(default_factory=lambda: dt.datetime.now(dt.timezone.utc), description="Date à la création de l'utilisateur")
    est_actif: bool            = Field(default=True, description="Etat actif du compte")

    def afficher(utilisateurs):
        """Affiche une liste d'objets SQLModel dans un tableau aligné (console).
 
        Appel : Utilisateur.afficher(liste)
 
        Les colonnes sont lues depuis le modèle (`model_fields`) : la méthode
        fonctionne donc pour n'importe quelle table, pas seulement Utilisateur.
 
        Args:
            utilisateurs: Liste d'objets SQLModel à afficher.
        """
        # Rien à afficher si la liste est vide
        if not utilisateurs:
            print("Aucune donnée.")
            return
        colonnes = list(type(utilisateurs[0]).model_fields)
        lignes = [[str(getattr(o, c)) for c in colonnes] for o in utilisateurs]

        # largeur de chaque colonne = valeur la plus longue (titre inclus)
        largeurs = [max(len(c), *(len(l[i]) for l in lignes))
                    for i, c in enumerate(colonnes)]

        print("  ".join(c.ljust(w) for c, w in zip(colonnes, largeurs)))
        for l in lignes:
            print("  ".join(v.ljust(w) for v, w in zip(l, largeurs)))


    def ajouter_utilisateurs(utilisateurs, engine):
        """
        
        """
        with Session(engine) as session:
            session.add_all(utilisateurs)       # 1. on confie l'objet à la session (rien n'est encore écrit)
            session.commit()        # 2. la session envoie l'INSERT et valide la transaction
            for utilisateur in utilisateurs:
                session.refresh(utilisateur)   # 3. on recharge l'objet depuis la base, pour récupérer son id






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









